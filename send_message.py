import time
import requests
import gc

gc.collect()


def url_encode(text):
    replacements = {
        " ": "%20",
        "!": "%21",
        '"': "%22",
        "#": "%23",
        "$": "%24",
        "%": "%25",
        "&": "%26",
        "'": "%27",
        "(": "%28",
        ")": "%29",
        "*": "%2A",
        "+": "%2B",
        ",": "%2C",
        "-": "%2D",
        ".": "%2E",
        "/": "%2F",
        ":": "%3A",
        ";": "%3B",
        "<": "%3C",
        "=": "%3D",
        ">": "%3E",
        "?": "%3F",
        "@": "%40",
        "[": "%5B",
        "\\": "%5C",
        "]": "%5D",
        "^": "%5E",
        "_": "%5F",
        "`": "%60",
        "{": "%7B",
        "|": "%7C",
        "}": "%7D",
        "~": "%7E"
    }
    return "".join(replacements.get(c, c) for c in text)


gc.threshold(10000)
def send_message(mes):
    mes_encoded = url_encode(mes)  # Codifica caracteres especiales en el mensaje
    mes=mes_encoded
    api='3930802'
    phone='+34676535751'
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={mes_encoded}&apikey={api}"
    
    try:
        start=time.ticks_ms()
        response=requests.get(url)
        if response.status_code==200:
            print("Exito!")
        else:
            print(f"Error en la respuesta: {response.status_code}")
            print("Contenido de la respuesta:")
            print(response.text)  # Muestra el contenido de la respuesta
    except Exception as e:
        print(f"Error: {e}")
    gc.collect()
    time.sleep(1)