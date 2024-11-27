import sqlite3

db_path = "/var/www/html/data.db"

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    query = """
    SELECT COUNT(*) 
    FROM sqlite_master 
    WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """
    cursor.execute(query)
    table_count = cursor.fetchone()[0]

print(f"Número de tablas en la base de datos: {table_count}")
