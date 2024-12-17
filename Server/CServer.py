import time
import json
import socket
import threading
import sqlite3
import sys
from flask import Flask, Response

# Asegúrate de que las clases CSensor y CESP32 estén bien definidas en tu entorno
from CSensor import CSensor
from CESP32 import CESP32

class CServer:
    def __init__(self):
        self.isBoardCon = 0
        self.db_path = "/var/www/html/data.db"
        self.conBoards = []
        self.usedPorts = []

        # Inicia los hilos
        self.threadConnect = threading.Thread(target=self.connect_task)
        self.threadConnect.start()

        self.threadPoll = threading.Thread(target=self.poll_task)
        self.threadPoll.start()

        self.threadCam = threading.Thread(target=self.cam_task)
        self.threadCam.start()

    def find_available_port(self, start=1024, end=65535):
        """Encuentra un puerto disponible dentro del rango especificado."""
        for port in range(start, end + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("", port))
                    if port not in self.usedPorts:
                        self.usedPorts.append(port)
                        return port
                except OSError:
                    continue
        return None

    def cam_task(self):
        """Configura un servidor Flask para transmitir el flujo MJPEG."""
        print("Initializing cam task...")

        app = Flask(__name__)

        def mjpeg_stream():
            HOST = '0.0.0.0'  # Cambiar si es necesario
            PORT = 5000
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((HOST, PORT))
            server_socket.listen(1)
            print(f"Esperando conexión en {HOST}:{PORT}")
            conn, addr = server_socket.accept()
            print(f"Conexión establecida desde: {addr}")

            data = b""
            while True:
                try:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    start = data.find(b'\xff\xd8')  # SOI (Start of Image)
                    end = data.find(b'\xff\xd9')    # EOI (End of Image)

                    if start != -1 and end != -1:
                        jpg = data[start:end+2]
                        data = data[end+2:]
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')
                except Exception as e:
                    print(f"Error: {e}")
                    break

        @app.route('/video_feed')
        def video_feed():
            return Response(mjpeg_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

        app.run(host='0.0.0.0', port=8080)

    def poll_task(self):
        """Consulta periódica a las placas conectadas."""
        time.sleep(1)
        print("Entering polling server")
        while True:
            if self.isBoardCon:
                for board in self.conBoards:
                    try:
                        pollSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        pollSock.settimeout(5)
                        pollSock.connect((board.IP, board.PORT))

                        msgOut = "Poll"
                        pollSock.send(msgOut.encode('utf-8'))

                        msgIn = pollSock.recv(1024).decode('utf-8')
                        data = json.loads(msgIn)

                        for sensor in board.sensors:
                            sensor.rawVal = data[sensor.name]['rawVal']

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
                                update_query = f"""
                                UPDATE {table_name}
                                SET "{sensor.name}" = ?
                                WHERE id = 1
                                """
                                cursor.execute(update_query, (sensor.rawVal,))
                                conn.commit()
                    except Exception as e:
                        if board.isBoardCon:
                            board.isBoardCon = 0
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
        """Gestiona las conexiones entrantes."""
        host = '0.0.0.0'
        port = 138

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(10)
            print(f"Servidor escuchando en {host}:{port}")
        except Exception as e:
            print(f"Error creando el socket del servidor: {e}")
            return

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión establecida desde: {addr}")

            try:
                key = "U3%ZhnN+S]m1H6iQFfg<jTfDDLs4R2"
                data = conn.recv(1024).decode('utf-8')
                if data == key:
                    conn.send(f"ACK: {key}".encode('utf-8'))

                    data = conn.recv(1024).decode('utf-8')
                    if data == "ACK":
                        newPort = self.find_available_port()
                        conn.send(str(newPort).encode('utf-8'))

                    data = conn.recv(1024).decode('utf-8')
                    received_data = json.loads(data)

                    name = received_data['name']
                    ip = received_data['IP']
                    port = received_data['PORT']
                    remoteADD = received_data['remoteIP']
                    sensors = received_data['sensors']

                    sensorList = [CSensor(sensor['name'], sensor['pin']) for sensor in sensors]

                    new_board = CESP32(name, ip, port, remoteADD, sensorList)
                    new_board.isBoardCon = 1
                    self.isBoardCon = 1
                    self.conBoards.append(new_board)
                    self.create_table_for_esp(name, sensorList)
                else:
                    print("Clave incorrecta. Conexión rechazada.")
            except Exception as e:
                print(f"Error procesando la conexión: {e}")
            finally:
                conn.close()

    def create_table_for_esp(self, table_name, sensorList):
        """Crea una tabla SQLite para la placa."""
        try:
            with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                cursor = conn.cursor()
                table_name = f'"{table_name}"'

                sensor_columns = ", ".join([f'"{sensor.name}" REAL' for sensor in sensorList])

                drop_query = f"DROP TABLE IF EXISTS {table_name}"
                cursor.execute(drop_query)

                create_table_query = f"""
                CREATE TABLE {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    IP TEXT,
                    port INTEGER,
                    {sensor_columns}
                )
                """
                cursor.execute(create_table_query)

                conn.commit()
        except Exception as e:
            print(f"Error creando la tabla '{table_name}': {e}")
