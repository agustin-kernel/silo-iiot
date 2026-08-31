### Sistema Predictivo de Monitoreo para Silos de Granos.

Es un sistema de  IIoT y Edge Computing diseñado para predecir y evitar pérdidas de granos por deterioro de humedad, hongos o combustión espontánea.

- **Propuesta de valor:** El sistema evoluciona el monitoreo reactivo tradicional hacia un modelo proactivo mediante análisis predictivo, permitiendo mitigar riesgos financieros y operativos antes de que ocurran.

###  Arquitectura de la Infraestructura 

- El ecosistema se ejecuta íntegramente sobre un servidor AlmaLinux mediante contenedores gestionados por el Motor de Docker.
    
- **Generación de Datos (Python):** Un script actúa como simulador de sensores físicos, inyectando continuamente marcas de tiempo, datos de temperatura, humedad y anomalías programadas (por ejemplo, un silo que eleva su temperatura de forma sostenida).
    
- **Ingesta y Enrutamiento:** Mosquitto funciona como el broker MQTT encargado de recibir los datos de los sensores. A su vez, Telegraf actúa como el puente que transfiere esta información desde el broker hacia el almacenamiento.
    
- **Almacenamiento (InfluxDB 2.7):** Se utiliza esta base de datos de series temporales (TSDB) por su extrema eficiencia para comprimir e indexar datos secuenciales asociados a marcas de tiempo.
    
- **Visualización (Grafana):** Un centro de control que se conecta a la base de datos para mostrar el estado de los silos mediante medidores y gráficos históricos en un tablero en tiempo real.
    

###  Capa de Inteligencia Artificial (Roadmap / Futuro)

- El proyecto contempla la integración de un motor de IA enfocado en la prevención predictiva de fallas.
    
- Se proyecta utilizar modelos de aprendizaje automático (como Regresión Lineal, ARIMA o algoritmos de detección de anomalías basados en la curva de CO₂/temperatura) para evaluar el historial térmico.
    
- El objetivo del modelo es calcular el ritmo térmico y disparar alertas tempranas horas antes de que la temperatura alcance un umbral crítico de combustión.
    

###  Instrucciones de Despliegue (How to use this repositoory)

Requisitos Previos Para replicar este entorno de monitoreo IIoT, tu infraestructura debe contar con: 

* **Motor de Contenedores:** Docker y Docker Compose activos en el servidor destino (testeado en AlmaLinux) para levantar InfluxDB, Telegraf, Mosquitto y Grafana. 
* **Nodo Edge:** Python 3 y `pip` instalados en el equipo inyector (testeado en EndeavourOS) para ejecutar el script simulador dentro de un entorno virtual. 
* **Red Segura:** Conexión VPN punto a punto (ej. Tailscale) entre el nodo edge y el servidor homelab para enviar telemetría MQTT sin exponer puertos al internet público. 
* **Hardware Mínimo del Servidor:** Al menos 3 GB de RAM y procesador básico (ej. AMD A6) para gestionar la compresión TSM en disco de la base de datos de series temporales.


 1. Clonar el repositorio:
  Descargá el código fuente a tu entorno local: 

  git clone [https://github.com/agustin-kernel/silo-iiot.git](https://github.com/agustin-kernel/silo-iiot.git) 
  cd silo-iiot

2. Levantar los contenedores:

docker compose up -d

3. Configurar el entorno virtual de Python

python3 -m venv venv
source venv/bin/activate
pip install paho-mqtt python-dotenv

4. Apuntar a la IP

Crear un archivo .env y escribir dentro:
BROKER_IP="TU_IP"

5. Inyectar Telemetría

Con el entorno activado y las credenciales listas, encendé la inyección de datos:

python simulador.py


6.  Configurar el Centro de Control

 Ingresá desde tu navegador a `http://<IP_DE_TU_SERVIDOR>:3000`.

 En el menú lateral izquierdo, navegá hacia **Dashboards** y seleccioná **Import**.

 Arrastrá el archivo `.json` ubicado en el directorio `grafana/dashboards/` para cargar los velocímetros térmicos en tiempo real.
