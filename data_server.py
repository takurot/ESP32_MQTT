import sqlite3
import json
import paho.mqtt.client as mqtt

# SQLiteデータベースの設定
DB_NAME = 'sensors.db'

# MQTTの設定
BROKER_ADDRESS = 'localhost'
TOPIC = 'sensor_data'

# SQLiteデータベースの初期化
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY,
            time LONG,
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

    elapsed_time = data['time']
    voltage = data['voltage']
    temperature = data['temperature']

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (time, voltage, temperature) VALUES (?, ?, ?)", (elapsed_time, voltage, temperature))
    conn.commit()
    conn.close()

    print(f"Saved Data - elapsed_time: {elapsed_time}, Voltage: {voltage}, Temperature: {temperature}")

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
