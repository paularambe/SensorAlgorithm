#!/usr/bin/python
import cgi
import sqlite3
import os
import datetime

# Habilita la recepción de datos del formulario
form = cgi.FieldStorage()

# Obtiene el ID de los parámetros de la URL
id = form.getvalue("id")
url = form.getvalue("url")
remote_ip = os.environ.get("REMOTE_ADDR")

# Realiza una consulta   en la base de datos para verificar el ID
conn = sqlite3.connect('/var/www/html/data.db')  # Reemplaza con la ruta correcta
fecha_creacion_vencida = datetime.datetime.now() - datetime.timedelta(hours=12)

cursor = conn.cursor()
cursor.execute("UPDATE users SET session_id = NULL, IP = NULL WHERE expiration <= ?", (fecha_creacion_vencida,))
cursor.execute("SELECT * FROM users WHERE session_id = ? AND ip = ?", (id, remote_ip))
result = cursor.fetchone()
conn.commit()  # Guarda los cambios en la base de datos


query = """
SELECT COUNT(*) 
FROM sqlite_master 
WHERE type='table' AND name NOT LIKE 'sqlite_%';
"""
cursor.execute(query)
table_count = cursor.fetchone()[0]
nBoards= table_count-1

conn.commit()  # Guarda los cambios en la base de datos


conn.close()

# Configura el encabezado de respuesta HTTP
if result:
    # El ID se encontró en la base de datos, puedes continuar con el contenido de home.html
    print(f"Location: {url}&c=1\n")
else:
    # El ID no se encontró en la base de datos, redirige a error_login.html
    print("Location: error_login.html\n")
