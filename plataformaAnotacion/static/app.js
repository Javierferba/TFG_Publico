// Clean frontend implementation
const API_URL = 'http://localhost:5000';

// Fallback por si las variables de plantilla no están definidas (modo legacy)
if (typeof APP_MODE === 'undefined') window.APP_MODE = 'normal';
if (typeof DOC_DATA === 'undefined') window.DOC_DATA = null;

let abbreviations = {};
let processedData = [];
let currentAbbrIndex = null;
// no pending auto-save on close: user must press button or click option
let pendingSelectionText = null;

function getElement(id) {
    const el = document.getElementById(id);
    if (!el) console.warn(`No element with id ${id}`);
    return el;
}

window.addEventListener('DOMContentLoaded', async () => {
    const csvStatus = getElement('csvStatus');
    if (!csvStatus) return;

    csvStatus.textContent = 'Cargando diccionario...';
    try {
        const r = await fetch(`${API_URL}/api/abreviaciones`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = await r.json();
        if (!data.success) throw new Error(data.error || 'No data');
        abbreviations = data.abbreviations || {};
        csvStatus.textContent = `\u2713 ${data.message}`;

        // En modo normal habilitamos el botón de proceso
        const processBtn = getElement('processBtn');
        if (processBtn) processBtn.disabled = false;

        // IMPORTANTE: cargar el documento DESPUÉS de que el diccionario esté listo
        if (typeof APP_MODE !== 'undefined' && APP_MODE === 'review') {
            await loadReviewDocument();
        }

    } catch (e) {
        csvStatus.textContent = `Error cargando diccionario: ${e.message}`;
        const processBtn = getElement('processBtn');
        if (processBtn) processBtn.disabled = true;
    }
});


// ---------------------------------------------------------------------------
// MODO REVISIÓN: cargar documento pre-anotado
// ---------------------------------------------------------------------------

async function loadReviewDocument() {
    const out = getElement('tokenizedText');
    if (!out) return;

    if (!DOC_DATA) {
        out.textContent = 'Error: no se recibieron datos del documento.';
        return;
    }

    out.textContent = 'Cargando texto y abreviaciones...';

    try {
        const r = await fetch(`${API_URL}/api/process-text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: DOC_DATA.text })
        });
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = await r.json();
        if (!data.success) throw new Error(data.error || 'Error server');

        // Mapa de significados pre-anotados por posición de carácter
        const annotationMap = {};
        if (DOC_DATA.abbreviations && Array.isArray(DOC_DATA.abbreviations)) {
            DOC_DATA.abbreviations.forEach(a => {
                annotationMap[`${a.char_begin}-${a.char_end}`] = a.meaning;
            });
        }

        // Reconstruir índices de carácter y aplicar anotaciones
        let charCursor = 0;
        const text = DOC_DATA.text;

        processedData = data.tokens.map(t => {
            const tokenText = (t.clean || t.text || '').trim();

            if (!tokenText) {
                while (charCursor < text.length && /\s/.test(text[charCursor])) charCursor++;
                return t.type === 'abbreviation' ? { ...t, selected: null, isAuto: false } : t;
            }

            const foundAt = text.indexOf(tokenText, charCursor);
            if (foundAt !== -1) {
                const charBegin = foundAt;
                const charEnd = foundAt + tokenText.length;
                charCursor = charEnd;

                if (t.type === 'abbreviation') {
                    const preAnnotated = annotationMap[`${charBegin}-${charEnd}`];
                    if (preAnnotated) {
                        return { ...t, selected: preAnnotated, isAuto: false };
                    } else if (t.options && t.options.length === 1) {
                        return { ...t, selected: t.options[0].meaning, isAuto: true };
                    } else {
                        return { ...t, selected: null, isAuto: false };
                    }
                }
            }
            return t;
        });

        renderTokens(processedData);

    } catch (e) {
        if (out) out.textContent = `Error al cargar documento: ${e.message}`;
        console.error('loadReviewDocument error', e);
    }
}

async function processText() {
    const input = getElement('inputText');
    const out = getElement('tokenizedText');
    const processBtn = getElement('processBtn');
    if (!input || !out || !processBtn) return;

    processBtn.disabled = true;
    out.textContent = 'Procesando...';

    try {
        const r = await fetch(`${API_URL}/api/process-text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input.value })
        });
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        
        let data;
        try { data = await r.json(); } catch (e) { throw new Error('Respuesta no es JSON'); }
        if (!data.success) throw new Error(data.error || 'Error server');

        // 1. Preservar selecciones previas Y si eran automáticas
        const prevStates = {};
        processedData.forEach(t => {
            if (t.type === 'abbreviation' && t.selected) {
                const key = ((t.clean || t.text) + '').trim().toLowerCase();
                prevStates[key] = { selected: t.selected, isAuto: t.isAuto };
            }
        });

        // 2. Procesar nuevos tokens aplicando la lógica automática
        processedData = data.tokens.map(t => {
            if (t.type === 'abbreviation') {
                const key = ((t.clean || t.text) + '').trim().toLowerCase();
                const prevState = prevStates[key];
                
                let selected = null;
                let isAuto = false;

                if (prevState) {
                    // Restaurar estado anterior
                    selected = prevState.selected;
                    isAuto = prevState.isAuto;
                } else {
                    // SI NO hay estado previo, comprobar si tiene UNA ÚNICA opción
                    if (t.options && t.options.length === 1) {
                        selected = t.options[0].meaning;
                        isAuto = true; // Marcamos como automático
                    }
                }
                
                return { ...t, selected: selected, isAuto: isAuto };
            }
            return t;
        });
        
        renderTokens(processedData);
    } catch (e) {
        out.textContent = `Error: ${e.message}`;
        console.error('processText error', e);
    } finally {
        processBtn.disabled = false;
    }
}

