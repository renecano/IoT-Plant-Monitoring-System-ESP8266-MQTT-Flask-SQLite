# 🌱 IoT Plant Monitoring (ESP8266 + MQTT + Flask + SQLite)

This project is a complete **IoT-based plant monitoring system**.  
An **ESP8266** microcontroller with a **DHT11** sensor measures temperature and humidity and sends the data via **MQTT** to a **Raspberry Pi** (or any local server).  
The data is stored in an **SQLite** database and displayed in a **web dashboard** built with **Flask + Bootstrap + Chart.js**.


## 🏗️ System Architecture

### 1. **ESP8266 + DHT11**
- Connects to WiFi  
- Reads temperature and humidity  
- Sends JSON-formatted data to MQTT topics, such as:
  - `plantas/rene`
  - `plantas/alan`
  - `plantas/alessandro`

### 2. **MQTT Server + Python Receiver**
- Python script `iot_receiver.py` subscribes to `plantas/#`
- Every incoming message is stored in `plantas.db` (table: `lecturas`)

### 3. **Web Server (Flask)**
- `app.py` runs a Flask server
- Serves the dashboard at `/` (`index.html`)
- Exposes `/data` endpoint returning JSON for graphs

### 4. **Web Dashboard**
- Built with HTML + Bootstrap  
- Charts made with Chart.js  
- Status cards display alerts (e.g., *normal*, *high temperature*, *low humidity*, etc.)

---

## 🧰 Technologies Used

### **Hardware**
- ESP8266  
- DHT11 Sensor  
- (Optional) Raspberry Pi as MQTT + Flask host  

### **Software / Backend**
- C++ (Arduino ESP8266 firmware)
- Python 3  
- Flask  
- paho-mqtt  
- SQLite  

### **Frontend**
- HTML5  
- CSS3 + Bootstrap  
- Chart.js  

---

## 📁 Project Structure

```text
iot-plantas/
├─ firmware/
│  └─ esp_planta.ino          # ESP8266 code (WiFi + MQTT + DHT11)
├─ server/
│  ├─ iot_receiver.py         # MQTT client that stores readings into SQLite
│  ├─ app.py                  # Flask server hosting the dashboard
│  └─ templates/
│     └─ index.html           # Dashboard UI (Bootstrap + Chart.js)
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## 🔧 ASCII Architecture Diagram

```text
      ┌────────────────┐
      │   ESP8266      │
      │ + DHT11 Sensor │
      └───────┬────────┘
              │ JSON MQTT
              ▼
      ┌──────────────────┐
      │   MQTT Broker     │
      │ (Mosquitto/RPi)   │
      └────────┬──────────┘
               │ subscribes plantas/#
               ▼
      ┌──────────────────┐
      │  Python Receiver  │
      │  iot_receiver.py  │
      └────────┬──────────┘
               │ writes to SQLite
               ▼
      ┌──────────────────┐
      │   SQLite DB       │
      │   plantas.db      │
      └────────┬──────────┘
               │ serves data
               ▼
      ┌──────────────────┐
      │   Flask Server    │
      │     app.py        │
      └────────┬──────────┘
               │ /data + /
               ▼
      ┌──────────────────┐
      │ Web Dashboard     │
      │ HTML + Bootstrap  │
      │    Chart.js       │
      └──────────────────┘
```

---

