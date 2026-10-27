import os
import json
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

# --- CONFIGURACIÓN DE RUTAS ---
# BASE_DIR es la carpeta 'ScriptsModelo'
BASE_DIR      = os.path.dirname(os.path.abspath(__file__)) 
# ROOT_DIR ahora apunta a la raíz del proyecto 'TFG'
ROOT_DIR      = os.path.dirname(BASE_DIR)                  

# Ajustamos la ruta para que apunte directamente a 'modelos_fineTuned' en la raíz
TRAIN_DIR     = os.path.join(ROOT_DIR, "Documentacion", "EDA", "Final", "Train")
OUTPUT_DIR    = os.path.join(ROOT_DIR, "modelos_fineTuned")
PROMPTS_PATH   = os.path.join(ROOT_DIR, "ScriptsModelo", "prompts.json")

# --- PARÁMETROS ---
MODEL_NAME = "Qwen/Qwen3.5-4B"
PROMPT_VERSION = 2

def cargar_prompts(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        # Cargamos el JSON y convertimos las llaves a enteros para mantener compatibilidad
        data = json.load(f)
        return {int(k): v for k, v in data.items()}

# Sustituye el diccionario estático por esto:
PROMPT_TEMPLATES = cargar_prompts(PROMPTS_PATH)

# 1. FUNCIÓN PARA CARGAR Y FORMATEAR TUS JSON
def preparar_dataset_entrenamiento(train_dir, prompt_version):
    template = PROMPT_TEMPLATES.get(prompt_version)
    
    if not template:
        raise ValueError(f"ERROR: La versión de prompt '{prompt_version}' no se encuentra en {PROMPTS_PATH}. Revisa tu archivo JSON.")
    
    data_rows = []
    
    print(f"Buscando archivos JSON en: {train_dir}")
    for filename in os.listdir(train_dir):
        if not filename.endswith(".json"): continue
        
        with open(os.path.join(train_dir, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        texto_completo = data.get("text", "")
        
        for abbr in data.get("abbreviations", []):
            target     = abbr.get("text", "").strip()
            esperado   = abbr.get("meaning", "").strip()
            candidatos = abbr.get("candidates", [])

            if not target or not esperado: continue
            if not candidatos: candidatos = [esperado]

            opciones_str = "\n".join(f"- {c}" for c in candidatos)
            cb, ce = abbr.get("char_begin", 0), abbr.get("char_end", 0)
            frase  = texto_completo[max(0, cb - 100): min(len(texto_completo), ce + 100)]

            # 1. Generamos el prompt EXACTAMENTE igual que en la evaluación
            prompt_usuario = template.format(
                abreviatura    = target,
                opciones       = opciones_str,
                frase          = frase,
                texto_completo = texto_completo[:1500],
            )
            
            # 2. Generamos la respuesta que el modelo debe aprender a dar
            # ensure_ascii=False para que los acentos salgan bien
            respuesta_asistente = json.dumps({"eleccion": esperado}, ensure_ascii=False)
            
            # 3. Formato conversacional (El estándar moderno de SFTTrainer)
            data_rows.append({
                "messages": [
                    {"role": "user", "content": prompt_usuario},
                    {"role": "assistant", "content": respuesta_asistente}
                ]
            })
            
    print(f"Se han extraído {len(data_rows)} ejemplos de entrenamiento.")
    return Dataset.from_list(data_rows)

# Cargar dataset
dataset_train = preparar_dataset_entrenamiento(TRAIN_DIR, PROMPT_VERSION)

# 2. CONFIGURACIÓN DE CUANTIZACIÓN (QLoRA)
print("\nConfigurando QLoRA para optimizar VRAM...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# 3. CARGA DE MODELO Y TOKENIZADOR
print(f"Cargando modelo base: {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# Si el modelo no tiene pad_token, usamos el eos_token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
model.config.use_cache = False

model = prepare_model_for_kbit_training(model)

# 4. CONFIGURACIÓN DE LORA
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], # Máximo alcance para mejor aprendizaje
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 5. CONFIGURACIÓN DEL ENTRENAMIENTO

sft_config = SFTConfig(
    output_dir=OUTPUT_DIR,
    max_length=1500,           # ← renombrado de max_seq_length a max_length
    per_device_train_batch_size=4,      
    gradient_accumulation_steps=4,      
    optim="paged_adamw_32bit",          
    save_strategy="epoch",              
    save_total_limit=1,                 
    logging_steps=5,                   
    learning_rate=2e-4,                 
    num_train_epochs=3,                 
    bf16=True,                          
    warmup_steps=50,                   
    lr_scheduler_type="cosine",
    report_to="none",
    packing=False
)
# 6. INICIALIZAR EL ENTRENADOR
print("\nIniciando SFTTrainer...")

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset_train,
    peft_config=peft_config,
    args=sft_config,
    processing_class=tokenizer,
)

# Ejecutar entrenamiento
print("\n¡Configuración aceptada! Iniciando entrenamiento...")
trainer.train()

# 7. GUARDAR EL MODELO FINAL
ruta_final = os.path.join(OUTPUT_DIR, f"LoRA_{MODEL_NAME.replace('/', '_')}")
print(f"\nGuardando adaptador final en: {ruta_final}")
trainer.model.save_pretrained(ruta_final)
tokenizer.save_pretrained(ruta_final)
print("¡Entrenamiento completado!")