function renderTokens(tokens) {
    const container = getElement('tokenizedText');
    if (!container) return;
    container.innerHTML = '';

    tokens.forEach(token => {
        if (token.type === 'abbreviation') {
            const span = document.createElement('span');
            span.classList.add('abbreviation');
            
            const disp = (token.text || '').replace(/\r/g, '');
            span.textContent = disp;
            span.dataset.index = token.index;
            
            // --- LÓGICA DE COLORES MODIFICADA ---
            if (token.selected === 'IGNORAR') {
                span.classList.add('ignored');
            } else if (token.selected) {
                // Si está seleccionado, miramos si es automático o manual
                if (token.isAuto) {
                    span.classList.add('auto-selected'); // AZUL
                    span.title = "Automático (Única opción) - Haz clic para confirmar";
                } else {
                    span.classList.add('selected'); // VERDE (Confirmado)
                }
            } else if (token.options && token.options.length > 0) {
                span.classList.add('pending'); // AMARILLO (Pendiente)
            }
            
            span.addEventListener('click', (e) => {
                e.stopPropagation();
                window.getSelection().removeAllRanges();
                openModalForIndex(token.index);
            });
            container.appendChild(span);
        } else {
            const rawText = (token.text || '').replace(/\r/g, '');
            // Preservar saltos de línea: dividir por \n e insertar <br>
            const parts = rawText.split('\n');
            parts.forEach((part, i) => {
                if (part) container.appendChild(document.createTextNode(part));
                if (i < parts.length - 1) container.appendChild(document.createElement('br'));
            });
        }
    });

    container.onmouseup = (e) => {
        const selObj = window.getSelection();
        const sel = selObj ? selObj.toString().trim() : '';
        if (sel && sel.length > 1) showAddNewModal(sel);
    };

    const gen = getElement('generateBtn');
    if (gen) gen.disabled = !tokens.some(t => t.type === 'abbreviation' && t.selected && t.selected !== 'IGNORAR');
}

