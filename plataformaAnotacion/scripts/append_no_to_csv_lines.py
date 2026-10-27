import csv
import os
import shutil

base_dir = os.path.dirname(os.path.dirname(__file__))
src = os.path.join(base_dir, 'abreviaciones.csv')
backup = src + '.bak_append_no'
tmp = src + '.tmp_append_no'

print(f"Procesando archivo: {src}")
shutil.copy2(src, backup)
print(f"Backup creado: {backup}")

with open(src, 'r', encoding='utf-8-sig', newline='') as fin:
    reader = csv.reader(fin)
    rows = list(reader)

with open(tmp, 'w', encoding='utf-8', newline='') as fout:
    writer = csv.writer(fout)
    # Si el primer row tiene encabezado y ya contiene 'Facultativo', conservamos
    header = rows[0] if rows else []
    if header and len(header) >= 3 and header[0].lower().strip() == 'abreviacion':
        # Reescribir encabezado asegurando 'Facultativo'
        writer.writerow(['Abreviacion', 'Definicion', 'Facultativo'])
        start = 1
    else:
        # No reconocido encabezado: escribimos un encabezado estándar
        writer.writerow(['Abreviacion', 'Definicion', 'Facultativo'])
        start = 0

    for row in rows[start:]:
        if not row:
            continue
        if len(row) >= 3:
            # Si ya hay un valor en la columna 3, no lo sobrescribimos pero
            # si está vacío lo ponemos a 'NO'
            if row[2].strip() == '':
                row[2] = 'NO'
            writer.writerow(row[:3])
        elif len(row) == 2:
            writer.writerow([row[0].strip(), row[1].strip(), 'NO'])
        elif len(row) == 1:
            writer.writerow([row[0].strip(), '', 'NO'])
        else:
            # Fila misteriosa
            pass

shutil.move(tmp, src)
print('Operación completada: todas las líneas ahora tienen la columna \'Facultativo\' (NO si estaba vacía).')
