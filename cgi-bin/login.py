#!/usr/bin/python3

import cgi
import sqlite3
import random
import os
import datetime
conn = sqlite3.connect("/var/www/html/data.db")
cursor = conn.cursor()

id = random.randrange(10**15, 10**16)

# Obtiene los datos del formulario
form = cgi.FieldStorage()
username = form.getvalue("username")
password = form.getvalue("password")

# Consulta la base de datos para verificar las credenciales
cursor.execute("SELECT * FROM users WHERE usuario = ? AND contraseña = ?", (username, password))
result1 = cursor.fetchone()
remote_ip = os.environ.get("REMOTE_ADDR")
now = datetime.datetime.now()
# Al inicio de las respuestas:

if result1:
    # Si las credenciales son correctas, actualiza session_id con el valor aleatorio id
    cursor.execute("UPDATE users SET session_id = ?, ip = ?, expiration = ? WHERE usuario = ?", (id, remote_ip, now, username))
    conn.commit()  # Guarda los cambios en la base de datos

    # Redirecciona al usuario a la página de inicio con el id aleatorio
    print("Status: 302 Found")
    print(f"Location: http://192.168.2.24/home.html?id={id}\n")
    print()
else:
    print("Location: http://192.168.2.24/error.html\n")
    print()

# Cierra la conexión a la base de datos
conn.close()