function openModalForIndex(index) {
    const modal = getElement('modal');
    const options = getElement('optionsContainer');
    const modalText = getElement('modalAbbrText');
    const selectBtn = getElement('selectContextBtn');
    if (!modal || !options || !modalText || !selectBtn) return;

    const token = processedData.find(t => t.type === 'abbreviation' && t.index === index);
    if (!token) return;
    currentAbbrIndex = index;

    modalText.textContent = token.clean;
    options.innerHTML = '';
    const opts = (token.options || []);
    // dynamic sizing: adapt to content with fixed bottom padding and max height for scrolling
    options.style.height = 'auto';
    options.style.maxHeight = '600px';
    options.style.paddingBottom = '20px';
    options.style.overflowY = 'auto';

    opts.forEach(opt => {
        const div = document.createElement('div');
        const isCurrentlySelected = token.selected && token.selected === opt.meaning;
        div.className = 'option' + (isCurrentlySelected ? ' option-active' : '');
        div.innerHTML = `<p class="font-semibold">${opt.meaning}</p>`
            + (isCurrentlySelected ? '<span class="ml-2 text-xs bg-green-600 text-white px-2 py-0.5 rounded">\u2713 Seleccionada</span>' : '')
            + (opt.facultativo ? '<span class="ml-2 text-xs bg-blue-500 text-white px-2 rounded">Facultativo</span>' : '');
        // clicking an option now immediately applies it
        div.addEventListener('click', async () => {
            // apply meaning
            token.selected = opt.meaning;
            // IMPORTANTE: Al seleccionar manual, quitamos el automático para que se ponga verde
            token.isAuto = false;

            // also save this choice to the CSV so that picking a suggestion
            // behaves like the "seleccionar palabra" flow
            try {
                await addNewAbbreviation(token.clean, opt.meaning, opt.facultativo || false);
            } catch (e) {
                // ignore failures – the in‑memory state is already updated
                console.error('failed to persist selected option', e);
            }
            
            renderTokens(processedData);
            // close modal
            modal.style.display = 'none';
        });
        options.appendChild(div);
    });

    const customDiv = document.createElement('div');
    customDiv.className = 'mt-3';
    customDiv.innerHTML = `<label class='block font-semibold'>Añadir definición:</label><input id='modalCustomMeaning' class='w-full p-2 border rounded' placeholder='Nueva definición...'>`;
    options.appendChild(customDiv);

    // Set button label to new text
    selectBtn.textContent = 'Guardar otra definición';
    // Initially disabled until the user types a custom definition (or clicks an option)
    selectBtn.disabled = true;
    // enable when input has content
    setTimeout(() => {
        const inputEl = document.getElementById('modalCustomMeaning');
        if (inputEl) {
            inputEl.addEventListener('input', () => {
                selectBtn.disabled = !(inputEl.value && inputEl.value.trim().length > 0);
            });
        }
    }, 0);

    selectBtn.onclick = async () => {
        const custom = getElement('modalCustomMeaning').value.trim();
        if (!custom) return;
        const res = await addNewAbbreviation(token.clean, custom, true);
        if (res && res.success) {
            // Actualizar las opciones del token en memoria
            if (!token.options) token.options = [];
            if (!token.options.some(o => o.meaning === custom)) {
                token.options.push({ meaning: custom, context: '', original: token.clean });
            }
            // Actualizar el diccionario local (clave en MAYÚSCULAS, como usa el servidor)
            const key = (token.clean || '').toUpperCase();
            if (!abbreviations[key]) abbreviations[key] = [];
            if (!abbreviations[key].some(o => o.meaning === custom)) {
                abbreviations[key].push({ meaning: custom, context: '', original: token.clean });
            }
            token.selected = custom;
            token.isAuto = false;
            renderTokens(processedData);
            // Reabrir el modal para mostrar la nueva opción en la lista
            openModalForIndex(token.index);
        }
    };

    getElement('selectIgnoreBtn').onclick = () => {
        token.selected = 'IGNORAR';
        token.isAuto = false;
        renderTokens(processedData);
        modal.style.display = 'none';
    };

    // attach Enter handler to custom input to allow quick submit
    setTimeout(() => {
        const input = document.getElementById('modalCustomMeaning');
        if (input) {
            input.addEventListener('keydown', async (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const custom = input.value.trim();
                    if (!custom) return;
                    // same behavior as selectBtn
                    const res = await addNewAbbreviation(token.clean, custom, true);
                    if (res && res.success) {
                        if (!token.options) token.options = [];
                        if (!token.options.some(o => o.meaning === custom)) {
                            token.options.push({ meaning: custom, context: '', original: token.clean });
                        }
                        const key = (token.clean || '').toUpperCase();
                        if (!abbreviations[key]) abbreviations[key] = [];
                        if (!abbreviations[key].some(o => o.meaning === custom)) {
                            abbreviations[key].push({ meaning: custom, context: '', original: token.clean });
                        }
                        token.selected = custom;
                        token.isAuto = false; // Manual
                        renderTokens(processedData);
                        // Reabrir el modal para mostrar la nueva opción en la lista
                        openModalForIndex(token.index);
                    }
                }
            });
        }
    }, 0);

    modal.style.display = 'flex';
}

