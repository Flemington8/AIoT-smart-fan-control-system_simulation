import json
import time
from queue import Queue

import paho.mqtt.client as mqtt


class HQYJMqttClient:
    def __init__(self, broker_ip: str, broker_port: int, client_id: str):
        self.mqtt_queue = Queue(255)
        self.is_connected = False
        self.client = mqtt.Client(client_id)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.result_code = 100
        try:
            self.client.connect(broker_ip, broker_port, 3)
        except Exception as e:
            print(e)

    def on_message(self, message):
        msg = json.loads(message.payload.decode())
        self.mqtt_queue.put(msg)

    def on_connect(self, client, userdata, flags, result_code):
        print("connected & return result_code:", result_code)
        self.result_code = result_code


hqyj_mqtt_clt = HQYJMqttClient('mqtt.yyzlab.com.cn', 1883, '11111')
hqyj_mqtt_clt.client.loop_start()  # open a new thread to handle the network loop
time.sleep(3)
if hqyj_mqtt_clt.result_code == 0:
    print('MQTT connected')
    hqyj_mqtt_clt.client.subscribe('AIOTSIM2APP', qos = 0)

    while True:
        mqtt_data = hqyj_mqtt_clt.mqtt_queue.get()
        if ('tem' in mqtt_data) and ('id' in mqtt_data) and (mqtt_data['id'] == 0):
            if (float(mqtt_data["tem"])) > 8:
                hqyj_mqtt_clt.client.publish('APP2AIOTSIM',
                                             payload = json.dumps(({"fan": True, "id": 0}), ensure_ascii = False))
                print('温度太高，打开风扇', float(mqtt_data["tem"]))
            if (float(mqtt_data["tem"])) < 8:
                hqyj_mqtt_clt.client.publish('APP2AIOTSIM',
                                             payload = json.dumps(({"fan": False, "id": 0}), ensure_ascii = False))
                print('温度太低，关闭风扇', float(mqtt_data["tem"]))
