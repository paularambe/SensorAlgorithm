import time
import json
import socket
import threading
import sqlite3

import sys

from CSensor import CSensor
from CESP32 import CESP32





class CServer:
    def __init__(self):
        self.isBoardCon = 0
        self.db_path="/var/www/html/data.db"
        self.conBoards = []
        self.threadConnect = threading.Thread(target=self.connect_task)
        self.threadConnect.start()
        self.usedPorts = []

        self.threadPoll = threading.Thread(target=self.poll_task)
        self.threadPoll.start()

    def find_available_port(self,start=1024, end=65535):

        for port in range(start, end + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('', port))  # Prueba enlazar el puerto
                    if not (port in self.usedPorts):
                        self.usedPorts.append(port)
                        return port
                except OSError:
                    continue  # Si el puerto está en uso, prueba el siguiente
        
        return None  # Si no hay puertos disponibles


    def poll_task(self):
        time.sleep(1)
        print("Entering polling server")
        while True:
            if self.isBoardCon:
                # print("Polling activo...")
                for board in self.conBoards:
                    try:
                        # print(f"Conectando a la board {board.IP}:{board.PORT}...")

                        # Crear un nuevo socket para cada conexión
                        pollSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        pollSock.settimeout(5)
                        pollSock.connect((board.IP, board.PORT))

                        # print("Socket conectado!")

                        # Enviar mensaje de polling
                        msgOut = "Poll"
                        pollSock.send(msgOut.encode('utf-8'))
                        # print("Mensaje enviado. Esperando respuesta...")

                        # Recibir respuesta de la board
                        msgIn = pollSock.recv(1024).decode('utf-8')
                        # print(f"Respuesta desde {board.IP}:{board.PORT} -> {msgIn}")
                        data = json.loads(msgIn)
                        print(data)
                        for sensor in board.sensors:
                            sensor.rawVal = data[sensor.name]['rawVal']
                        print("")
                        with sqlite3.connect(self.db_path, check_same_thread=False) as conn:

                            cursor = conn.cursor()
                            table_name = f'"{board.name}"'

                            update = f"""
                                UPDATE {table_name}
                                SET IP = ?, port = ?
                                WHERE id = 1
                                """ 
                            
                            cursor.execute(update, (board.IP, board.PORT))


                            
                            for sensor in board.sensors:
                                


                                # Query para actualizar si no está vacía
                                update_query = f"""
                                UPDATE {table_name}
                                SET "{sensor.name}" = ?
                                WHERE id = 1
                                """

                                

                                # Ejecuta el UPDATE si ya hay registros
                                print(sensor.name)
                                print(sensor.rawVal)
                                cursor.execute(update_query, (sensor.rawVal,))

                                conn.commit()
                    except Exception as e:
                        if board.isBoardCon:
                            board.isBoardCon=0
                            drop_query = f"DROP TABLE {board.name}"
                            with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                                cursor = conn.cursor()
                                cursor.execute(drop_query)
                                conn.commit()
                            
                            self.conBoards = [boar for boar in self.conBoards if boar.name != board.name]


                        print(f"Error durante el polling con {board.IP}:{board.PORT}: {e}")
                    finally:
                        pollSock.close()





    def connect_task(self):
        host = '0.0.0.0'
        port = 138  # Puerto de escucha del servidor

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(10)  # Escuchar hasta 5 conexiones simultáneas
            print(f"Servidor escuchando en {host}:{port}")
        except Exception as e:
            print(f"Error creando el socket del servidor: {e}")
            return

        while True:
            print("Esperando conexiones...")
            conn, addr = server_socket.accept()
            print(f"Conexión establecida desde: {addr}")

            try:
                # Recibir la clave
                key = "U3%ZhnN+S]m1H6iQFfg<jTfDDLs4R2"
                data = conn.recv(1024).decode('utf-8')
                if data == key:
                    print("Clave correcta. Enviando ACK...")
                    conn.send(f"ACK: {key}".encode('utf-8'))

                    # Recibir datos JSON
                    data = conn.recv(1024).decode('utf-8')
                    if data=="ACK":
                        newPort=self.find_available_port()
                        msgOut=str(newPort)
                        conn.send(msgOut.encode('utf-8'))


                    data = conn.recv(1024).decode('utf-8')
                    
                    received_data = json.loads(data)
                    print("Datos recibidos:", received_data)

                    # Procesar los datos
                    name = received_data['name']
                    ip=received_data['IP']
                    port=received_data['PORT']
                    remoteADD=received_data['remoteIP']
                    sensors = received_data['sensors']
                    print(sensors)
                    sensorList=[]
                    for sensor in sensors:
                        sensorList.append(CSensor(sensor['name'], sensor['pin']))
                    
                    
                    for s in sensorList:
                        print(f"Name: {name}, Ip: {ip}Sensors: {s.name}")

                    # Crear una nueva instancia de la placa

                    new_board = CESP32(name, ip, port, remoteADD, sensorList)
                    new_board.isBoardCon = 1
                    self.isBoardCon=1
                    self.conBoards.append(new_board)
                    self.create_table_for_esp(name,sensorList)
                    print(self.conBoards)
                    conn.close()

                else:
                    print("Clave incorrecta. Conexión rechazada.")
            except Exception as e:
                print(f"Error procesando la conexión: {e}")
            finally:
                conn.close()

                
    def create_table_for_esp(self, table_name, sensorList):
        """
        Crea una tabla en la base de datos SQLite con el nombre especificado.
        """
        db_path = "/var/www/html/data.db"
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            table_name = f'"{table_name}"'

            # Crear una lista de columnas dinámicamente basadas en sensorList
            sensor_columns = ", ".join([f'"{sensor.name}" REAL' for sensor in sensorList])

            # Ejecutar el DROP TABLE en una consulta separada
            drop_query = f"DROP TABLE IF EXISTS {table_name}"
            cursor.execute(drop_query)

            # Construir y ejecutar la sentencia CREATE TABLE
            create_table_query = f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                IP TEXT,
                port INTEGER,
                {sensor_columns}
            )
            """
            cursor.execute(create_table_query)

            # Insertar valores iniciales si la tabla está vacía
            for sensor in sensorList:
                insert_query = f"""
                INSERT INTO {table_name} (IP, port, "{sensor.name}")
                SELECT ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM {table_name}
                )
                """
                cursor.execute(insert_query, (0, 0, 0))

            conn.commit()
            print(f"Tabla '{table_name}' creada correctamente en la base de datos.")
        except Exception as e:
            print(f"Error creando la tabla '{table_name}': {e}")
        finally:
            conn.close()

    