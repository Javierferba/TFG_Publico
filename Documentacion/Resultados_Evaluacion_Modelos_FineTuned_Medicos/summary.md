# Resumen de Evaluación de Modelos IA

*Generado: 2026-06-16 02:43:30 UTC*

## Rendimiento Global por Modelo y Prompt

| Modelo | Prompt | Archivo | Casos | Aciertos | Precisión | Tiempo Total (s) | Tiempo Medio/Query (s) | Max VRAM (GB) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| LoRA_Qwen_Qwen3.5-0.8B | prompt2 | LoRA_Qwen_Qwen3.5-0.8B_prompt2.csv | 299 | 184 | 0.615 | 208.98 | 0.70 | N/A |
| LoRA_Qwen_Qwen3.5-2B | prompt2 | LoRA_Qwen_Qwen3.5-2B_prompt2.csv | 299 | 247 | 0.826 | 215.85 | 0.72 | N/A |
| LoRA_Qwen_Qwen3.5-4B | prompt2 | LoRA_Qwen_Qwen3.5-4B_prompt2.csv | 299 | 271 | 0.906 | 307.78 | 1.03 | N/A |
| LoRA_google_gemma-3-1b-it | prompt2 | LoRA_google_gemma-3-1b-it_prompt2.csv | 299 | 165 | 0.552 | 160.04 | 0.54 | N/A |

## Rendimiento por archivo y por texto (doc_id)

### LoRA_Qwen_Qwen3.5-0.8B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 20 | 0.714 |
| 120_Evolucion | 9 | 7 | 0.778 |
| 120_PruebasComplementarias | 136 | 74 | 0.544 |
| 121_Evolucion | 26 | 20 | 0.769 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 33 | 0.673 |
| 124_PruebasComplementarias | 43 | 25 | 0.581 |

### LoRA_Qwen_Qwen3.5-2B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 21 | 0.750 |
| 120_Evolucion | 9 | 7 | 0.778 |
| 120_PruebasComplementarias | 136 | 114 | 0.838 |
| 121_Evolucion | 26 | 23 | 0.885 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 43 | 0.878 |
| 124_PruebasComplementarias | 43 | 34 | 0.791 |

### LoRA_Qwen_Qwen3.5-4B_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 28 | 1.000 |
| 120_Evolucion | 9 | 9 | 1.000 |
| 120_PruebasComplementarias | 136 | 119 | 0.875 |
| 121_Evolucion | 26 | 26 | 1.000 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 44 | 0.898 |
| 124_PruebasComplementarias | 43 | 40 | 0.930 |

### LoRA_google_gemma-3-1b-it_prompt2.csv

| doc_id | Casos | Aciertos | Precisión |
|---|---:|---:|---:|
| 05_PruebasComplementarias | 28 | 18 | 0.643 |
| 120_Evolucion | 9 | 7 | 0.778 |
| 120_PruebasComplementarias | 136 | 62 | 0.456 |
| 121_Evolucion | 26 | 19 | 0.731 |
| 121_PlanTerapeutico copy | 8 | 5 | 0.625 |
| 121_PruebasComplementarias | 49 | 31 | 0.633 |
| 124_PruebasComplementarias | 43 | 23 | 0.535 |

## Abreviaturas con mayor frecuencia de fallo (global)

Todas las abreviaturas ordenadas de más fallos a menos (suma sobre todos los archivos, modelos y prompts).

