import os
import shutil

base_dir = os.path.dirname(os.path.dirname(__file__))
src = os.path.join(base_dir, 'abreviaciones.csv')
backup = src + '.bak_text'
tmp = src + '.tmp_text'

print(f"Procesando (texto): {src}")
shutil.copy2(src, backup)
print(f"Backup creado: {backup}")

with open(src, 'rb') as fin, open(tmp, 'wb') as fout:
    for raw in fin:
        # Mantener la codificación original: procesamos bytes y preservamos saltos
        line = raw.rstrip(b'\r\n')
        if not line:
            fout.write(b'\n')
            continue
        # Si ya termina con ,NO (case-sensitive) no añadimos
        if line.endswith(b',NO'):
            fout.write(line + b'\n')
        else:
            fout.write(line + b',NO\n')

shutil.move(tmp, src)
print('Operación completada: añadido ",NO" al final de las líneas que no lo tenían.')
