#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// MQTTブローカー情報
const char* mqtt_server = "your_mqtt_broker_address";
const int mqtt_port = 8883;
const char* mqtt_user = "your_mqtt_user";
const char* mqtt_password = "your_mqtt_password";
const char* topic = "your_topic";

// CA証明書
const char* ca_cert = R"EOF(
-----BEGIN CERTIFICATE-----
...  // ここにca.crtの内容をペースト
-----END CERTIFICATE-----
)EOF";

WiFiClientSecure espClient;
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
  espClient.setCACert(ca_cert);

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

  delay(10000);  // 10秒ごとにデータを送信
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
