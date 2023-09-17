import sqlite3
import json
import paho.mqtt.client as mqtt

# SQLiteデータベースの設定
DB_NAME = 'sensors.db'

# MQTTの設定
BROKER_ADDRESS = 'your_mqtt_broker_address'
TOPIC = 'your_topic'

# SQLiteデータベースの初期化
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY,
            voltage FLOAT,
            temperature FLOAT
        )
    ''')
    conn.commit()
    conn.close()

# MQTTのコールバック
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)

    voltage = data['voltage']
    temperature = data['temperature']

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (voltage, temperature) VALUES (?, ?)", (voltage, temperature))
    conn.commit()
    conn.close()

    print(f"Saved Data - Voltage: {voltage}, Temperature: {temperature}")

def main():
    init_db()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, 1883, 60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()

if __name__ == '__main__':
    main()
