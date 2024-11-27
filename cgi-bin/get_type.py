#!/usr/bin/python
import sqlite3
import json
import cgi

# Conectarse a la base de datos
conn = sqlite3.connect('/var/www/html/data.db')
cursor = conn.cursor()

# Obtener el tipo de video desde los parámetros de la URL
form = cgi.FieldStorage()
video_type = form.getvalue("type")  # Obtiene el valor del parámetro "type"
# Consultar la base de datos
cursor.execute("SELECT name, path FROM videos WHERE type=?", (video_type,))
videos = cursor.fetchall()

# Cerrar la conexión a la base de datos
conn.close()

# Devolver los datos como JSON
print("Content-Type: application/json")
print()  # Línea en blanco
print(json.dumps(videos))  # Convierte la lista de videos a JSON y lo imprime
