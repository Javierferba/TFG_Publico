#!/usr/bin/env python3
import csv
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# ---------------------------------------------------------------------------
base = Path('Documentacion/Resultados_Evaluacion_Modelos_FineTuned_Medicos')
logs_base = Path('Documentacion/Logs_FineTuned')
out_md = base / 'summary.md'

files = sorted(base.glob('*.csv'))
if not files:
    print('No CSV files found in', base)
    raise SystemExit(1)

# Aggregators
# Estructura: (model, prompt, file, n, correct, total_time, max_vram)
model_prompt_stats = []  
per_file_doc_stats = {}  # file -> {doc_id: (n, correct)}

# Contadores globales de abreviaturas (todos los archivos, todos los modelos)
abbr_counts = Counter()    # abreviatura -> total ocurrencias
abbr_failures = Counter()  # abreviatura -> total fallos

for f in files:
    model_prompt = f.stem  # Ej: 'google_gemma-3-4b-it_prompt3'
    
    # Separar modelo y prompt
    if '_prompt' in model_prompt:
        model, prompt = model_prompt.rsplit('_prompt', 1)
        prompt = 'prompt' + prompt
    else:
        model = model_prompt
        prompt = ''

    n = 0
    correct = 0
    total_time = 0.0
    doc_stats = defaultdict(lambda: [0, 0])

    # 1. Leer CSV para métricas de acierto y tiempo
    with f.open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            n += 1
            
            # Obtener aciertos
            try:
                acertado = int(row.get('acertado', 0))
            except ValueError:
                acertado = 0
                
            # Obtener tiempos
            try:
                tiempo = float(row.get('tiempo_s', 0.0))
            except ValueError:
                tiempo = 0.0

            correct += acertado
            total_time += tiempo

            # Rendimiento por doc_id
            doc_id = row.get('doc_id', 'unknown')
            doc_stats[doc_id][0] += 1
            doc_stats[doc_id][1] += acertado

            # Contadores de fallos de abreviaturas
            abbr = row.get('abreviatura', '').strip()
            if abbr:
                abbr_counts[abbr] += 1
                if acertado == 0:
                    abbr_failures[abbr] += 1

    per_file_doc_stats[f.name] = doc_stats

    # 2. Buscar Peak VRAM en el log más actualizado
    max_vram = "N/A"
    if logs_base.exists():
        # Patrón esperado: ibm-granite_granite-4.0-h-350M_prompt1_*.log
        log_pattern = f"{model_prompt}_*.log"
        matching_logs = list(logs_base.glob(log_pattern))
        
        if matching_logs:
            # Obtener el log con fecha de modificación más reciente
            latest_log = max(matching_logs, key=lambda p: p.stat().st_mtime)
            
            # Regex para buscar "Max VRAM: X.XX GB" que genera test_modelo_prompt_automatico.py
            vram_pattern = re.compile(r"Max VRAM:\s*([\d\.]+)\s*GB")
            
            try:
                with latest_log.open('r', encoding='utf-8') as lf:
                    for line in lf:
                        match = vram_pattern.search(line)
                        if match:
                            max_vram = match.group(1)
            except Exception as e:
                print(f"Error leyendo log {latest_log}: {e}")

    # Guardar estadísticas globales para este CSV
    model_prompt_stats.append((model, prompt, f.name, n, correct, total_time, max_vram))


# ── GENERACIÓN DEL MARKDOWN ──────────────────────────────────────────────────
lines = []
lines.append('# Resumen de Evaluación de Modelos IA')
lines.append('')
lines.append(f'*Generado: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC*')
lines.append('')

# ── 1. Rendimiento Global ────────────────────────────────────────────────────
lines.append('## Rendimiento Global por Modelo y Prompt')
lines.append('')
lines.append('| Modelo | Prompt | Archivo | Casos | Aciertos | Precisión | Tiempo Total (s) | Tiempo Medio/Query (s) | Max VRAM (GB) |')
lines.append('|---|---|---|---:|---:|---:|---:|---:|---:|')

# Ordenar por modelo y luego por prompt
model_prompt_stats.sort(key=lambda x: (x[0], x[1]))

for model, prompt, fname, n, correct, t_total, vram in model_prompt_stats:
    acc = correct / n if n else 0.0
    t_medio = t_total / n if n else 0.0
    lines.append(f'| {model} | {prompt} | {fname} | {n} | {correct} | {acc:.3f} | {t_total:.2f} | {t_medio:.2f} | {vram} |')

lines.append('')

# ── 2. Rendimiento por archivo y doc_id ──────────────────────────────────────
lines.append('## Rendimiento por archivo y por texto (doc_id)')
lines.append('')
for fname, doc_stats in per_file_doc_stats.items():
    lines.append(f'### {fname}')
    lines.append('')
    lines.append('| doc_id | Casos | Aciertos | Precisión |')
    lines.append('|---|---:|---:|---:|')
    for doc, (n, corr) in sorted(doc_stats.items(), key=lambda x: x[0]):
        acc = corr / n if n else 0.0
        lines.append(f'| {doc} | {n} | {corr} | {acc:.3f} |')
    lines.append('')

# ── 3. Abreviaturas con mayor frecuencia de fallo (global) ───────────────────
lines.append('## Abreviaturas con mayor frecuencia de fallo (global)')
lines.append('')
lines.append('Todas las abreviaturas ordenadas de más fallos a menos (suma sobre todos los archivos, modelos y prompts).')
lines.append('')
lines.append('| Abreviatura | Ocurrencias | Fallos | Tasa de fallo |')
lines.append('|---|---:|---:|---:|')

# Orden: primero por nº de fallos desc, luego por ocurrencias desc, luego alfabético
ranked = sorted(
    abbr_counts.keys(),
    key=lambda a: (-abbr_failures[a], -abbr_counts[a], a.lower())
)

for a in ranked:
    fails = abbr_failures[a]
    total = abbr_counts[a]
    rate = fails / total if total else 0.0
    lines.append(f'| {a} | {total} | {fails} | {rate:.3f} |')

# Escribir a disco
try:
    with out_md.open('w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    print(f'✅ Resumen generado exitosamente en: {out_md}')
except Exception as e:
    print(f'❌ Error al escribir el archivo {out_md}: {e}')