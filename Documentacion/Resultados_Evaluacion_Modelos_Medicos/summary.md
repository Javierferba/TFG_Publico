# Resumen de Evaluación de Modelos IA

*Generado: 2026-06-16 02:54:24 UTC*

## Rendimiento Global por Modelo y Prompt

| Modelo | Prompt | Archivo | Casos | Aciertos | Precisión | Tiempo Total (s) | Tiempo Medio/Query (s) | Max VRAM (GB) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Qwen_Qwen3.5-0.8B | prompt1 | Qwen_Qwen3.5-0.8B_prompt1.csv | 299 | 226 | 0.756 | 224.51 | 0.75 | N/A |
| Qwen_Qwen3.5-0.8B | prompt2 | Qwen_Qwen3.5-0.8B_prompt2.csv | 299 | 244 | 0.816 | 220.04 | 0.74 | N/A |
| Qwen_Qwen3.5-0.8B | prompt3 | Qwen_Qwen3.5-0.8B_prompt3.csv | 299 | 193 | 0.645 | 238.87 | 0.80 | N/A |
| Qwen_Qwen3.5-2B | prompt1 | Qwen_Qwen3.5-2B_prompt1.csv | 299 | 268 | 0.896 | 228.89 | 0.77 | N/A |
| Qwen_Qwen3.5-2B | prompt2 | Qwen_Qwen3.5-2B_prompt2.csv | 299 | 258 | 0.863 | 223.79 | 0.75 | N/A |
| Qwen_Qwen3.5-2B | prompt3 | Qwen_Qwen3.5-2B_prompt3.csv | 299 | 251 | 0.839 | 224.67 | 0.75 | N/A |
| Qwen_Qwen3.5-4B | prompt1 | Qwen_Qwen3.5-4B_prompt1.csv | 299 | 278 | 0.930 | 358.54 | 1.20 | N/A |
| Qwen_Qwen3.5-4B | prompt2 | Qwen_Qwen3.5-4B_prompt2.csv | 299 | 274 | 0.916 | 333.59 | 1.12 | N/A |
| Qwen_Qwen3.5-4B | prompt3 | Qwen_Qwen3.5-4B_prompt3.csv | 299 | 275 | 0.920 | 335.74 | 1.12 | N/A |
| google_gemma-3-1b-it | prompt1 | google_gemma-3-1b-it_prompt1.csv | 299 | 108 | 0.361 | 344.05 | 1.15 | N/A |
| google_gemma-3-1b-it | prompt2 | google_gemma-3-1b-it_prompt2.csv | 299 | 125 | 0.418 | 463.19 | 1.55 | N/A |
| google_gemma-3-1b-it | prompt3 | google_gemma-3-1b-it_prompt3.csv | 299 | 78 | 0.261 | 341.50 | 1.14 | N/A |
| google_gemma-3-4b-it | prompt1 | google_gemma-3-4b-it_prompt1.csv | 299 | 272 | 0.910 | 317.35 | 1.06 | N/A |
| google_gemma-3-4b-it | prompt2 | google_gemma-3-4b-it_prompt2.csv | 299 | 272 | 0.910 | 315.95 | 1.06 | N/A |
| google_gemma-3-4b-it | prompt3 | google_gemma-3-4b-it_prompt3.csv | 299 | 274 | 0.916 | 318.72 | 1.07 | N/A |
| ibm-granite_granite-4.0-h-1B | prompt1 | ibm-granite_granite-4.0-h-1B_prompt1.csv | 299 | 253 | 0.846 | 7720.65 | 25.82 | N/A |
| ibm-granite_granite-4.0-h-1B | prompt2 | ibm-granite_granite-4.0-h-1B_prompt2.csv | 299 | 238 | 0.796 | 8105.19 | 27.11 | N/A |
| ibm-granite_granite-4.0-h-1B | prompt3 | ibm-granite_granite-4.0-h-1B_prompt3.csv | 299 | 234 | 0.783 | 9165.74 | 30.65 | N/A |
| ibm-granite_granite-4.0-h-350M | prompt1 | ibm-granite_granite-4.0-h-350M_prompt1.csv | 299 | 73 | 0.244 | 4490.04 | 15.02 | N/A |
| ibm-granite_granite-4.0-h-350M | prompt2 | ibm-granite_granite-4.0-h-350M_prompt2.csv | 299 | 102 | 0.341 | 4973.23 | 16.63 | N/A |
| ibm-granite_granite-4.0-h-350M | prompt3 | ibm-granite_granite-4.0-h-350M_prompt3.csv | 299 | 61 | 0.204 | 3311.58 | 11.08 | N/A |

