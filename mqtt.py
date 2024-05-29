import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("topic/translation") 
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode('utf-8')}' on topic '{message.topic}'")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: ", str(mid), str(granted_qos))

def setup_mqtt_subscriber():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    
    client.connect("broker.hivemq.com", 1883, 60)  # Connect to the MQTT broker
    client.loop_forever()  # Process network traffic and dispatch callbacks

if __name__ == "__main__":
    setup_mqtt_subscriber()
