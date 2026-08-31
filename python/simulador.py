import time
import random
import json
import datetime
import paho.mqtt.publish as publish

import os
from dotenv import load_dotenv
import paho.mqtt.publish as publish

# Cargar la caja fuerte local
load_dotenv()

# Extraer la IP sin exponerla en el código
BROKER = os.getenv("BROKER_IP") 
PORT = 1883

# Estado inicial de los silos
silos = {
    1: {"temperatura": 22.5, "humedad": 13.2},
    2: {"temperatura": 21.5, "humedad": 12.7},
    3: {"temperatura": 19.3, "humedad": 14.5},
    4: {"temperatura": 24.0, "humedad": 13.0},
    5: {"temperatura": 27.1, "humedad": 15.3},
}

print(f"Iniciando simulador. Enviando datos a Mosquitto en {BROKER}...")

while True:
    marca_tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{marca_tiempo}] Generando nuevas lecturas:")
    
    for numero_silo, datos_silo in silos.items():
        # Simulamos las variaciones térmicas y de humedad
        datos_silo["temperatura"] += random.uniform(-0.2, 0.2)
        datos_silo["humedad"] += random.uniform(-0.2, 0.2)
        
        # Armamos el paquete de datos en formato JSON ligero
        payload_dict = {
            "temperatura": round(datos_silo["temperatura"], 2),
            "humedad": round(datos_silo["humedad"], 2)
        }
        payload_json = json.dumps(payload_dict)
        
        # El "buzón" específico para cada silo (Ej: silos/silo_1/sensores)
        topic_silo = f"silos/silo_{numero_silo}/sensores"
        
        # Enviamos el mensaje al broker MQTT
        try:
            publish.single(topic_silo, payload_json, hostname=BROKER, port=PORT)
            print(f"  ✅ Silo {numero_silo} enviado: {payload_json}")
        except Exception as e:
            print(f"  ❌ Error al conectar con el servidor: {e}")
            
    time.sleep(5)






