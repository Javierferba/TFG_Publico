<div align="center">

# 🩺 DesambiMED
### Desambiguación de Terminología Médica en Informes Hospitalarios

*Trabajo de Fin de Grado — Grado en Ingeniería Informática*
*Escuela Politécnica Superior de Jaén · Universidad de Jaén*

![Estado](https://img.shields.io/badge/estado-TFG%20completado-2ea44f)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API%20REST-000000?logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-Transformers-ee4c2c?logo=pytorch&logoColor=white)
![LaTeX](https://img.shields.io/badge/memoria-LaTeX-008080?logo=latex&logoColor=white)
![NLP](https://img.shields.io/badge/dominio-PLN%20cl%C3%ADnico-e6007e)
![Licencia](https://img.shields.io/badge/licencia-CC%20BY--NC--SA%204.0-lightgrey)

</div>

---

## 🎯 ¿De qué va este proyecto?

Los informes hospitalarios están **saturados de siglas y abreviaturas** (`FA`, `ECG`, `IAM`…). Muchas son **polisémicas**: una misma sigla puede significar cosas distintas según el contexto, lo que genera confusión entre profesionales e incluso errores clínicos. Algunos estudios registran tasas de error cercanas al **43 %** al descifrar abreviaturas entre facultativos de la *misma* especialidad.

**DesambiMED** aborda este problema desde el Procesamiento del Lenguaje Natural. Es, ante todo, un **estudio de evaluación comparativa**: mide en qué medida distintos **Modelos de Lenguaje Pequeños** (*Small Language Models*, < 5B de parámetros) son capaces de **desambiguar automáticamente** las siglas médicas de informes de alta reales, eligiendo la expansión correcta según el contexto.

La pregunta central: **¿puede un modelo ligero, ejecutable en una GPU de consumo y sin salir del hospital, resolver esta tarea con precisión clínicamente admisible?**

> 💡 La restricción no es anecdótica: la privacidad de los datos clínicos **excluye la nube**, así que todo el sistema está pensado para ejecutarse **en local** ("privacidad soberana"), con hardware modesto.

---

## 🏆 Resultados destacados

El trabajo demuestra empíricamente que **los SLMs de menos de 5B de parámetros bastan** para desambiguar terminología médica con precisión clínicamente admisible, **sin nube ni GPU de alta gama**. No hay un único ganador absoluto, sino una **recomendación según el escenario de despliegue**:

| Escenario | Modelo recomendado | Precisión (Corpus Médicos) | VRAM | Latencia |
|---|---|:---:|:---:|:---:|
| 🥇 **Máxima precisión clínica** | `Qwen3.5-4B` **(base)** | **91,6 %** | ~8,10 GB | ~1,03 s/consulta |
| ⚡ **Eficiencia / despliegue distribuido** | `Qwen3.5-2B` **(base)** | **86,3 %** | ~3,65 GB | ~0,72 s/consulta |

Otros hallazgos clave:

- 🧠 **El *prompting* importa tanto como el tamaño.** El **Prompt 2** (razonamiento por eliminación sobre una lista cerrada de candidatos del diccionario de la **SEDOM**) fue **la mejor estrategia de forma unánime** en todas las arquitecturas.
- ⚠️ **El *Chain-of-Thought* (Prompt 3) empeora** el rendimiento en modelos pequeños: agotan su atención generando la justificación y pierden el formato de salida.
- 🔧 **El modelo base supera a su versión LoRA** en el Corpus Médicos (`Qwen3.5-4B`: 91,6 % base vs. 90,6 % LoRA). Por eso **LoRA no se recomienda para maximizar precisión**; su valor real es la **adherencia al formato de salida** y la inmunidad al ruido sintáctico (el output de `LoRA_Qwen3.5-4B` es consumible sin postprocesado).
- 🎭 **El efecto de LoRA depende de la familia:** degrada a Qwen (−20,1 pts en 0.8B, −1,0 pts en 4B) pero es el único que **mejora** a `Gemma-3-1b-it` (**+13,4 pts**), al corregir su tendencia a respuestas conversacionales.

> 📈 Estas cifras provienen de la evaluación sobre el **Corpus Médicos** (anotado por cardiólogos), el estándar de referencia más exigente del trabajo.

---

## 🧪 El experimento en una cápsula

<table>
<tr>
<td><b>📚 Corpus</b></td>
<td>
Informes de alta de <b>cardiología</b> del Hospital Universitario de Jaén, anonimizados (RGPD).<br>
• <b>Corpus IA</b>: 125 instancias (anotación semi-automática con Gemini / ChatGPT vía Brat)<br>
• <b>Corpus Médicos</b>: 299 instancias (anotadas por <b>cardiólogos</b> — estándar de referencia)
</td>
</tr>
<tr>
<td><b>🤖 Modelos (7)</b></td>
<td>
<code>granite-4.0-h-350M</code>, <code>granite-4.0-h-1B</code> · <code>Qwen3.5-0.8B/2B/4B</code> · <code>gemma-3-1b-it</code>, <code>gemma-3-4b-it</code><br>
Tres familias: <b>IBM Granite</b>, <b>Qwen</b> y <b>Google Gemma</b>, todas por debajo de 5B de parámetros.
</td>
</tr>
<tr>
<td><b>💬 Prompts (3)</b></td>
<td>
1️⃣ Análisis de contexto médico · 2️⃣ Razonamiento por eliminación ✅ <i>(el mejor)</i> · 3️⃣ Consistencia documental (CoT)
</td>
</tr>
<tr>
<td><b>🔧 Ajuste fino</b></td>
<td>
<b>LoRA / QLoRA</b> (4 bits NF4, <code>r=16</code>, <code>α=32</code>) sobre 4 modelos: <code>Qwen3.5-0.8B/2B/4B</code> y <code>gemma-3-1b-it</code>.
</td>
</tr>
<tr>
<td><b>📊 Escala</b></td>
<td>
<b>25 configuraciones</b> de evaluación · más de <b>10.000</b> llamadas de inferencia.
</td>
</tr>
</table>

<details>
<summary>📋 <b>Tabla completa de precisión y eficiencia (modelos ajustados con LoRA)</b></summary>

| Configuración | Precisión | Latencia media | Max VRAM |
|---|:---:|:---:|:---:|
| `LoRA_Qwen3.5-0.8B` | 0,615 | 0,70 s | 1,53 GB |
| `LoRA_Gemma-3-1b-it` | 0,552 | 0,54 s | 2,10 GB |
| `LoRA_Qwen3.5-2B` | 0,826 | 0,72 s | 3,65 GB |
| `LoRA_Qwen3.5-4B` | 0,906 | 1,03 s | 8,10 GB |

*Precisión de los modelos base equivalentes sobre el Corpus Médicos: `Qwen3.5-0.8B` 81,6 % · `Qwen3.5-2B` 86,3 % · `Qwen3.5-4B` 91,6 % · `gemma-3-1b-it` 41,8 %.*

</details>

---

## 📂 Estructura del repositorio

```
DesambiMED/
│
├── 📁 Memoria/                      ← La memoria del TFG (LaTeX + PDF)
│   ├── main.pdf                     ← 📕 Memoria completa (léela aquí)
│   ├── main.tex · Portada.tex · Agradecimientos.tex · bibliografia.bib
│   ├── capitulos/                   ← Capítulos en .tex
│   ├── imagenes/                    ← Figuras y diagramas
│   ├── tablas/                      ← Tablas de ejemplo
│   └── Licencias/                   ← Iconos de licencias Creative Commons
│
├── 🛠️ plataformaAnotacion/          ← Herramienta de anotación web
│   ├── tagger_api.py                ← ⚙️ Servidor Flask (este es el que se arranca)
│   ├── index.html                   ← Interfaz web
│   ├── static/{app.js, styles.css}  ← Frontend
│   ├── abreviaciones.csv            ← Diccionario de siglas médicas (SEDOM)
│   ├── modeloBusqueda/              ← Modelo neuronal de detección (opcional)
│   └── scripts/                     ← Utilidades de mantenimiento del diccionario
│
├── 🧪 ScriptsModelo/                ← Pipeline experimental (reproducible)
│   ├── prompts.json                 ← Los 3 prompts evaluados
│   ├── test_modelo_prompt_automatico.py  ← Evalúa los modelos base
│   ├── fineTuning_Modelos.py        ← Ajuste fino LoRA/QLoRA
│   ├── test_modelo_fineTuned.py     ← Evalúa los modelos ajustados
│   └── generate_results_summary.py  ← Compila las métricas (summary.md)
│
├── 🤖 modelos_FineTuned/            ← Adaptadores LoRA ya entrenados
│   ├── LoRA_Qwen_Qwen3.5-0.8B/
│   ├── LoRA_Qwen_Qwen3.5-2B/
│   ├── LoRA_Qwen_Qwen3.5-4B/
│   └── LoRA_google_gemma-3-1b-it/
│       └── adapter_config.json · adapter_model.safetensors · tokenizer · chat_template
│
├── 📊 Documentacion/                ← Corpus, logs y resultados
│   ├── EDA/                         ← Corpus anotado en JSON (Train/Validation/Test)  ⚠️
│   ├── JSON_Nuevos/                 ← Salida de la herramienta de anotación
│   ├── Resultados_Evaluacion_Modelos_IA/         ← 21 CSV (base, Corpus IA) + summary.md
│   ├── Resultados_Evaluacion_Modelos_Medicos/    ← Resultados base sobre Corpus Médicos
│   ├── Resultados_Evaluacion_Modelos_Finetuned/  ← 4 CSV (LoRA) + summary.md
│   └── Resultados_Evaluacion_Modelos_FineTuned_Medicos/
│
├── requirements.txt
└── README.md
```

> ⚠️ **Privacidad:** por protección de datos, se han **eliminado los informes reales del HUJ** y cualquier archivo con información sensible. Las carpetas de `Documentacion/` que los contenían conservan un `README.txt` indicándolo, pero están vacías.

---

## 📕 La memoria (TFG)

La versión ya compilada está lista para leer en **[`Memoria/main.pdf`](Memoria/main.pdf)**.

<details>
<summary>🔨 <b>¿Quieres recompilarla desde las fuentes LaTeX?</b></summary>

Necesitas una distribución de LaTeX (TeX Live, MiKTeX…) con soporte para `babel`, `natbib`, `tikz` y `tcolorbox`. Desde la carpeta `Memoria/`:

```bash
# Opción recomendada (resuelve las pasadas de bibliografía automáticamente)
latexmk -pdf main.tex

# Opción manual equivalente
pdflatex main.tex
bibtex   main
pdflatex main.tex
pdflatex main.tex
```

El resultado es `main.pdf`. También puedes abrir `main.tex` directamente en **Overleaf**.

</details>

---

## 🛠️ Puesta en marcha: la herramienta de anotación

La memoria evalúa modelos, pero para ello hubo que construir un **corpus anotado por especialistas**. Con ese fin se desarrolló una **aplicación web** (arquitectura cliente-servidor) que permite a un cardiólogo anotar informes **sin conocimientos técnicos**.

### ✨ ¿Qué hace?

- 🔍 **Detecta automáticamente** las abreviaturas de un informe clínico.
- 📋 **Ofrece las expansiones candidatas** del diccionario para que el facultativo elija la correcta según el contexto.
- ➕ **Permite añadir** nuevas siglas no recogidas en el diccionario.
- 💾 **Exporta** cada anotación en **JSON estructurado**, listo para el pipeline de evaluación.
- ↩️ **Modo revisión**: reanuda o corrige documentos ya empezados.

### 🧩 Arquitectura

| Capa | Tecnología |
|---|---|
| **Backend** | Python + **Flask** (API REST, JSON) — `tagger_api.py` |
| **Frontend** | `index.html` + `static/app.js` + `static/styles.css` (+ Tailwind por CDN) |
| **Diccionario** | `abreviaciones.csv` (basado en el diccionario de siglas de la **SEDOM**) |
| **Detección** | Modelo neuronal `lmolino/extractor_abreviaciones` (Hugging Face) **con *fallback* automático** al diccionario CSV si no está disponible |

### 📋 Requisitos previos

- **Python 3.10+** y `pip`
- Un **navegador moderno** (Chrome, Firefox, Edge…)
- *(Opcional)* Una **GPU NVIDIA con CUDA** para acelerar la detección neuronal. Sin GPU, el modelo corre en CPU o, si no puede cargarse, la herramienta **sigue funcionando** en modo diccionario.

### 🚀 Instalación y arranque

**1. Crea y activa un entorno virtual** (recomendado):

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

**2. Instala las dependencias** desde la raíz del repositorio:

```bash
pip install -r requirements.txt
```

> ⚠️ Si `torch` viene fijado a una versión CUDA concreta (p. ej. `torch==2.9.1+cu130`) y tu equipo **no** tiene esa GPU, instala la versión de CPU desde [pytorch.org](https://pytorch.org/get-started/locally/) o elimina el sufijo `+cu130`. La herramienta funcionará igualmente con el diccionario.

**3. Arranca el servidor** desde la carpeta de la herramienta:

```bash
cd plataformaAnotacion
python tagger_api.py
```

Verás en consola el dispositivo detectado (GPU / CPU) y si el modelo se cargó. La herramienta queda disponible en:

```
🌐 http://localhost:5000/
```

### 🖥️ Modos de uso

| Modo | URL | Para qué sirve |
|---|---|---|
| 📝 **Normal** | `http://localhost:5000/` | Pegar un informe y anotarlo **desde cero** |
| 🔎 **Revisión** | `http://localhost:5000/<nombre_documento>` | **Reanudar o corregir** un documento ya pre-procesado (busca `<nombre_documento>.json` en `Documentacion/EDA/JSON_Nuevos/`) |

### 🎨 Código de colores de la interfaz

- 🟡 **Amarillo** → pendiente: hay varias opciones, aún sin elegir.
- 🔵 **Azul** → auto-asignada: solo había una opción posible (conviene revisarla).
- 🟢 **Verde** → confirmada por el anotador.

<details>
<summary>🔌 <b>Endpoints de la API</b></summary>

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Interfaz en modo normal |
| `GET` | `/<doc_name>` | Interfaz en modo revisión |
| `GET` | `/api/abreviaciones` | Devuelve el diccionario completo (JSON) |
| `GET` | `/api/model-status` | Estado del modelo neuronal |
| `POST` | `/api/process-text` | Tokeniza el texto y detecta abreviaturas |
| `POST` | `/api/add-abbreviation` | Añade una sigla nueva al diccionario |
| `POST` | `/api/save-json` | Persiste la anotación en JSON |

</details>

<details>
<summary>📄 <b>Formatos de datos (diccionario y salida)</b></summary>

**Diccionario `abreviaciones.csv`:**

```csv
Abreviacion,Definicion,Facultativo
AChA,Arteria coroidea anterior.,NO
DMNID,Diabetes mellitus no insulinodependiente.,NO
```

- **Abreviacion** — la sigla o abreviatura.
- **Definicion** — su expansión. Una misma sigla puede aparecer en varias filas (varias acepciones): ahí entra la desambiguación.
- **Facultativo** — `SI` si la añadió un médico durante la anotación, `NO` en caso contrario.

**Salida JSON anotada:**

```json
{
  "docid": "cardiologia_001",
  "text": "El paciente presenta FA con respuesta ventricular...",
  "abbreviations": [
    { "char_begin": 22, "char_end": 24, "text": "FA", "meaning": "Fibrilación auricular" }
  ]
}
```

> 📖 El **Apéndice B** de la memoria contiene el manual de usuario completo, paso a paso.

</details>

---

## 🔬 Reproducir los experimentos

El pipeline experimental vive en **`ScriptsModelo/`** y es reproducible. Los tres prompts se definen en `prompts.json`, y la evaluación se parametriza por modelo y prompt (o por lotes con todas las combinaciones).

```bash
# 1. Evaluar los modelos base con los prompts (fase base)
python ScriptsModelo/test_modelo_prompt_automatico.py

# 2. Ajustar finamente los modelos con LoRA/QLoRA
python ScriptsModelo/fineTuning_Modelos.py

# 3. Evaluar los modelos ya ajustados
python ScriptsModelo/test_modelo_fineTuned.py

# 4. Compilar las métricas en un summary.md
python ScriptsModelo/generate_results_summary.py
```

Cada ejecución genera un CSV por combinación modelo-prompt en `Documentacion/Resultados_Evaluacion_Modelos_*`, con las columnas `doc_id`, `abreviatura`, `acertado` (0/1), significado correcto y significado elegido. Los adaptadores LoRA ya entrenados se incluyen en **`modelos_FineTuned/`**.

> 🔧 Revisa los parámetros configurables al inicio de cada script (modelo, versión de prompt, rutas) antes de lanzarlo.

---

## 🔒 Datos y privacidad

El corpus procede de informes clínicos reales **cedidos por el Hospital Universitario de Jaén** y **anonimizados** conforme al **RGPD (UE 2016/679)** y la **LOPDGDD 3/2018**. Por ese motivo, **los datos clínicos NO se distribuyen** en este repositorio. Todo el procesamiento de la herramienta es **local**: ningún texto sale del equipo.

---

## 🌍 Objetivos de Desarrollo Sostenible

El proyecto se alinea con la **Agenda 2030** (ODS 3 *Salud y bienestar*, ODS 4, ODS 10, ODS 12, ODS 13 y ODS 15), priorizando modelos **eficientes en recursos** para reducir la huella computacional de la IA aplicada a la salud.

---

## 👤 Autoría y créditos

| Rol | Persona |
|---|---|
| ✍️ **Autor** | Javier Fernández Basso |
| 👨‍🏫 **Tutores** | Manuel Carlos Díaz Galiano · Lucas Molino Piñar |
| 🏛️ **Centro** | Escuela Politécnica Superior de Jaén · Universidad de Jaén |

---

## 📜 Licencia

[![Licencia: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es)

Este trabajo (memoria, código de la herramienta y resultados) se distribuye bajo la licencia **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**.

Esto significa que puedes **copiar, redistribuir, remezclar, transformar y crear a partir del material**, siempre que:

- 🖊️ **Atribución** — cites correctamente la autoría (ver cita sugerida más abajo).
- 🚫 **NoComercial** — no lo utilices con fines comerciales.
- 🔁 **CompartirIgual** — si remezclas, transformas o creas a partir del material, debes distribuir tu contribución bajo **la misma licencia** que el original.

Se eligió deliberadamente **SA en lugar de ND** para permitir que otros trabajos de investigación puedan **construir sobre este** (ampliar el corpus, adaptar el diccionario de siglas, mejorar la herramienta…), del mismo modo en que este TFG se apoya en trabajos previos (véase el Estado del arte de la memoria).

Licencia completa: **https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es**

> El **corpus clínico no se incluye** en este repositorio por razones de privacidad.

### 📎 Cómo citar este trabajo

```
Fernández Basso, J. (2026). Desambiguación de Terminología Médica en Informes
Hospitalarios (DesambiMED) [Trabajo de Fin de Grado, Universidad de Jaén].
Directores: Manuel Carlos Díaz Galiano y Lucas Molino Piñar.
```

<details>
<summary>BibTeX</summary>

```bibtex
@mastersthesis{fernandezbasso2026desambimed,
  author       = {Fernández Basso, Javier},
  title        = {Desambiguación de Terminología Médica en Informes Hospitalarios (DesambiMED)},
  school       = {Universidad de Jaén},
  year         = {2026},
  type         = {Trabajo de Fin de Grado},
  note         = {Directores: Manuel Carlos Díaz Galiano y Lucas Molino Piñar}
}
```

</details>

<div align="center">

---

*Hacer los informes hospitalarios más claros, seguros y comprensibles — para profesionales y pacientes.* 🫀

</div>