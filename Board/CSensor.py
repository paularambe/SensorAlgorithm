from machine import ADC, Pin
import dht

class CSensor():
    dht_instance = None  # Clase compartida para evitar múltiples instancias del DHT11

    def __init__(self, nombre, pin):
        self.name = nombre
        self.pin = pin
        self.rawVal = 0

        if nombre == "Photoresistor":
            self.sensor = ADC(Pin(pin))
        elif nombre == "Movement":
            self.sensor = Pin(pin, Pin.IN)
        elif nombre == "Button":
            self.sensor = Pin(pin, Pin.IN, Pin.PULL_UP)
        elif nombre in ["Humidity", "Temperature"]:
            if CSensor.dht_instance is None:
                CSensor.dht_instance = dht.DHT11(Pin(pin))
            self.sensor = CSensor.dht_instance
        else:
            self.sensor = None

    def get_value(self):
        if self.name == "Photoresistor":
            self.sensor.atten(ADC.ATTN_11DB)
            val = self.sensor.read()
            self.rawVal = 1 if val >= 1200 else 0
        elif self.name == "Movement":
            self.rawVal = self.sensor.value()
        elif self.name == "Button":
            self.rawVal = 0 if self.sensor.value() == 1 else 1
        elif self.name == "Humidity":
            try:
                self.sensor.measure()
                self.rawVal = self.sensor.humidity()
            except Exception as e:
                print("Error leyendo Humidity:", e)
                self.rawVal = 0
        elif self.name == "Temperature":
            try:
                self.sensor.measure()
                self.rawVal = self.sensor.temperature()
            except Exception as e:
                print("Error leyendo Temperature:", e)
                self.rawVal = 0

        return self.rawVal

    def get_json(self):
        json_data = {
            "name": self.name,
            "pin": self.pin,
            "rawVal": self.rawVal
        }
        return json_data
