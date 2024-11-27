#!/usr/bin/python

import cgi
import sqlite3
import random
import os
import datetime
conn = sqlite3.connect("/var/www/html/data.db")
cursor = conn.cursor()
form = cgi.FieldStorage()
id = form.getvalue("id")





# Si las credenciales son correctas, actualiza session_id con el valor aleatorio id
cursor.execute("UPDATE users SET session_id = NULL, ip = NULL, expiration = NULL WHERE session_id = ?", (id,))
conn.commit()  # Guarda los cambios en la base de datos

# Redirecciona al usuario a la página de inicio con el id aleatorio
print("Status: 302 Found")
print(f"Location: login.html?id={id}\n")
print()
conn.close()
