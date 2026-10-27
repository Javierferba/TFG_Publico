from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from buscador_abreviaciones import BuscadorAbreviaciones
from extractor_abreviaciones import ExtractorAbreviaciones

def main():
    RUTA_CSV_SIGLAS = "../../abreviaciones.csv"
    RUTA_PROMPT     = "./prompt_finetunig_terminos.txt"
    MODELO_HF       = "lmolino/extractor_abreviaciones"

    texto_medico = """
    El paciente presenta HTA y DM tipo 2. Se le administró paracetamol 500mg c/8h.
    Los valores de planta:TA fueron 140/90 mmHg. Se solicitó ECG y Rx de tórax.
    El diagnóstico indica IAM con elevación del ST.
    """

    print("="*60)
    print("SISTEMA DE EXTRACCION Y BUSQUEDA DE ABREVIACIONES MEDICAS")
    print("="*60)
    print(f"\nTexto a analizar:\n{texto_medico}\n")

    print(f"Cargando modelo '{MODELO_HF}' desde Hugging Face...")
    tokenizer = AutoTokenizer.from_pretrained(MODELO_HF)
    model = AutoModelForCausalLM.from_pretrained(
        MODELO_HF,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,  # FIX: era 'dtype'
        device_map="auto" if torch.cuda.is_available() else None
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        model = model.to(device)

    print(f"Modelo cargado en dispositivo: {device}")

    print("Inicializando extractor de abreviaciones...")
    extractor = ExtractorAbreviaciones(
        ruta_modelo=MODELO_HF,
        ruta_prompt=RUTA_PROMPT
    )

    print("\nExtrayendo abreviaciones del texto...")
    abreviaciones_encontradas = extractor.extraer_abreviaciones(
        model, tokenizer, texto_medico, device
    )

    print(f"\nSe encontraron {len(abreviaciones_encontradas)} abreviaciones:")
    for abrev in abreviaciones_encontradas:
        print(f"  - {abrev}")

    print(f"\nCargando diccionario de siglas desde '{RUTA_CSV_SIGLAS}'...")
    buscador = BuscadorAbreviaciones(RUTA_CSV_SIGLAS)
    print(f"Diccionario cargado con {len(buscador.diccionario_siglas)} entradas")

    print("\n" + "="*60)
    print("DEFINICIONES DE LAS ABREVIACIONES ENCONTRADAS")
    print("="*60)

    for abrev in sorted(abreviaciones_encontradas):
        definiciones = buscador.buscar_abreviacion(abrev)
        print(f"\n{abrev}:")
        if definiciones:
            for i, definicion in enumerate(definiciones, 1):
                print(f"  {i}. {definicion}")
        else:
            print(f"  No se encontro definicion en el diccionario")

    print("\n" + "="*60)
    print("Proceso completado")
    print("="*60)

if __name__ == "__main__":
    main()