import os

# Ruta del archivo original
filename = "/home/pablo/Documents/actacolne.txt"

# Tamaño de cada archivo (en este caso, 2000 caracteres)
chunk_size = 2000

# Abre el archivo original y obtiene su contenido
with open(filename, 'r') as file:
    content = file.read()

# Dividir el contenido en chunks de tamaño chunk_size
chunks = [content[i:i+chunk_size] for i in range(0, len(content), 
chunk_size)]

# Asigna un número único a cada archivo
for i, chunk in enumerate(chunks):
    # Crea un nuevo archivo con el nombre base + número del chunk
    new_filename = f"{os.path.splitext(filename)[0]}_{i+1}.txt"
    
    # Escribe el contenido del chunk en el nuevo archivo
    with open(new_filename, 'w') as file:
        file.write(chunk)