| Abreviatura | Ocurrencias | Fallos | Tasa de fallo |
|---|---:|---:|---:|
| PCR | 36 | 24 | 0.667 |
| mm | 40 | 21 | 0.525 |
| VI | 24 | 21 | 0.875 |
| Vmax | 16 | 16 | 1.000 |
| IT | 28 | 15 | 0.536 |
| Mg | 20 | 15 | 0.750 |
| mg | 16 | 15 | 0.938 |
| Na | 24 | 11 | 0.458 |
| Cr | 24 | 9 | 0.375 |
| pH | 12 | 9 | 0.750 |
| Ca | 16 | 8 | 0.500 |
| Estenosis | 8 | 8 | 1.000 |
| MOD | 8 | 8 | 1.000 |
| Regurgitación | 8 | 8 | 1.000 |
| K | 24 | 7 | 0.292 |
| AI | 12 | 7 | 0.583 |
| cm | 12 | 7 | 0.583 |
| D | 8 | 7 | 0.875 |
| VA | 12 | 6 | 0.500 |
| BP | 8 | 6 | 0.750 |
| HTP | 8 | 6 | 0.750 |
| Ti | 8 | 6 | 0.750 |
| ST | 12 | 5 | 0.417 |
| VD | 12 | 5 | 0.417 |
| O2 | 8 | 5 | 0.625 |
| FE | 12 | 4 | 0.333 |
| RD | 8 | 4 | 0.500 |
| m | 4 | 4 | 1.000 |
| HDL | 8 | 3 | 0.375 |
| TVP | 8 | 3 | 0.375 |
| DVI | 4 | 3 | 0.750 |
| DVIs | 4 | 3 | 0.750 |
| F | 4 | 3 | 0.750 |
| III | 4 | 3 | 0.750 |
| OM | 4 | 3 | 0.750 |
| T | 4 | 3 | 0.750 |
| TT | 4 | 3 | 0.750 |
| TP | 8 | 2 | 0.250 |
| VT | 8 | 2 | 0.250 |
| atm | 4 | 2 | 0.500 |
| BR | 4 | 2 | 0.500 |
| FR | 4 | 2 | 0.500 |
| ICP | 4 | 2 | 0.500 |
| p | 4 | 2 | 0.500 |
| PCT | 4 | 2 | 0.500 |
| RC | 4 | 2 | 0.500 |
| s | 4 | 2 | 0.500 |
| SAT | 4 | 2 | 0.500 |
| TG | 4 | 2 | 0.500 |
| TnT | 4 | 2 | 0.500 |
| VTD | 4 | 2 | 0.500 |
| GGT | 16 | 1 | 0.062 |
| ml | 12 | 1 | 0.083 |
| CO2 | 8 | 1 | 0.125 |
| E/e' | 8 | 1 | 0.125 |
| BPM | 4 | 1 | 0.250 |
| m/seg | 4 | 1 | 0.250 |
| ms | 4 | 1 | 0.250 |
| Hb | 44 | 0 | 0.000 |
| mmHg | 28 | 0 | 0.000 |
| FG | 24 | 0 | 0.000 |
| BiPAP | 20 | 0 | 0.000 |
| Hto | 20 | 0 | 0.000 |
| mm3 | 20 | 0 | 0.000 |
| m/s | 16 | 0 | 0.000 |
| QRS | 16 | 0 | 0.000 |
| ECG | 12 | 0 | 0.000 |
| GPmáx | 12 | 0 | 0.000 |
| L/min | 12 | 0 | 0.000 |
| LDL | 12 | 0 | 0.000 |
| lpm | 12 | 0 | 0.000 |
| VCM | 12 | 0 | 0.000 |
| ALT | 8 | 0 | 0.000 |
| BT | 8 | 0 | 0.000 |
| Cx | 8 | 0 | 0.000 |
| EPAP | 8 | 0 | 0.000 |
| GSV | 8 | 0 | 0.000 |
| HCO3 | 8 | 0 | 0.000 |
| HCT | 8 | 0 | 0.000 |
| INR | 8 | 0 | 0.000 |
| IPAP | 8 | 0 | 0.000 |
| NTproBNP | 8 | 0 | 0.000 |
| Rx | 8 | 0 | 0.000 |
| SARS | 8 | 0 | 0.000 |
| TAPSE | 8 | 0 | 0.000 |
| TSH | 8 | 0 | 0.000 |
| V. | 8 | 0 | 0.000 |
| a. | 4 | 0 | 0.000 |
| AAS | 4 | 0 | 0.000 |
| ACOD | 4 | 0 | 0.000 |
| AVA | 4 | 0 | 0.000 |
| aVF | 4 | 0 | 0.000 |
| B12 | 4 | 0 | 0.000 |
| BD | 4 | 0 | 0.000 |
| BIPAP | 4 | 0 | 0.000 |
| C. | 4 | 0 | 0.000 |
| ColTotal | 4 | 0 | 0.000 |
| comp | 4 | 0 | 0.000 |
| CoV2 | 4 | 0 | 0.000 |
| CPAP | 4 | 0 | 0.000 |
| Creat | 4 | 0 | 0.000 |
| CX | 4 | 0 | 0.000 |
| Diam | 4 | 0 | 0.000 |
| Dimero | 4 | 0 | 0.000 |
| DM-2 | 4 | 0 | 0.000 |
| DVId | 4 | 0 | 0.000 |
| Dímero | 4 | 0 | 0.000 |
| Eco | 4 | 0 | 0.000 |
| eFG | 4 | 0 | 0.000 |
| ETT | 4 | 0 | 0.000 |
| FEVI | 4 | 0 | 0.000 |
| GSA | 4 | 0 | 0.000 |
| ICT | 4 | 0 | 0.000 |
| ISGLT2 | 4 | 0 | 0.000 |
| IST | 4 | 0 | 0.000 |
| iv | 4 | 0 | 0.000 |
| IVUS | 4 | 0 | 0.000 |
| JL | 4 | 0 | 0.000 |
| max | 4 | 0 | 0.000 |
| min | 4 | 0 | 0.000 |
| mL | 4 | 0 | 0.000 |
| Na+ | 4 | 0 | 0.000 |
| pCO2 | 4 | 0 | 0.000 |
| PPVId | 4 | 0 | 0.000 |
| PR | 4 | 0 | 0.000 |
| Pro-BNP | 4 | 0 | 0.000 |
| pro-BNP | 4 | 0 | 0.000 |
| ProBNP | 4 | 0 | 0.000 |
| QT | 4 | 0 | 0.000 |
| S' | 4 | 0 | 0.000 |
| SAHS | 4 | 0 | 0.000 |
| SAt | 4 | 0 | 0.000 |
| SatO2 | 4 | 0 | 0.000 |
| SIVd | 4 | 0 | 0.000 |
| SO2 | 4 | 0 | 0.000 |
| T4 | 4 | 0 | 0.000 |
| TGC | 4 | 0 | 0.000 |
| tr-band | 4 | 0 | 0.000 |
| TTPA | 4 | 0 | 0.000 |
| UCI | 4 | 0 | 0.000 |
| UI | 4 | 0 | 0.000 |
| V5-V6 | 4 | 0 | 0.000 |
| VfdVI | 4 | 0 | 0.000 |
