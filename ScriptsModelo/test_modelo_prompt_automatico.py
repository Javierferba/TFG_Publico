#!/usr/bin/env python3
import json
import csv
import os
import re
import ast
import argparse
import string
import difflib
import logging
import time
import torch
from datetime import datetime
from transformers import pipeline, logging as hf_logging
from huggingface_hub import login

# ⚠️ Recuerda revocar este token cuando termines tu proyecto
login("TU_TOKEN_DE_HUGGINGFACE")

# Silenciar warnings de HuggingFace
hf_logging.set_verbosity_error()
logging.getLogger("transformers").setLevel(logging.ERROR)

# ---------------------------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# ---------------------------------------------------------------------------
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR      = os.path.dirname(BASE_DIR)

INPUT_DIR     = os.path.join(ROOT_DIR, "Documentacion", "EDA", "Final", "Test")
OUTPUT_FOLDER = os.path.join(ROOT_DIR, "Documentacion", "Resultados_Evaluacion_Modelos_Medicos")
PROMPTS_PATH  = os.path.join(ROOT_DIR, "ScriptsModelo", "prompts.json")
LOGS_FOLDER   = os.path.join(ROOT_DIR, "Documentacion", "Logs")
DICT_PATH     = os.path.join(ROOT_DIR, "prototipoVisualización", "abreviaciones.csv")

# --- PARÁMETROS DEL EXPERIMENTO ---
MODEL_NAME     = "Qwen/Qwen3.5-4B"
PROMPT_VERSION = 1

# ---------------------------------------------------------------------------
# LOGGER  (se configura al arrancar evaluar())
# ---------------------------------------------------------------------------
log = logging.getLogger("evaluador")


def setup_logger(model_name: str, prompt_version: int) -> logging.Logger:
    os.makedirs(LOGS_FOLDER, exist_ok=True)
    ts         = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_slug = model_name.replace("/", "_")
    log_file   = os.path.join(LOGS_FOLDER, f"{model_slug}_prompt{prompt_version}_{ts}.log")

    logger = logging.getLogger("evaluador")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s [%(levelname)-7s] %(message)s", "%H:%M:%S")

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info(f"=== Sesión | modelo={model_name} | prompt={prompt_version} ===")
    logger.info(f"Log: {log_file}")
    return logger


