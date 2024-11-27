#!/usr/bin/python
import sqlite3
import json
import cgi

# Conectarse a la base de datos
conn = sqlite3.connect('/var/www/html/data.db')  # Reemplaza con la ubicación de tu base de datos
cursor = conn.cursor()

# Obtener el id (session_id) desde los parámetros de la URL
form = cgi.FieldStorage()
session_id = form.getvalue("id")  # Obtiene el valor del parámetro "id"

# Consultar la base de datos para obtener el usuario correspondiente al id
cursor.execute("SELECT Nombre FROM users WHERE session_id=?", (session_id,))
user = cursor.fetchone()

# Cerrar la conexión a la base de datos
conn.close()

# Devolver el usuario como JSON
print("Content-Type: application/json")
print()  # Línea en blanco

if user:
    user_data = {'usuario': user[0]}
    print(json.dumps(user_data))  # Convierte los datos del usuario a JSON y lo imprime
else:
    error_data = {'error': 'Usuario no encontrado'}
    print(json.dumps(error_data))  # Devuelve un mensaje de error si el usuario no se encontró
