import cv2
import requests
import numpy as np

ESP32_CAM_IP = "http://192.168.2.223"
CAPTURE_URL = f"{ESP32_CAM_IP}/capture"

def main():
    try:
        while True:
            # Solicita una imagen a la ESP32-CAM
            response = requests.get(CAPTURE_URL, stream=True)
            if response.status_code == 200:
                # Convierte los datos de la imagen en un array de numpy
                img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                # Decodifica la imagen como una imagen de OpenCV
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                
                # Muestra la imagen en una ventana
                if img is not None:
                    cv2.imshow("Video ESP32-CAM", img)
                else:
                    print("Error al decodificar la imagen")
                
                # Presiona 'q' para salir
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print(f"Error al capturar imagen: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la ESP32-CAM: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
