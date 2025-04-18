import time
from machine import Pin
from umqtt.simple import MQTTClient
import network

# Wi-Fi credentials
WIFI_SSID = "SSID"
WIFI_PASSWORD = "PSWD"

# MQTT settings
MQTT_BROKER = "192.168.0.115"  # Replace with your computer's local IP
MQTT_TOPIC = "esp32/intruder_alert"
CLIENT_ID = "esp32_client"
MQTT_USER = "myuser"  # Replace with your Mosquitto username
MQTT_PASSWORD = "123"  # Replace with your Mosquitto password

# Pin setup
PIR_PIN = 15 # GPIO pin connected to PIR sensor
pir = Pin(PIR_PIN, Pin.IN)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Wi-Fi connected:", wlan.ifconfig())

# MQTT callback (for subscriptions, if needed)
def on_message(topic, msg):
    print(f"Received message: {msg} on topic {topic}")

# Connect to MQTT broker
def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.set_callback(on_message)
    client.connect()
    print("Connected to MQTT broker")
    return client

# Main logic
def main():
    connect_wifi()
    mqtt_client = connect_mqtt()

    while True:
        if pir.value() == 1:  # Motion detected
            print("Intruder detected!")
            mqtt_client.publish(MQTT_TOPIC, "Intruder Detected!")
            time.sleep(2)  # Debounce delay to avoid multiple triggers
        time.sleep(0.1)  # Small delay to reduce CPU usage

if __name__ == "__main__":
    main()