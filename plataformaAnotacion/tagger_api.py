from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import csv
import os
import sys
import json

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR      = os.path.join(BASE_DIR, 'static')
ROOT_DIR        = os.path.dirname(BASE_DIR)
MODEL_DIR       = os.path.join(BASE_DIR, 'modeloBusqueda')
PROMPT_PATH     = os.path.join(MODEL_DIR, 'prompt_finetunnig_terminos.txt')
JSON_INPUT_DIR  = os.path.join(ROOT_DIR, 'Documentacion', 'EDA', 'JSON_Nuevos')  # carpeta con JSON de entrada para revisión. Modifícala a médicos para la revisión por parte de profesionales de textos ya formateados.
JSON_OUTPUT_DIR = os.path.join(ROOT_DIR, 'Documentacion', 'EDA', 'JSON_Nuevos')

sys.path.insert(0, MODEL_DIR)

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
CORS(app)

abbreviations_db = {}
_model        = None
_tokenizer    = None
_extractor    = None
_model_device = 'cpu'
_model_loaded = False
_model_error  = None


def _load_model():
    global _model, _tokenizer, _extractor, _model_device, _model_loaded, _model_error
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        from extractor_abreviaciones import ExtractorAbreviaciones

        MODELO_HF = "lmolino/extractor_abreviaciones"

        if torch.cuda.is_available():
            _model_device = "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            _model_device = "mps"
        else:
            _model_device = "cpu"

        print(f"\n  Dispositivo detectado: {_model_device.upper()}")
        print(f"  Cargando modelo '{MODELO_HF}'...")

        _tokenizer = AutoTokenizer.from_pretrained(MODELO_HF)
        _model = AutoModelForCausalLM.from_pretrained(
            MODELO_HF,
            torch_dtype=torch.float16 if _model_device != "cpu" else torch.float32,
            device_map="auto" if _model_device == "cuda" else None
        )

        if _model_device != "cuda":
            _model = _model.to(_model_device)

        _extractor = ExtractorAbreviaciones(
            ruta_modelo=MODELO_HF,
            ruta_prompt=PROMPT_PATH
        )

        _model_loaded = True
        print(f"  Modelo cargado correctamente en: {_model_device.upper()}")

    except Exception as e:
        _model_error  = str(e)
        _model_loaded = False
        print(f"  Modelo NO disponible: {e}")
        print(f"  Fallback activo: busqueda por diccionario CSV.")


