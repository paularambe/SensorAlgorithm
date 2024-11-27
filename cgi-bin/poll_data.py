#!/usr/bin/env python3

import sqlite3
import json
import cgi
import cgitb
import os

cgitb.enable()  # Muestra errores en el navegador para depuración

# Ruta a la base de datos
DB_PATH = "/var/www/html/data.db"

def get_tables():
    """
    Recupera todas las tablas de la base de datos.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener nombres de todas las tablas
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name != 'users';"
    cursor.execute(query)
    tables = [row[0] for row in cursor.fetchall()]

    conn.close()
    return tables

def get_table_data(table_name):
    """
    Recupera todos los datos de una tabla específica.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener los datos de la tabla
    query = f"SELECT * FROM '{table_name}';"
    cursor.execute(query)
    columns = [description[0] for description in cursor.description]  # Nombres de columnas
    rows = cursor.fetchall()

    conn.close()

    # Formatear datos como lista de diccionarios
    data = [dict(zip(columns, row)) for row in rows]
    return data

# Encabezado CGI
print("Content-Type: application/json\n")

# Recuperar todas las tablas y sus datos
tables = get_tables()
result = {}
tables=tables[1:]


for table in tables:
    result[table] = get_table_data(table)



# Convertir el resultado a JSON y enviarlo
print(json.dumps(result))

