import os
import shutil

# Directorio a organizar (tu carpeta actual)
directorio_destino = '.'

# Diccionario de extensiones y carpetas de destino
extensiones = {
    '.py': 'Scripts_Python',
    '.sh': 'Scripts_Bash',
    '.pdf': 'Documentos_Prepa',
    '.txt': 'Apuntes',
    '.png': 'Capturas',
    '.jpg': 'Capturas',
}

for archivo in os.listdir(directorio_destino):
  nombre, ext = os.path.splitext(archivo)

  # Si la extensión está en nuestro diccionario, movemos el archivo
  if ext in extensiones:
    carpeta = extensiones[ext]

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta):
      os.makedirs(carpeta)

    # Evitar mover el script a sí mismo
    if archivo == 'organizador.py':
      continue

    # Mover el archivo
    shutil.move(archivo, os.path.join(carpeta, archivo))
    print(f'Movido: {archivo} -> {carpeta}/')

print('\n¡Organización completada con éxito!')