## Rendimiento por archivo y por texto (doc_id)

### Qwen_Qwen3.5-0.8B_prompt1.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 25 | 0.893 |
| 120_Evolucion | 9 | 8 | 0.889 |
| 120_PruebasComplementarias | 136 | 99 | 0.728 |
| 121_Evolucion | 26 | 22 | 0.846 |
| 121_PlanTerapeutico copy | 8 | 3 | 0.375 |
| 121_PruebasComplementarias | 49 | 34 | 0.694 |
| 124_PruebasComplementarias | 43 | 35 | 0.814 |

### Qwen_Qwen3.5-0.8B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 27 | 0.964 |
| 120_Evolucion | 9 | 8 | 0.889 |
| 120_PruebasComplementarias | 136 | 103 | 0.757 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 40 | 0.816 |
| 124_PruebasComplementarias | 43 | 35 | 0.814 |

### Qwen_Qwen3.5-0.8B_prompt3.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 24 | 0.857 |
| 120_Evolucion | 9 | 7 | 0.778 |
| 120_PruebasComplementarias | 136 | 81 | 0.596 |
| 121_Evolucion | 26 | 19 | 0.731 |
| 121_PlanTerapeutico copy | 8 | 6 | 0.750 |
| 121_PruebasComplementarias | 49 | 30 | 0.612 |
| 124_PruebasComplementarias | 43 | 26 | 0.605 |

### Qwen_Qwen3.5-2B_prompt1.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 26 | 0.929 |
| 120_Evolucion | 9 | 8 | 0.889 |
| 120_PruebasComplementarias | 136 | 120 | 0.882 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 43 | 0.878 |
| 124_PruebasComplementarias | 43 | 40 | 0.930 |

### Qwen_Qwen3.5-2B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 27 | 0.964 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 110 | 0.809 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 43 | 0.878 |
| 124_PruebasComplementarias | 43 | 38 | 0.884 |

### Qwen_Qwen3.5-2B_prompt3.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 26 | 0.929 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 106 | 0.779 |
| 121_Evolucion | 26 | 25 | 0.962 |
| 121_PlanTerapeutico copy | 8 | 6 | 0.750 |
| 121_PruebasComplementarias | 49 | 41 | 0.837 |
| 124_PruebasComplementarias | 43 | 38 | 0.884 |

### Qwen_Qwen3.5-4B_prompt1.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 28 | 1.000 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 124 | 0.912 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 45 | 0.918 |
| 124_PruebasComplementarias | 43 | 41 | 0.953 |

### Qwen_Qwen3.5-4B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 28 | 1.000 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 121 | 0.890 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 45 | 0.918 |
| 124_PruebasComplementarias | 43 | 40 | 0.930 |

### Qwen_Qwen3.5-4B_prompt3.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 28 | 1.000 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 121 | 0.890 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 46 | 0.939 |
| 124_PruebasComplementarias | 43 | 40 | 0.930 |

### google_gemma-3-1b-it_prompt1.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 14 | 0.500 |
| 120_Evolucion | 9 | 4 | 0.444 |
| 120_PruebasComplementarias | 136 | 39 | 0.287 |
| 121_Evolucion | 26 | 17 | 0.654 |
| 121_PlanTerapeutico copy | 8 | 2 | 0.250 |
| 121_PruebasComplementarias | 49 | 19 | 0.388 |
| 124_PruebasComplementarias | 43 | 13 | 0.302 |