def get_template():
    tpl_path = os.path.join(BASE_DIR, 'index.html')
    with open(tpl_path, 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/')
def index():
    return render_template_string(
        get_template(),
        mode='normal',
        doc_data='null',
        doc_name=''
    )


@app.route('/<doc_name>')
def review(doc_name):
    if '.' in doc_name:
        return 'Archivo no encontrado', 404

    json_path = os.path.join(JSON_INPUT_DIR, f'{doc_name}.json')

    if not os.path.exists(json_path):
        return (
            f'No se encontro el archivo {doc_name}.json en Documentacion/EDA/JSON/',
            300
        )

    with open(json_path, 'r', encoding='utf-8') as f:
        doc_data = json.load(f)

    return render_template_string(
        get_template(),
        mode='review',
        doc_data=json.dumps(doc_data),
        doc_name=doc_name
    )


@app.route('/api/model-status', methods=['GET'])
def model_status():
    return jsonify({
        'loaded':  _model_loaded,
        'device':  _model_device.upper() if _model_loaded else None,
        'error':   _model_error,
        'message': (
            f'Modelo activo en {_model_device.upper()}'
            if _model_loaded
            else f'Modelo no disponible - usando diccionario CSV. ({_model_error})'
        )
    })


@app.route('/api/abreviaciones', methods=['GET'])
def get_abbreviations():
    try:
        csv_path = os.path.join(BASE_DIR, 'abreviaciones.csv')

        if not os.path.exists(csv_path):
            return jsonify({
                'success': False,
                'error': 'No se encontro abreviaciones.csv en prototipoInicial/.'
            }), 404

        abbreviations_db.clear()

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            content = f.read().replace('\ufeff', '').strip()
            lines   = content.split('\n')

            start_index = 0
            if lines and lines[0].strip().lower().startswith('abreviacion'):
                start_index = 1

            count = 0
            for i in range(start_index, len(lines)):
                try:
                    row = list(csv.reader([lines[i]]))[0]
                except Exception:
                    continue

                if len(row) >= 2:
                    abbr    = row[0].strip()
                    meaning = row[1].strip()
                    context = row[2].strip() if len(row) > 2 else ''

                    key = abbr.upper()
                    if key not in abbreviations_db:
                        abbreviations_db[key] = []

                    abbreviations_db[key].append({
                        'meaning':  meaning,
                        'context':  context,
                        'original': abbr
                    })
                    count += 1

        return jsonify({
            'success':       True,
            'message':       (
                f'Cargadas {len(abbreviations_db)} abreviaciones unicas '
                f'({count} definiciones totales).'
            ),
            'abbreviations': abbreviations_db,
            'model_loaded':  _model_loaded,
            'model_status':  (
                f'Modelo ML activo ({_model_device.upper()})'
                if _model_loaded
                else 'Fallback: busqueda por diccionario CSV'
            )
        })

    except Exception as e:
        print(f"Error al cargar CSV: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/process-text', methods=['POST'])
def process_text():
    """
    Deteccion de abreviaciones con estrategia combinada:

      CON modelo activo:
        - El modelo detecta abreviaciones en el texto completo.
        - El diccionario CSV aporta las que el modelo pueda haber omitido.
        - Un token se marca si lo detecta el MODELO *o* si esta en el DICCIONARIO.
        - Esto maximiza el recall: ninguna abreviacion conocida se pierde.

      SIN modelo (fallback):
        - Solo se usan las entradas del diccionario CSV.
    """
    try:
        if not abbreviations_db:
            get_abbreviations()

        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No se proporciono texto'}), 400

        # --- TOKENIZACION ---
        words        = []
        current_word = ''
        text_norm    = text.replace('\r', '')

        for char in text_norm:
            if char in ' \t\n':
                if current_word:
                    words.append(current_word)
                    current_word = ''
                words.append(char)  # preserve el carácter real (\n, \t, espacio)
            else:
                current_word += char
        if current_word:
            words.append(current_word)

        # --- DETECCION CON MODELO ML ---
        model_detections = set()
        used_model       = False

        if _model_loaded:
            try:
                found = _extractor.extraer_abreviaciones(
                    _model, _tokenizer, text_norm, _model_device
                )
                # Normalizamos a mayusculas y tambien sin puntuacion de borde,
                # para que coincidan con los lookup_key de los tokens
                for a in found:
                    a_clean = a.strip().strip('.,;:!?()/\\-_ ')
                    if a_clean:
                        model_detections.add(a_clean.upper())

                used_model = True
                print(f"  Modelo detecto {len(model_detections)} abreviaciones: {model_detections}")
            except Exception as e:
                print(f"  Error en modelo ML: {e} - activando fallback de diccionario.")

        # --- CONSTRUCCION DE TOKENS ---
        result     = []
        abbr_index = 0

        for word in words:
            clean_word = word.strip('.,;:!?()/\\-_ ')

            # Descartar tokens sin ninguna letra ni numero (parentesis solos, guiones, etc.)
            if not any(c.isalnum() for c in clean_word):
                result.append({'type': 'text', 'text': word})
                continue

            lookup_key = clean_word.upper()
            in_dict    = lookup_key in abbreviations_db

            if used_model:
                # UNION: modelo O diccionario — maxima cobertura
                is_abbr = (lookup_key in model_detections) or in_dict
            else:
                # Fallback: solo diccionario
                is_abbr = in_dict

            if is_abbr:
                result.append({
                    'type':       'abbreviation',
                    'text':       word,
                    'clean':      clean_word,
                    'index':      abbr_index,
                    'options':    abbreviations_db.get(lookup_key, []),
                    'in_dict':    in_dict,
                    'used_model': used_model
                })
                abbr_index += 1
            else:
                result.append({'type': 'text', 'text': word})

        return jsonify({
            'success':    True,
            'tokens':     result,
            'used_model': used_model,
            'model_info': (
                f'Modelo ML + Diccionario ({_model_device.upper()})'
                if used_model
                else 'Diccionario CSV'
            )
        })

    except Exception as e:
        print(f"Error al procesar texto: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-abbreviation', methods=['POST'])
def add_abbreviation():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'success': False, 'error': 'No JSON body provided'}), 400

        abbr    = (data.get('abbreviation') or '').strip()
        meaning = (data.get('meaning') or '').strip()
        facultativo = bool(data.get('facultativo', False))
        if not abbr or not meaning:
            return jsonify({'success': False, 'error': 'Faltan campos abbreviation o meaning'}), 400

        csv_path = os.path.join(BASE_DIR, 'abreviaciones.csv')
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                csv.writer(f).writerow(['Abreviacion', 'Definicion', 'Facultativo'])

        key = abbr.upper()
        existing_meanings = [m['meaning'] for m in abbreviations_db.get(key, [])]
        if meaning in existing_meanings:
            return jsonify({'success': True, 'message': 'Definicion ya existente'}), 200

        # write row: use SI/NO depending on facultativo
        flag_str = 'SI' if facultativo else 'NO'
        with open(csv_path, 'a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow([abbr, meaning, flag_str])

        if key not in abbreviations_db:
            abbreviations_db[key] = []
        abbreviations_db[key].append({'meaning': meaning, 'context': '', 'original': abbr})

        return jsonify({'success': True, 'message': 'Anadida correctamente'}), 200

    except Exception as e:
        print(f"Error al anadir abreviacion: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/save-json', methods=['POST'])
def save_json():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'success': False, 'error': 'No JSON body provided'}), 400

        os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)

        docid    = (data.get('docid') or 'documento_anotado').strip()
        filename = f"{docid}.json"
        filepath = os.path.join(JSON_OUTPUT_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return jsonify({
            'success':  True,
            'message':  f'Guardado en Documentacion/EDA/JSON_Nuevos/{filename}',
            'filename': filename
        })

    except Exception as e:
        print(f"Error al guardar JSON: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
    _load_model()
    print("\n" + "="*70)
    print("  🏥  SERVIDOR DE ABREVIACIONES MÉDICAS")
    print("="*70)
    print(f"  ✅  Modo normal   → http://localhost:5000/")
    print(f"  📄  Modo revisión → http://localhost:5000/<nombre>")
    print(f"  📥  JSON entrada  → {JSON_INPUT_DIR}")
    print(f"  💾  JSON salida   → {JSON_OUTPUT_DIR}")
    print(f"  Modelo ML     -> {'ACTIVO en ' + _model_device.upper() if _model_loaded else 'NO DISPONIBLE (fallback: diccionario CSV)'}")
    print("="*70 + "\n")
    app.run(debug=True, port=5000)