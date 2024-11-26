# boot.py -- run on boot-up
import network
import time# Crear una interfaz de red Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # Activa la interfaz

# Configura los datos de la red Wi-Fi
ssid = "ASUS"
pswd = "JAIMEBEGITEK"
mac = wlan.config('mac')

# Convierte la MAC a formato legible (hexadecimal)
mac_address = ':'.join(['{:02x}'.format(b) for b in mac])
print(f"Dirección MAC: {mac_address}")
# Crea una instancia de la interfaz WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # Activa la interfaz Wi-Fi

# Conecta a la red Wi-Fi
print(f"C a {ssid}...")
wlan.connect(ssid, pswd)

# Espera hasta que se establezca la conexión con un temporizador
timeout = 30  # Tiempo máximo de espera en segundos
start_time = time.time()

while not wlan.isconnected() and (time.time() - start_time) < timeout:
    print(f"Conectando a {ssid}...")
    time.sleep(1)

# Verifica si se conectó exitosamente
if wlan.isconnected():
    print("----Conectado a internet!----")
    print("Detalles de la conexion:", wlan.ifconfig())
else:
    print("----No se pudo conectar a la red. Verifique las credenciales y la señal.----")