### google_gemma-3-1b-it_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 14 | 0.500 |
| 120_Evolucion | 9 | 2 | 0.222 |
| 120_PruebasComplementarias | 136 | 51 | 0.375 |
| 121_Evolucion | 26 | 18 | 0.692 |
| 121_PlanTerapeutico copy | 8 | 3 | 0.375 |
| 121_PruebasComplementarias | 49 | 23 | 0.469 |
| 124_PruebasComplementarias | 43 | 14 | 0.326 |

### google_gemma-3-1b-it_prompt3.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 12 | 0.429 |
| 120_Evolucion | 9 | 5 | 0.556 |
| 120_PruebasComplementarias | 136 | 25 | 0.184 |
| 121_Evolucion | 26 | 12 | 0.462 |
| 121_PlanTerapeutico copy | 8 | 1 | 0.125 |
| 121_PruebasComplementarias | 49 | 14 | 0.286 |
| 124_PruebasComplementarias | 43 | 9 | 0.209 |

### google_gemma-3-4b-it_prompt1.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 28 | 1.000 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 122 | 0.897 |
| 121_Evolucion | 26 | 25 | 0.962 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 43 | 0.878 |
| 124_PruebasComplementarias | 43 | 40 | 0.930 |

### google_gemma-3-4b-it_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 28 | 1.000 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 120 | 0.882 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 44 | 0.898 |
| 124_PruebasComplementarias | 43 | 40 | 0.930 |

### google_gemma-3-4b-it_prompt3.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 27 | 0.964 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 122 | 0.897 |
| 121_Evolucion | 26 | 25 | 0.962 |
| 121_PlanTerapeutico copy | 8 | 8 | 1.000 |
| 121_PruebasComplementarias | 49 | 43 | 0.878 |
| 124_PruebasComplementarias | 43 | 40 | 0.930 |

### ibm-granite_granite-4.0-h-1B_prompt1.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 22 | 0.786 |
| 120_Evolucion | 9 | 8 | 0.889 |
| 120_PruebasComplementarias | 136 | 114 | 0.838 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 4 | 0.500 |
| 121_PruebasComplementarias | 49 | 42 | 0.857 |
| 124_PruebasComplementarias | 43 | 37 | 0.860 |

### ibm-granite_granite-4.0-h-1B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 20 | 0.714 |
| 120_Evolucion | 9 | 8 | 0.889 |
| 120_PruebasComplementarias | 136 | 107 | 0.787 |
| 121_Evolucion | 26 | 24 | 0.923 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 40 | 0.816 |
| 124_PruebasComplementarias | 43 | 34 | 0.791 |

### ibm-granite_granite-4.0-h-1B_prompt3.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 19 | 0.679 |
| 120_Evolucion | 9 | 7 | 0.778 |
| 120_PruebasComplementarias | 136 | 110 | 0.809 |
| 121_Evolucion | 26 | 25 | 0.962 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 38 | 0.776 |
| 124_PruebasComplementarias | 43 | 30 | 0.698 |

### ibm-granite_granite-4.0-h-350M_prompt1.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 8 | 0.286 |
| 120_Evolucion | 9 | 5 | 0.556 |
| 120_PruebasComplementarias | 136 | 39 | 0.287 |
| 121_Evolucion | 26 | 1 | 0.038 |
| 121_PlanTerapeutico copy | 8 | 1 | 0.125 |
| 121_PruebasComplementarias | 49 | 8 | 0.163 |
| 124_PruebasComplementarias | 43 | 11 | 0.256 |

### ibm-granite_granite-4.0-h-350M_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 14 | 0.500 |
| 120_Evolucion | 9 | 6 | 0.667 |
| 120_PruebasComplementarias | 136 | 42 | 0.309 |
| 121_Evolucion | 26 | 4 | 0.154 |
| 121_PlanTerapeutico copy | 8 | 4 | 0.500 |
| 121_PruebasComplementarias | 49 | 16 | 0.327 |
| 124_PruebasComplementarias | 43 | 16 | 0.372 |