function showAddNewModal(selectedText) {
    const modal = getElement('modal');
    const options = getElement('optionsContainer');
    const modalText = getElement('modalAbbrText');
    const selectBtn = getElement('selectContextBtn');
    if (!modal || !options || !modalText || !selectBtn) return;

    modalText.textContent = selectedText;
    options.innerHTML = '';

    // style modal compact when there are no predefined options
    options.style.maxHeight = '220px';
    options.style.overflowY = 'auto';

    const customDiv = document.createElement('div');
    customDiv.innerHTML = `<label class='block font-semibold'>Definición para "${selectedText}":</label><input id='modalCustomMeaning' class='w-full p-2 border rounded' placeholder='Definición...'/>`;
    options.appendChild(customDiv);

    // Show button to save definition for this selected text
    selectBtn.textContent = 'Guardar otra definición';
    selectBtn.disabled = true;
    setTimeout(() => {
        const inputEl = document.getElementById('modalCustomMeaning');
        if (inputEl) {
            inputEl.addEventListener('input', () => {
                selectBtn.disabled = !(inputEl.value && inputEl.value.trim().length > 0);
            });
        }
    }, 0);

    selectBtn.onclick = async () => {
        const custom = getElement('modalCustomMeaning').value.trim();
        if (!custom) return;

        selectBtn.disabled = true;
        selectBtn.textContent = 'Guardando...';

        const res = await addNewAbbreviation(selectedText, custom, true);
        if (res && res.success) {
            // Actualizar diccionario local con clave en MAYÚSCULAS (igual que el servidor)
            const key = selectedText.trim().toUpperCase();
            if (!abbreviations[key]) abbreviations[key] = [];
            if (!abbreviations[key].some(o => o.meaning === custom)) {
                abbreviations[key].push({ meaning: custom, context: '', original: selectedText });
            }

            // Actualizar processedData: convertir tokens de texto que coincidan
            // en abreviaciones y marcarlos como seleccionados
            const stripPunct = s => s.replace(/^[.,;:!?()/\\|\-_ ]+|[.,;:!?()/\\|\-_ ]+$/g, '');
            const selLc = stripPunct(selectedText.trim()).toLowerCase();
            processedData.forEach(t => {
                const tokenClean = stripPunct(((t.clean || t.text || '') + '').trim()).toLowerCase();
                if (tokenClean === selLc) {
                    t.type = 'abbreviation';
                    t.clean = t.clean || stripPunct((t.text || '').trim());
                    if (!t.options) t.options = [];
                    if (!t.options.some(o => o.meaning === custom)) {
                        t.options.push({ meaning: custom, context: '', original: selectedText });
                    }
                    t.selected = custom;
                    t.isAuto = false;
                    if (t.index === undefined) {
                        const maxIdx = processedData
                            .filter(x => x.type === 'abbreviation' && x.index !== undefined)
                            .reduce((m, x) => Math.max(m, x.index), -1);
                        t.index = maxIdx + 1;
                    }
                }
            });

            renderTokens(processedData);
            modal.style.display = 'none';
        } else {
            selectBtn.disabled = false;
            selectBtn.textContent = 'Guardar definición';
        }
    };

    getElement('selectIgnoreBtn').onclick = () => modal.style.display = 'none';
    modal.style.display = 'flex';
}

