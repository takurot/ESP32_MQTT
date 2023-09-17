#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "SSID";
const char* password = "password";

// MQTTブローカー情報
const char* mqtt_server = "192.168.0.100";
// const int mqtt_port = 8883; //for TLS
const int mqtt_port = 1883;
// const char* mqtt_user = "user";
// const char* mqtt_password = "pass";
const char* topic = "sensor_data";

// CA証明書
// const char* ca_cert = R"EOF(
// -----BEGIN CERTIFICATE-----
// ...  // ここにca.crtの内容をペースト
// -----END CERTIFICATE-----
// )EOF";

// WiFiClientSecure espClient;
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  
  // WiFi接続
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // TLS設定
  // espClient.setCACert(ca_cert);

  // MQTT設定
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  // 温度と電圧のサンプルデータ (実際にはセンサーからの読み取りなどを行う)
  float temperature = getTemperature();  // 例
  float voltage = getVoltage();       // 例

  // JSON形式でデータを生成
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["temperature"] = temperature;
  jsonDoc["voltage"] = voltage;
  char jsonData[128];
  serializeJson(jsonDoc, jsonData);

  // MQTTトピックにデータを送信
  client.publish(topic, jsonData);

  delay(3000);  // 10秒ごとにデータを送信
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

float getTemperature() {
  // ここで温度センサから温度を取得するコードを記述します
  // この例ではダミーデータを返します
  return 25.0;
}

float getVoltage() {
  // ここで電圧を取得するコードを記述します
  // この例ではダミーデータを返します
  return 3.3;
}
