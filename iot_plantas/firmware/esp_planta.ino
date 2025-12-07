#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// --- WIFI ---
const char* ssid = "Wifi";
const char* password = "password";

// --- MQTT ---
const char* mqtt_server = "192.168.0.100";  // IP de la Raspberry Pi
const char* TOPIC = "plantas/name";        

// --- SENSOR ---
#define DHTPIN D1
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// --- ALUMNO ---
const String NOMBRE = "name";
const String MATRICULA = "id";

WiFiClient espClient;
PubSubClient client(espClient);

// ==========================================================
void setup_wifi() {
  delay(100);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}
// ==========================================================
void reconnect() {
  while (!client.connected()) {
    client.connect("ESP_name");      
    delay(500);
  }
}
// ==========================================================
void setup() {
  Serial.begin(115200);
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}
// ==========================================================
void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Error leyendo sensor");
    delay(5000);
    return;
  }

  // Crear JSON
  String payload = "{";
  payload += "\"nombre\":\"" + NOMBRE + "\",";
  payload += "\"matricula\":\"" + MATRICULA + "\",";
  payload += "\"temperatura\":" + String(t, 2) + ",";
  payload += "\"humedad\":" + String(h, 2);
  payload += "}";

  client.publish(TOPIC, payload.c_str());

  Serial.println("Enviado MQTT: " + payload);

  delay(3000); // cada 3 segundos
}