async function addNewAbbreviation(abbr, meaning, facultativoFlag = false) {
    try {
        const r = await fetch(`${API_URL}/api/add-abbreviation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ abbreviation: abbr, meaning: meaning, facultativo: facultativoFlag })
        });
        if (!r.ok) {
            const text = await r.text();
            throw new Error(`HTTP ${r.status}: ${text.slice(0,200)}`);
        }
        let data;
        try { data = await r.json(); } catch (e) { const t = await r.text(); throw new Error('Respuesta no es JSON: ' + (t && t.slice ? t.slice(0,200) : String(t))); }
        if (!data.success) throw new Error(data.error || 'Error adding');
    if (!abbreviations[abbr]) abbreviations[abbr] = [];
    abbreviations[abbr].push({ meaning: meaning, facultativo: facultativoFlag });
    return { success: true };
    } catch (e) {
        console.error('Error adding abbreviation', e);
        alert('Error al añadir abreviación: ' + e.message);
        return { success: false, error: e.message };
    }
}

// --- MODIFICACIÓN CLAVE AQUÍ ---
async function saveAsJSON() {
    // Obtener docid y text según el modo
    let docid, text;
    if (typeof APP_MODE !== 'undefined' && APP_MODE === 'review') {
        docid = (DOC_DATA && DOC_DATA.docid) ? DOC_DATA.docid : 'documento';
        text  = DOC_DATA ? DOC_DATA.text : '';
    } else {
        docid = (getElement('docId') && getElement('docId').value.trim()) || '';
        text  = getElement('inputText') ? getElement('inputText').value : '';
    }
    const abbreviationsOut = [];
    let searchIndex = 0;

    processedData.forEach(token => {
        // Obtenemos el texto del token (preferiblemente clean si es abbr, sino text)
        let tokenText = (token.clean || token.text || '').trim();

        // 1. SINCRONIZACIÓN: Si el token está vacío (era solo espacio/puntuación que trim borró),
        // forzamos al cursor a avanzar consumiendo espacios en el texto original.
        if (!tokenText) {
            while (searchIndex < text.length && /\s/.test(text[searchIndex])) {
                searchIndex++;
            }
            return; // Pasamos al siguiente token, pero ya movimos el cursor
        }

        // 2. BÚSQUEDA: Buscamos el token real
        const foundAt = text.indexOf(tokenText, searchIndex);
        
        if (foundAt !== -1) {
            const char_begin = foundAt;
            const char_end = foundAt + tokenText.length;
            
            // Avanzamos cursor
            searchIndex = char_end;

            // Guardamos solo si es válido
            if (token.type === 'abbreviation' && token.selected && token.selected !== 'IGNORAR') {
                abbreviationsOut.push({
                    char_begin: char_begin,
                    char_end: char_end,
                    text: tokenText,
                    meaning: token.selected
                });
            }
        }
    });

    const payload = { docid: docid, text: text, abbreviations: abbreviationsOut };

    try {
        const r = await fetch(`${API_URL}/api/save-json`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const result = await r.json();
        if (!result.success) throw new Error(result.error || 'Error al guardar');
        alert(`\u2705 ${result.message}`);
    } catch (e) {
        console.error('Error guardando JSON', e);
        // Fallback: descarga local
        alert(`\u26a0\ufe0f No se pudo guardar en el servidor: ${e.message}\nSe descargará localmente.`);
        const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${docid || 'documento'}_anotado.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Wire UI once
(() => {
    const procBtn = document.getElementById('processBtn');
    if (procBtn) procBtn.addEventListener('click', processText);
    const genBtn = document.getElementById('generateBtn');
    if (genBtn) genBtn.addEventListener('click', saveAsJSON);
    const copyBtn = document.getElementById('copyBtn');
    if (copyBtn) copyBtn.addEventListener('click', () => {
        const text = getElement('finalText') && getElement('finalText').textContent;
        if (!text) return;
        const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
    });

    // Close buttons: just close modal without auto-saving
    document.querySelectorAll('.close').forEach(b => b.addEventListener('click', () => {
        const m = getElement('modal'); if (m) m.style.display = 'none';
    }));

    window.addEventListener('click', (e) => { if (e.target.classList && e.target.classList.contains('modal')) e.target.style.display = 'none'; });
})();