### ibm-granite_granite-4.0-h-350M_prompt3.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 3 | 0.107 |
| 120_Evolucion | 9 | 0 | 0.000 |
| 120_PruebasComplementarias | 136 | 45 | 0.331 |
| 121_Evolucion | 26 | 0 | 0.000 |
| 121_PlanTerapeutico copy | 8 | 0 | 0.000 |
| 121_PruebasComplementarias | 49 | 5 | 0.102 |
| 124_PruebasComplementarias | 43 | 8 | 0.186 |

## Abreviaturas con mayor frecuencia de fallo (global)

Todas las abreviaturas ordenadas de más fallos a menos (suma sobre todos los archivos, modelos y prompts).

| Abreviatura | Ocurrencias | Fallos | Tasa de fallo |
|---|---:|---:|---:|
| PCR | 189 | 117 | 0.619 |
| Vmax | 84 | 81 | 0.964 |
| VI | 126 | 74 | 0.587 |
| IT | 147 | 72 | 0.490 |
| mm | 210 | 69 | 0.329 |
| mg | 84 | 62 | 0.738 |
| mmHg | 147 | 56 | 0.381 |
| K | 126 | 46 | 0.365 |
| Mg | 105 | 44 | 0.419 |
| Ca | 84 | 42 | 0.500 |
| Regurgitación | 42 | 40 | 0.952 |
| Cr | 126 | 37 | 0.294 |
| Hb | 231 | 34 | 0.147 |
| AI | 63 | 34 | 0.540 |
| Estenosis | 42 | 28 | 0.667 |
| Na | 126 | 26 | 0.206 |
| mm3 | 105 | 23 | 0.219 |
| D | 42 | 23 | 0.548 |
| GGT | 84 | 21 | 0.250 |
| MOD | 42 | 21 | 0.500 |
| pH | 63 | 20 | 0.317 |
| TP | 42 | 20 | 0.476 |
| L/min | 63 | 19 | 0.302 |
| LDL | 63 | 19 | 0.302 |
| VD | 63 | 19 | 0.302 |
| BiPAP | 105 | 18 | 0.171 |
| ml | 63 | 18 | 0.286 |
| m | 21 | 18 | 0.857 |
| FE | 63 | 17 | 0.270 |
| m/s | 84 | 16 | 0.190 |
| lpm | 63 | 16 | 0.254 |
| cm | 63 | 15 | 0.238 |
| VCM | 63 | 15 | 0.238 |
| RC | 21 | 15 | 0.714 |
| III | 21 | 14 | 0.667 |
| QRS | 84 | 13 | 0.155 |
| CO2 | 42 | 13 | 0.310 |
| HCT | 42 | 13 | 0.310 |
| HDL | 42 | 13 | 0.310 |
| NTproBNP | 42 | 13 | 0.310 |
| FG | 126 | 12 | 0.095 |
| GPmáx | 63 | 12 | 0.190 |
| ST | 63 | 12 | 0.190 |
| BT | 42 | 12 | 0.286 |
| TSH | 42 | 12 | 0.286 |
| F | 21 | 12 | 0.571 |
| s | 21 | 12 | 0.571 |
| ECG | 63 | 11 | 0.175 |
| VA | 63 | 11 | 0.175 |
| EPAP | 42 | 11 | 0.262 |
| HTP | 42 | 11 | 0.262 |
| O2 | 42 | 11 | 0.262 |
| RD | 42 | 11 | 0.262 |
| Rx | 42 | 11 | 0.262 |
| Ti | 42 | 11 | 0.262 |
| BR | 21 | 11 | 0.524 |
| min | 21 | 11 | 0.524 |
| OM | 21 | 11 | 0.524 |
| ALT | 42 | 10 | 0.238 |
| BP | 42 | 10 | 0.238 |
| SARS | 42 | 10 | 0.238 |
| TT | 21 | 10 | 0.476 |
| E/e' | 42 | 9 | 0.214 |
| HCO3 | 42 | 9 | 0.214 |
| TVP | 42 | 9 | 0.214 |
| AAS | 21 | 9 | 0.429 |
| ICT | 21 | 9 | 0.429 |
| SIVd | 21 | 9 | 0.429 |
| V. | 42 | 8 | 0.190 |
| VT | 42 | 8 | 0.190 |
| Diam | 21 | 8 | 0.381 |
| DVIs | 21 | 8 | 0.381 |
| pro-BNP | 21 | 8 | 0.381 |
| S' | 21 | 8 | 0.381 |
| GSV | 42 | 7 | 0.167 |
| IPAP | 42 | 7 | 0.167 |
| CX | 21 | 7 | 0.333 |
| Dimero | 21 | 7 | 0.333 |
| FR | 21 | 7 | 0.333 |
| mL | 21 | 7 | 0.333 |
| QT | 21 | 7 | 0.333 |
| T4 | 21 | 7 | 0.333 |
| VTD | 21 | 7 | 0.333 |
| CoV2 | 21 | 6 | 0.286 |
| DVI | 21 | 6 | 0.286 |
| GSA | 21 | 6 | 0.286 |
| JL | 21 | 6 | 0.286 |
| m/seg | 21 | 6 | 0.286 |
| ms | 21 | 6 | 0.286 |
| PCT | 21 | 6 | 0.286 |
| Pro-BNP | 21 | 6 | 0.286 |
| T | 21 | 6 | 0.286 |
| TG | 21 | 6 | 0.286 |
| TnT | 21 | 6 | 0.286 |
| UI | 21 | 6 | 0.286 |
| V5-V6 | 21 | 6 | 0.286 |
| Hto | 105 | 5 | 0.048 |
| Cx | 42 | 5 | 0.119 |
| aVF | 21 | 5 | 0.238 |
| BD | 21 | 5 | 0.238 |
| Dímero | 21 | 5 | 0.238 |
| ETT | 21 | 5 | 0.238 |
| ICP | 21 | 5 | 0.238 |
| IST | 21 | 5 | 0.238 |
| IVUS | 21 | 5 | 0.238 |
| max | 21 | 5 | 0.238 |
| pCO2 | 21 | 5 | 0.238 |
| SAT | 21 | 5 | 0.238 |
| VfdVI | 21 | 5 | 0.238 |
| INR | 42 | 4 | 0.095 |
| a. | 21 | 4 | 0.190 |
| atm | 21 | 4 | 0.190 |
| BIPAP | 21 | 4 | 0.190 |
| BPM | 21 | 4 | 0.190 |
| DVId | 21 | 4 | 0.190 |
| Eco | 21 | 4 | 0.190 |
| iv | 21 | 4 | 0.190 |
| p | 21 | 4 | 0.190 |
| PPVId | 21 | 4 | 0.190 |
| ProBNP | 21 | 4 | 0.190 |
| TTPA | 21 | 4 | 0.190 |
| ACOD | 21 | 3 | 0.143 |
| CPAP | 21 | 3 | 0.143 |
| DM-2 | 21 | 3 | 0.143 |
| eFG | 21 | 3 | 0.143 |
| ISGLT2 | 21 | 3 | 0.143 |
| Na+ | 21 | 3 | 0.143 |
| SAHS | 21 | 3 | 0.143 |
| SatO2 | 21 | 3 | 0.143 |
| SO2 | 21 | 3 | 0.143 |
| UCI | 21 | 3 | 0.143 |
| TAPSE | 42 | 2 | 0.048 |
| AVA | 21 | 2 | 0.095 |
| B12 | 21 | 2 | 0.095 |
| Creat | 21 | 2 | 0.095 |
| FEVI | 21 | 2 | 0.095 |
| PR | 21 | 2 | 0.095 |
| SAt | 21 | 2 | 0.095 |
| ColTotal | 21 | 1 | 0.048 |
| comp | 21 | 1 | 0.048 |
| TGC | 21 | 1 | 0.048 |
| C. | 21 | 0 | 0.000 |
| tr-band | 21 | 0 | 0.000 |
