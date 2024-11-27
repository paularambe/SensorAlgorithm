#!/usr/bin/python

import cgi
import sqlite3
import os

# Habilita el manejo de errores en CGI
# Establece el tipo de contenido para HTML
print("Content-type: text/html\n")

# Obtiene los datos del formulario
form = cgi.FieldStorage()
username = form.getvalue("username")
password = form.getvalue("password")
email = form.getvalue("email")
address = form.getvalue("address")
firstName = form.getvalue("firstName")
secondName = form.getvalue("secondName")
phone = form.getvalue("phone")

# Obtén el archivo de imagen del formulario
profile_image = form['profileImage']

# Verifica si se proporcionó un archivo de imagen
if profile_image.filename:
    # Establece la ruta donde se guardará la imagen
    upload_dir = "/var/www/html/prf_pic/"

    # Genera un nombre de archivo único
    file_name = username

    # Guarda la imagen en la ruta especificada
    with open(os.path.join(upload_dir, file_name), 'wb') as f:
        f.write(profile_image.file.read())

    # Conecta a la base de datos SQLite
    conn = sqlite3.connect("/var/www/html/data.db")  # Reemplaza con la ruta correcta
    cursor = conn.cursor()

    # Inserta los datos en la base de datos
    try:
        cursor.execute("INSERT INTO users (Nombre, Apellido, usuario, rol, contraseña, email, phone, profile_pic, direccion) VALUES (?, ?, ?, 'user', ?, ?, ?, ?, ?)", (firstName, secondName, username, password, email, phone, file_name, address))
        conn.commit()
        conn.close()
        print("<html><body>")
        print("<script>window.location.href = 'login.html';</script>")
        print("</body></html>")

    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        print("<html><body>")
        print(e)
        print("Error en el registro. <a href='error.html'>Volver</a>")
        print("</body></html>")
else:
    print("<html><body>")
    print("Por favor, selecciona una imagen. <a href='register.html'>Volver</a>")
    print("</body></html>")
