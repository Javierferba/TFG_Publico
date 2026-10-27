# Resumen de rendimiento — Resultados_Evaluacion_Modelos

Fecha:
2026-05-29 07:46 UTC

## Resumen general por modelo y prompt

| Modelo | Prompt | Archivo | Casos | Aciertos | Precisión |
|---|---|---:|---:|---:|---:|
| LoRA_Qwen_Qwen3.5-0.8B | prompt2 | LoRA_Qwen_Qwen3.5-0.8B_prompt2.csv | 125 | 120 | 0.960 |
| LoRA_Qwen_Qwen3.5-2B | prompt2 | LoRA_Qwen_Qwen3.5-2B_prompt2.csv | 125 | 123 | 0.984 |
| LoRA_Qwen_Qwen3.5-4B | prompt2 | LoRA_Qwen_Qwen3.5-4B_prompt2.csv | 125 | 117 | 0.936 |
| LoRA_google_gemma-3-1b-it | prompt2 | LoRA_google_gemma-3-1b-it_prompt2.csv | 125 | 111 | 0.888 |

## Rendimiento por archivo y por texto (doc_id)

### LoRA_Qwen_Qwen3.5-0.8B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| TextoAnotadoChatGPT_02_FinalizacionDeTratamientoYNefrologia | 15 | 15 | 1.000 |
| TextoAnotadoGemini_01_EstabilidadHemodinamicaYPruebasEspecificas | 37 | 36 | 0.973 |
| TextoAnotadoGemini_01_NeurologiaYPruebasMotorasFinales | 73 | 69 | 0.945 |

### LoRA_Qwen_Qwen3.5-2B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| TextoAnotadoChatGPT_02_FinalizacionDeTratamientoYNefrologia | 15 | 15 | 1.000 |
| TextoAnotadoGemini_01_EstabilidadHemodinamicaYPruebasEspecificas | 37 | 37 | 1.000 |
| TextoAnotadoGemini_01_NeurologiaYPruebasMotorasFinales | 73 | 71 | 0.973 |

### LoRA_Qwen_Qwen3.5-4B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| TextoAnotadoChatGPT_02_FinalizacionDeTratamientoYNefrologia | 15 | 10 | 0.667 |
| TextoAnotadoGemini_01_EstabilidadHemodinamicaYPruebasEspecificas | 37 | 36 | 0.973 |
| TextoAnotadoGemini_01_NeurologiaYPruebasMotorasFinales | 73 | 71 | 0.973 |

### LoRA_google_gemma-3-1b-it_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| TextoAnotadoChatGPT_02_FinalizacionDeTratamientoYNefrologia | 15 | 15 | 1.000 |
| TextoAnotadoGemini_01_EstabilidadHemodinamicaYPruebasEspecificas | 37 | 37 | 1.000 |
| TextoAnotadoGemini_01_NeurologiaYPruebasMotorasFinales | 73 | 59 | 0.808 |

## Abreviaturas con mayor frecuencia de fallo (global)

Todas las abreviaturas ordenadas de más fallos a menos (suma sobre todos los archivos, modelos y prompts).

| Abreviatura | Ocurrencias | Fallos | Tasa de fallo |
|---|---:|---:|---:|
| III | 8 | 6 | 0.750 |
| ºC | 28 | 5 | 0.179 |
| UPDRS | 8 | 4 | 0.500 |
| Hg | 48 | 2 | 0.042 |
| Tª | 8 | 2 | 0.250 |
| ACO | 4 | 1 | 0.250 |
| AP | 4 | 1 | 0.250 |
| CV | 4 | 1 | 0.250 |
| DAA | 4 | 1 | 0.250 |
| EA | 4 | 1 | 0.250 |
| EF | 4 | 1 | 0.250 |
| EVA | 4 | 1 | 0.250 |
| GCS | 4 | 1 | 0.250 |
| IT | 4 | 1 | 0.250 |
| ROT's | 4 | 1 | 0.250 |
| mm | 48 | 0 | 0.000 |
| NRL | 28 | 0 | 0.000 |
| PAD | 24 | 0 | 0.000 |
| PAS | 24 | 0 | 0.000 |
| rpm | 24 | 0 | 0.000 |
| FiO2 | 20 | 0 | 0.000 |
| mg/dl | 20 | 0 | 0.000 |
| MVC | 16 | 0 | 0.000 |
| AC | 12 | 0 | 0.000 |
| AR | 12 | 0 | 0.000 |
| RCP | 12 | 0 | 0.000 |
| EE | 8 | 0 | 0.000 |
| lpm | 8 | 0 | 0.000 |
| ACV | 4 | 0 | 0.000 |
| APACHE | 4 | 0 | 0.000 |
| HD | 4 | 0 | 0.000 |
| IC | 4 | 0 | 0.000 |
| IY | 4 | 0 | 0.000 |
| L'x | 4 | 0 | 0.000 |
| LHI | 4 | 0 | 0.000 |
| NE | 4 | 0 | 0.000 |
| NIHSS | 4 | 0 | 0.000 |
| ON | 4 | 0 | 0.000 |
| RASS | 4 | 0 | 0.000 |
| RESP | 4 | 0 | 0.000 |
| RHA | 4 | 0 | 0.000 |
| RHY | 4 | 0 | 0.000 |
| ROTS | 4 | 0 | 0.000 |
| RS | 4 | 0 | 0.000 |
| SOFA | 4 | 0 | 0.000 |
| SaO2 | 4 | 0 | 0.000 |
| TAM | 4 | 0 | 0.000 |
| TP | 4 | 0 | 0.000 |
| TR | 4 | 0 | 0.000 |
| TVOP | 4 | 0 | 0.000 |
| UCI | 4 | 0 | 0.000 |
| VHC | 4 | 0 | 0.000 |
| mmHg | 4 | 0 | 0.000 |
| pc | 4 | 0 | 0.000 |