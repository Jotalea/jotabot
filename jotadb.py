import sqlite3

# Crear una conexión a la base de datos (o crearla si no existe)
conn = sqlite3.connect('log.db')
cursor = conn.cursor()

# Crear una tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS command_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        user TEXT,
        server TEXT,
        channel TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Función para agregar un registro a la base de datos
def add_log(command, user, timestamp):
    cursor.execute('INSERT INTO command_logs (command, user, timestamp) VALUES (?, ?, ?)', (command, user, timestamp))
    conn.commit()

# Función para obtener todos los registros de la base de datos
def get_logs():
    cursor.execute('SELECT * FROM command_logs')
    return cursor.fetchall()

# Función para borrar todos los registros de la base de datos
def delete_all_logs():
    cursor.execute('DELETE FROM command_logs')
    conn.commit()

# Uso de las funciones
add_log('!help', 'usuario1', '2023-12-12 12:00:00')
add_log('!info', 'usuario2', '2023-12-12 12:05:00')

logs = get_logs()
print(logs)

# Cerrar la conexión a la base de datos al finalizar
conn.close()