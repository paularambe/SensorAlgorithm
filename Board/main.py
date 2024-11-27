
import json
import socket
import network
from CSensor import CSensor
from CESP32 import CESP32
import time








def poll_task():
    # Crear el socket una sola vez
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((thisBoard.IP, thisBoard.PORT))  # Enlazar el socket a la dirección de la ESP32
    ss.listen(1)
    print(f"Esperando conexiones en {thisBoard.IP}:{thisBoard.PORT}...")
    data_out={}
    print("Polling activo")

    while True:
        try:
            # Aceptar nueva conexión
            conn, addr = ss.accept()
            # print(f"Conexión aceptada desde: {addr}")

            while True:
                # Recibir mensaje del cliente
                data = conn.recv(1024).decode('utf-8')
                if not data:  # Si no hay datos, cierra la conexión
                    # print("El cliente ha cerrado la conexión.")
                    break

                if data == "Poll":
                    # print("Recibido 'Poll'. Enviando datos de sensores...")

                    # Enviar información de los sensores como JSON
                    for sensor in thisBoard.sensors:
                        # Agregar los datos del sensor al diccionario principal
                        print(f"Sensor: {sensor}")
                        data_out[sensor.name] = {
                            
                            "rawVal": sensor.get_value()
                        }
                        print(data_out)
                        
                    msgOut = json.dumps(data_out)
                    conn.send(msgOut.encode('utf-8'))  # Usar 'conn' para enviar
        except Exception as e:
            print(f"Error durante el polling: {e}")
        finally:
            conn.close()  # Cerrar la conexión con este cliente después de terminar



    





# Configuración WiFi (asegúrate de que la ESP32 esté conectada)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]

# Configuración del servidor remoto
remoteAdd = '192.168.2.24'  # Dirección IP de tu servidor
port = 138  # Puerto del servidor
# Configuración de la placa
name = "Kitchen"
sensors = [CSensor("Button", 0)]
# sensors.append(CSensor("Movement", 21))
thisBoard = CESP32(name, ip, port, remoteAdd,sensors)

# Clave para autenticación
key = "U3%ZhnN+S]m1H6iQFfg<jTfDDLs4R2"
while True:

    try:
        # Conectar al servidor
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((remoteAdd, port))

        print("Enviando clave al servidor...")
        s.send(key.encode('utf-8'))

        # Recibir ACK
        msgIn = s.recv(1024).decode('utf-8')
        if msgIn == f"ACK: {key}":
            print("Conexión establecida con éxito.")
            msgOut="ACK"
            s.send(msgOut.encode('utf-8'))
            msgIn = s.recv(1024).decode('utf-8')
            newPort=int(msgIn)
            thisBoard.PORT=newPort

            # Enviar datos JSON
            data_out = {
                "name": thisBoard.name,
                "IP": thisBoard.IP,
                "PORT": thisBoard.PORT,
                "remoteIP": thisBoard.remoteADD,
                "sensors": [sensor.get_json() for sensor in sensors],
            }

            mensaje = json.dumps(data_out)
            s.send(mensaje.encode('utf-8'))
            print("Datos enviados:", mensaje)
            print("Cerrando puerto...")
            s.close()

            poll_task()

        else:
            print("Clave incorrecta. No se pudo conectar.")
    except Exception as e:
        pass
    finally:
        pass