# ---------------------------------------------------------------------------
# CARGA DE DICCIONARIO GLOBAL DE ABREVIACIONES (Fallback de Candidatos)
# ---------------------------------------------------------------------------
def cargar_diccionario_abreviaciones(ruta_csv: str) -> dict:
    """
    Carga el CSV global para agrupar candidatos por cada abreviatura.
    Devuelve un diccionario { 'ECG': ['Electrocardiograma.', 'Ecocardiograma.'], ... }
    """
    dicc = {}
    if not os.path.exists(ruta_csv):
        ruta_csv = "abreviaciones.csv"
    
    if os.path.exists(ruta_csv):
        try:
            with open(ruta_csv, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                abbr_idx, def_idx = 0, 1
                if header:
                    for i, h in enumerate(header):
                        if "Abreviacion" in h or "abreviatura" in h.lower():
                            abbr_idx = i
                        if "Definicion" in h or "definicion" in h.lower() or "meaning" in h.lower():
                            def_idx = i
                
                for row in reader:
                    if len(row) > max(abbr_idx, def_idx):
                        a = row[abbr_idx].strip()
                        d = row[def_idx].strip()
                        if a and d:
                            if a not in dicc:
                                dicc[a] = []
                            if d not in dicc[a]:
                                dicc[a].append(d)
            print(f"✓ Diccionario global cargado con {len(dicc)} abreviaciones únicas.")
        except Exception as e:
            print(f"⚠ Alerta al cargar diccionario global: {e}")
    else:
        print(f"⚠ Archivo de diccionario global no encontrado en {ruta_csv}. No habrá fallback de candidatos.")
    return dicc


# ---------------------------------------------------------------------------
# CARGA DE PROMPTS
# ---------------------------------------------------------------------------
def cargar_prompts(ruta: str) -> dict:
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {int(k): v for k, v in data.items()}


try:
    PROMPT_TEMPLATES = cargar_prompts(PROMPTS_PATH)
except Exception:
    PROMPT_TEMPLATES = {}


# ---------------------------------------------------------------------------
# UTILIDADES DE TEXTO Y VALIDACIÓN
# ---------------------------------------------------------------------------
def normalizar_texto(texto: str) -> str:
    if not texto:
        return ""
    texto = texto.lower()
    for p in string.punctuation:
        texto = texto.replace(p, '')
    return " ".join(texto.split())


def _obtener_todos_los_strings(estructura) -> list:
    strings = []
    if isinstance(estructura, dict):
        for k, v in estructura.items():
            if isinstance(k, str):
                strings.append(k)
            strings.extend(_obtener_todos_los_strings(v))
    elif isinstance(estructura, (list, tuple, set)):
        for item in estructura:
            strings.extend(_obtener_todos_los_strings(item))
    elif isinstance(estructura, str):
        strings.append(estructura)
    return strings


def _extraer_de_dict(d: dict, candidatos: list) -> str:
    claves_objetivo = ("eleccion", "elección", "eleccion_correcta",
                       "definicion", "definición", "respuesta", "valor")
    d_lower = {k.lower(): v for k, v in d.items()}

    for clave in claves_objetivo:
        val = d_lower.get(clave)
        if not val:
            continue
        if isinstance(val, str) and val.strip():
            return val.strip()
        if isinstance(val, dict):
            sub_val = _extraer_de_dict(val, candidatos)
            if sub_val:
                return sub_val

    todos_los_valores = _obtener_todos_los_strings(d)
    for v in todos_los_valores:
        if not v.strip():
            continue
        v_norm = normalizar_texto(v)
        for c in candidatos:
            c_norm = normalizar_texto(c)
            if c_norm and (c_norm == v_norm or c_norm in v_norm or v_norm in c_norm):
                return c

    for v in todos_los_valores:
        if v.strip() and v.strip().lower() not in claves_objetivo:
            return v.strip()

    return ""


# ---------------------------------------------------------------------------
# ELIMINACIÓN DE BLOQUES DE RAZONAMIENTO (compatible con cualquier modelo)
# ---------------------------------------------------------------------------
# Patrones que indican inicio de razonamiento en texto libre (sin etiquetas).
# Se usa cuando el modelo no envuelve su CoT en <think>...</think>.
_THINK_HEADER_RE = re.compile(
    r'^(?:'
    r'thinking process'
    r'|thought process'
    r'|chain[- ]of[- ]thought'
    r'|step[- ]by[- ]step(?: reasoning| analysis)?'
    r'|my (?:reasoning|thinking|analysis|thought)'
    r'|reasoning process'
    r'|let me (?:think|analyze|reason)'
    r'|analysis'
    r')\s*[:\n]',
    re.IGNORECASE
)

# Marcadores que señalan el inicio de la conclusión final del modelo.
_CONCLUSION_RE = re.compile(
    r'(?:'
    r'\*{0,2}(?:final )?(?:answer|conclusion|elección|eleccion|respuesta|resultado)\*{0,2}'
    r'|therefore[,:]?'
    r'|in conclusion[,:]?'
    r'|(?:my |the )?(?:correct |best )?(?:choice|option|answer|selection) is[:\s]'
    r'|(?:la )?(?:opción|respuesta|elección) (?:correcta|final) (?:es|sería)[:\s]'
    r'|(?:elijo|selecciono|escojo)[:\s]'
    r')',
    re.IGNORECASE
)


def _eliminar_razonamiento(texto: str) -> str:
    """
    Elimina bloques de razonamiento del texto generado por el modelo.

    Maneja tres casos en orden:
      1. Etiquetas explícitas <think>...</think> (p.ej. modelos que usan CoT etiquetado).
      2. Cabeceras de razonamiento en texto libre seguidas de párrafos (p.ej. Qwen3.5
         que escribe 'Thinking Process:\n...').
      3. Si el texto resultante sigue siendo largo (>3 párrafos), intenta localizar
         un marcador de conclusión y quedarse sólo con esa parte final.

    Si ningún patrón detecta razonamiento, devuelve el texto original intacto.
    """
    # --- Caso 1: etiquetas <think>...</think> ---
    sin_think = re.sub(r'<think>.*?</think>', '', texto, flags=re.DOTALL).strip()
    if sin_think != texto:
        log.debug("    [filtro] bloque <think>...</think> eliminado")
        texto = sin_think

    # --- Caso 2: cabecera de razonamiento en texto libre ---
    parrafos = [p.strip() for p in texto.split('\n\n') if p.strip()]
    if parrafos and _THINK_HEADER_RE.match(parrafos[0]):
        # Buscar el primer párrafo que parezca una conclusión
        idx_conclusion = None
        for i, p in enumerate(parrafos[1:], 1):
            if _CONCLUSION_RE.search(p):
                idx_conclusion = i
                break
        if idx_conclusion is not None:
            log.debug(f"    [filtro] razonamiento libre eliminado; conclusión en párrafo {idx_conclusion}")
            texto = '\n\n'.join(parrafos[idx_conclusion:])
        else:
            # Sin marcador de conclusión: quedarse con el último párrafo
            log.debug("    [filtro] razonamiento libre eliminado (sin marcador); usando último párrafo")
            texto = parrafos[-1]

    # --- Caso 3: texto largo sin cabecera detectada pero con marcador de conclusión ---
    elif len(parrafos) > 3:
        for i, p in enumerate(parrafos):
            if _CONCLUSION_RE.search(p):
                log.debug(f"    [filtro] marcador de conclusión encontrado en párrafo {i}")
                texto = '\n\n'.join(parrafos[i:])
                break

    return texto.strip()


# ---------------------------------------------------------------------------
# PIPELINE ULTRA-ROBUSTO DE EXTRACCIÓN (Opción 4 Optimizado)
# ---------------------------------------------------------------------------
def extraer_eleccion(texto: str, candidatos: list) -> str:
    if not texto or not texto.strip():
        return "[sin respuesta]"

    texto = _eliminar_razonamiento(texto)
    texto_original = texto

    # Buscar desde el FINAL del texto para priorizar la conclusión del modelo
    texto_norm = normalizar_texto(texto)
    coincidencias_directas = []
    for c in candidatos:
        c_norm = normalizar_texto(c)
        if c_norm and c_norm in texto_norm:
            # rfind para coger la última aparición (más cercana a la conclusión)
            coincidencias_directas.append((texto_norm.rfind(c_norm), c))

    if coincidencias_directas:
        coincidencias_directas.sort(key=lambda x: x[0], reverse=True)
        log.debug(f"    [extracción robusta] Escaneo directo encontró candidato → '{coincidencias_directas[0][1][:60]}'")
        return coincidencias_directas[0][1]

    for pattern in [
        r'"elecc?i[oó]n"\s*:\s*"([^"]+)"',
        r'"definici[oó]n"\s*:\s*"([^"]+)"',
        r"'elecc?i[oó]n'\s*:\s*'([^']+)'",
        r"'definici[oó]n'\s*:\s*'([^']+)'",
    ]:
        m = re.search(pattern, texto, re.IGNORECASE)
        if m:
            res_campo = m.group(1).strip()
            log.debug(f"    [extracción] regex campo detectado → '{res_campo[:80]}'")
            
            res_campo_norm = normalizar_texto(res_campo)
            for c in candidatos:
                c_norm = normalizar_texto(c)
                if c_norm and (c_norm in res_campo_norm or res_campo_norm in c_norm):
                    return c
            texto = res_campo
            texto_norm = normalizar_texto(texto)
            break

    if texto == texto_original:
        dict_match = re.search(r'\{.*\}', texto, re.DOTALL)
        if dict_match:
            raw_dict = dict_match.group()
            try:
                data = json.loads(raw_dict)
                if isinstance(data, dict):
                    val = _extraer_de_dict(data, candidatos)
                    if val:
                        if val in candidatos:
                            return val
                        texto = val
                        texto_norm = normalizar_texto(texto)
            except json.JSONDecodeError:
                pass

            if texto == texto_original:
                try:
                    data = ast.literal_eval(raw_dict)
                    if isinstance(data, dict):
                        val = _extraer_de_dict(data, candidatos)
                        if val:
                            if val in candidatos:
                                return val
                            texto = val
                            texto_norm = normalizar_texto(texto)
                except Exception:
                    pass

    if texto in candidatos:
        return texto

    num_m = re.search(r'(?:opci[oó]n\s+|selecciono\s+la\s+)?\b(\d+)\b', texto, re.IGNORECASE)
    if num_m:
        idx = int(num_m.group(1))
        if 1 <= idx <= len(candidatos):
            log.debug(f"    [extracción] número de lista mapeado → candidato {idx}")
            return candidatos[idx - 1]

    if candidatos and texto_norm:
        scored = [(difflib.SequenceMatcher(None, normalizar_texto(c), texto_norm).ratio(), c)
                   for c in candidatos]
        best_s, best_c = max(scored, key=lambda x: x[0])
        log.debug(f"    [extracción] difflib robusto best={best_s:.2f} → '{best_c[:60]}'")
        if best_s >= 0.55:
            return best_c

    limpio = re.sub(r'[{}\"\'\[\]\\n\\r\\t]', ' ', texto).strip()
    return " ".join(limpio.split()) if limpio else "[sin respuesta]"


# ---------------------------------------------------------------------------
# INFERENCIA
# ---------------------------------------------------------------------------
def _es_modelo_qwen3(pipe) -> bool:
    """Detecta si el modelo es Qwen3 (cualquier variante) para aplicar enable_thinking=False."""
    try:
        nombre = pipe.model.config._name_or_path.lower()
        return "qwen3" in nombre or "qwen/qwen3" in nombre
    except Exception:
        return False


def call_model(prompt: str, pipe, candidatos: list) -> tuple:
    mensajes = [{"role": "user", "content": prompt}]

    # Qwen3 activa el modo thinking por defecto; se desactiva explícitamente
    # para evitar que el razonamiento agote el límite de tokens antes de la respuesta.
    # Otros modelos ignoran enable_thinking si su tokenizer no lo soporta.
    kwargs_template: dict = {"tokenize": False, "add_generation_prompt": True}
    if _es_modelo_qwen3(pipe):
        kwargs_template["enable_thinking"] = False
        log.debug("    [call_model] Qwen3 detectado → enable_thinking=False")

    try:
        prompt_formateado = pipe.tokenizer.apply_chat_template(mensajes, **kwargs_template)
    except TypeError:
        # El tokenizer no acepta enable_thinking; se reintenta sin él
        kwargs_template.pop("enable_thinking", None)
        try:
            prompt_formateado = pipe.tokenizer.apply_chat_template(mensajes, **kwargs_template)
        except Exception:
            prompt_formateado = prompt
    except Exception:
        prompt_formateado = prompt

    try:
        output = pipe(
            prompt_formateado,
            max_new_tokens=400,
            do_sample=False,
            temperature=0.0,
            repetition_penalty=1.0,
            pad_token_id=pipe.tokenizer.eos_token_id,
            return_full_text=False
        )
        raw = output[0]["generated_text"].strip()
        eleccion = extraer_eleccion(raw, candidatos)
        return eleccion, raw

    except Exception as e:
        log.error(f"  Error en inferencia: {e}")
        return "[sin respuesta]", ""


def cargar_modelo(model_name: str):
    device = 0 if torch.cuda.is_available() else -1
    pipe = pipeline(
        "text-generation",
        model=model_name,
        device=device,
        torch_dtype=torch.bfloat16 if device == 0 else torch.float32,
        trust_remote_code=True
    )
    if hasattr(pipe.model, "generation_config"):
        pipe.model.generation_config.max_length = None
    return pipe


# ---------------------------------------------------------------------------
# EVALUACIÓN PRINCIPAL CON MÉTRICAS METÓDICAS (TIEMPOS Y VRAM)
# ---------------------------------------------------------------------------
def evaluar(model_name: str = MODEL_NAME, prompt_version: int = PROMPT_VERSION):
    global log
    log = setup_logger(model_name, prompt_version)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_file = os.path.join(
        OUTPUT_FOLDER, f"{model_name.replace('/', '_')}_prompt{prompt_version}.csv"
    )

    template = PROMPT_TEMPLATES.get(prompt_version)
    if template is None:
        log.error(f"Versión de prompt '{prompt_version}' no definida.")
        return

    # Inicialización y reinicio de picos CUDA
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    # Carga de diccionario global para robustez en candidatos faltantes
    dicc_global = cargar_diccionario_abreviaciones(DICT_PATH)

    log.info(f"Cargando modelo: {model_name}")
    print(f"\nCargando modelo: {model_name} ...")
    
    t_start_model = time.monotonic()
    try:
        pipe = cargar_modelo(model_name)
        t_carga = time.monotonic() - t_start_model
        log.info(f"Modelo cargado correctamente en {t_carga:.2f} segundos.")
        print(f"✓ Modelo listo en {t_carga:.2f}s.\n")
    except Exception as e:
        log.error(f"Error al cargar el modelo: {e}")
        print(f"✗ Error al cargar el modelo: {e}")
        return

    if not os.path.exists(INPUT_DIR):
        log.error(f"Carpeta de entrada no encontrada: {INPUT_DIR}")
        return

    json_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    num_files  = len(json_files)
    log.info(f"Archivos JSON encontrados: {num_files}")
    print(f"Archivos encontrados: {num_files}")
    print(f"Salida: {output_file}\n" + "=" * 60)

    resultados = []
    total    = 0
    aciertos = 0
    start_total_eval = time.monotonic()

    for file_idx, filename in enumerate(json_files, 1):
        print(f"\n[{file_idx}/{num_files}] {filename}")
        log.info(f"── Archivo [{file_idx}/{num_files}]: {filename}")

        t_start_file = time.monotonic()

        try:
            with open(os.path.join(INPUT_DIR, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            log.error(f"Error leyendo {filename}: {e}")
            print(f"  ✗ Error leyendo {filename}: {e}")
            continue

        doc_id         = data.get("docid", filename)
        texto_completo = data.get("text", "")
        abreviaturas   = data.get("abbreviations", [])
        num_abbr       = len(abreviaturas)

        file_total    = 0
        file_aciertos = 0

        for abbr_idx, abbr in enumerate(abreviaturas, 1):
            target     = abbr.get("text", "").strip()
            esperado   = abbr.get("meaning", "").strip()
            candidatos = abbr.get("candidates") or []

            if not target or not esperado:
                continue
            
            # Fallback al diccionario si candidates no existe o viene vacío
            if not candidatos:
                if target in dicc_global and dicc_global[target]:
                    candidatos = list(dicc_global[target])
                    if esperado not in candidatos:
                        candidatos.append(esperado)
                else:
                    candidatos = [esperado]

            opciones_str = "\n".join(f"- {c}" for c in candidatos)
            cb, ce = abbr.get("char_begin", 0), abbr.get("char_end", 0)
            frase  = texto_completo[max(0, cb - 100): min(len(texto_completo), ce + 100)]

            prompt_final = template.format(
                abreviatura    = target,
                opciones       = opciones_str,
                frase          = frase,
                texto_completo = texto_completo[:1500],
            )

            log.debug(f"  [{abbr_idx}/{num_abbr}] abbr='{target}' "
                      f"| candidatos={len(candidatos)} "
                      f"| esperado='{esperado[:60]}'")

            # --- Medición temporal de la evaluación unitaria ---
            t_start_abbr = time.monotonic()
            try:
                eleccion, raw = call_model(prompt_final, pipe, candidatos)
                t_duration_abbr = time.monotonic() - t_start_abbr
                acertado = 1 if eleccion == esperado else 0

                if acertado:
                    log.debug(f"    ✓ ACIERTO | Tiempo: {t_duration_abbr:.2f}s")
                else:
                    log.warning(f"    ✗ FALLO | doc='{doc_id}' | abbr='{target}' | Tiempo: {t_duration_abbr:.2f}s")
                    log.warning(f"      esperado : '{esperado[:150]}'")
                    log.warning(f"      extraído : '{eleccion[:150]}'")
                    log.warning(f"      raw      : '{raw[:200]}'")

            except Exception as e:
                t_duration_abbr = time.monotonic() - t_start_abbr
                log.error(f"  Excepción en '{target}': {e}")
                print(f"  ⚠ Error en '{target}': {e}")
                eleccion, acertado = "[sin respuesta]", 0
                raw = ""

            aciertos      += acertado
            total         += 1
            file_aciertos += acertado
            file_total    += 1

            resultados.append({
                "doc_id"     : doc_id,
                "abreviatura": target,
                "esperado"   : esperado,
                "eleccion"   : eleccion,
                "acertado"   : acertado,
                "tiempo_s"   : round(t_duration_abbr, 3)
            })

            if abbr_idx % 5 == 0 or abbr_idx == num_abbr:
                prec = (aciertos / total * 100) if total else 0
                print(f"  [{abbr_idx}/{num_abbr}] — Acumulado: {aciertos}/{total} ({prec:.1f}%)")

        # Registro de rendimiento por Fichero e hilos CUDA
        t_duration_file = time.monotonic() - t_start_file
        vram_peak_file = torch.cuda.max_memory_allocated() / (1024 ** 3) if torch.cuda.is_available() else 0.0
        
        file_prec = (file_aciertos / file_total * 100) if file_total else 0
        log.info(f"  Resultado fichero: {file_aciertos}/{file_total} ({file_prec:.1f}%) | Tiempo: {t_duration_file:.2f}s | Pico VRAM: {vram_peak_file:.2f} GB")
        print(f"  ↳ Fichero evaluado en {t_duration_file:.2f}s | Precisión: {file_prec:.1f}% | Pico VRAM: {vram_peak_file:.2f} GB")

    # Guardar CSV mapeando la columna de tiempos de inferencia
    if resultados:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f, fieldnames=["doc_id", "abreviatura", "esperado", "eleccion", "acertado", "tiempo_s"]
            )
            writer.writeheader()
            writer.writerows(resultados)
        log.info(f"CSV guardado: {output_file}")
        print(f"\n✓ CSV guardado con columna de tiempos: {output_file}")

    t_total_eval = time.monotonic() - start_total_eval
    vram_peak_total = torch.cuda.max_memory_allocated() / (1024 ** 3) if torch.cuda.is_available() else 0.0

    final_prec = (aciertos / total * 100) if total else 0
    log.info(f"=== RESUMEN FINAL | {model_name} | prompt v{prompt_version} "
             f"| {final_prec:.2f}% ({aciertos}/{total}) | Tiempo Total: {t_total_eval:.2f}s | Max VRAM: {vram_peak_total:.2f} GB ===")
    
    print("\n" + "=" * 60)
    print(f" RESUMEN FINAL: {model_name} | Prompt v{prompt_version}")
    print(f" Precisión: {final_prec:.2f}% ({aciertos}/{total})")
    print(f" Tiempo Total de Evaluación: {t_total_eval:.2f} segundos")
    print(f" Pico máximo de VRAM alcanzado: {vram_peak_total:.2f} GB")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",  type=str, default=MODEL_NAME)
    parser.add_argument("--prompt", type=int, default=PROMPT_VERSION)
    args = parser.parse_args()
    evaluar(model_name=args.model, prompt_version=args.prompt)