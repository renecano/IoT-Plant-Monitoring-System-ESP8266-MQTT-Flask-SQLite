import json
import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime

DB = "plantas.db"

# ======================================
#  CREAR BASE DE DATOS (si no existe)
# ======================================
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS lecturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    planta TEXT,
    nombre TEXT,
    matricula TEXT,
    temperatura REAL,
    humedad REAL
)
""")
conn.commit()
conn.close()


# ======================================
#  FUNCIÓN CUANDO LLEGA UN MENSAJE MQTT
# ======================================
def on_message(client, userdata, msg):
    try:
        # Convertir JSON recibido
        payload = json.loads(msg.payload.decode())

        # Identificar la planta por el topic
        planta = msg.topic.split("/")[-1]  # rene, alan, alessandro

        # Timestamp
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar en base de datos
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""
            INSERT INTO lecturas (fecha, planta, nombre, matricula, temperatura, humedad) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fecha, planta, payload["nombre"], payload["matricula"], payload["temperatura"], payload["humedad"]))
        
        conn.commit()
        conn.close()

        print("Guardado:", fecha, planta, payload)

    except Exception as e:
        print("Error:", e)


# ======================================
#     CONFIGURACIÓN DEL CLIENTE MQTT
# ======================================
client = mqtt.Client()
client.on_message = on_message

client.connect("192.168.0.100", 1883, 60)
client.subscribe("plantas/#")

print("Escuchando MQTT en plantas/# ...")

client.loop_forever()
