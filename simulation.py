import json
import time
import base64
import requests
from queue import Queue
import paho.mqtt.client as mqtt


class Simulation_MQTT_Client:
    def __init__(self, broker_ip: str, broker_port: int, client_id: str):
        self.mqtt_queue = Queue(255)
        self.is_connected = False
        self.client = mqtt.Client(client_id)
        self.client.on_message = self.on_message  # cover the default on_message
        self.client.on_connect = self.on_connect  # cover the default on_connect
        self.result_code = 100
        try:
            self.client.connect(broker_ip, broker_port, 3)
        except Exception as e:
            print(e)

    def on_message(self, client, userdata, message):
        msg = json.loads(message.payload.decode())
        self.mqtt_queue.put(msg)

    def on_connect(self, client, userdata, flags, result_code):  # 0 means success； if client call client.on_connect(),
        print("connected & return result_code:", result_code)
        self.result_code = result_code


simulation_mqtt_client = Simulation_MQTT_Client('mqtt.yyzlab.com.cn', 1883, '11111')
simulation_mqtt_client.client.loop_start()  # open a new thread to handle the network loop
time.sleep(3)
if simulation_mqtt_client.result_code == 0:
    print('MQTT connected')
    simulation_mqtt_client.client.subscribe('AIOTSIM2APP', qos = 0)  # subscribe the topic

    while True:
        mqtt_data = simulation_mqtt_client.mqtt_queue.get()
        # if ('tem' in mqtt_data) and ('id' in mqtt_data) and (mqtt_data['id'] == 0):
        #     if (float(mqtt_data["tem"])) > 8:
        #         simulation_mqtt_client.client.publish('APP2AIOTSIM',
        #                                               payload = json.dumps(({"fan": True, "id": 0}),
        #                                                                    ensure_ascii = False))
        #         print('温度太高，打开风扇', float(mqtt_data["tem"]))
        #     if (float(mqtt_data["tem"])) < 8:
        #         simulation_mqtt_client.client.publish('APP2AIOTSIM',
        #                                               payload = json.dumps(({"fan": False, "id": 0}),
        #                                                                    ensure_ascii = False))
        #         print('温度太低，关闭风扇', float(mqtt_data["tem"]))
def capture_temperature():
    return float(mqtt_data["tem"])
def control_fan(ON):
    if ON:
        simulation_mqtt_client.client.publish('APP2AIOTSIM',
                                              payload = json.dumps(({"fan": True, "id": 0}),
                                                                   ensure_ascii = False))
        print('Turn on the fan ', float(mqtt_data["tem"]))
    else:
        simulation_mqtt_client.client.publish('APP2AIOTSIM',
                                              payload = json.dumps(({"fan": False, "id": 0}),
                                                                   ensure_ascii = False))
        print('Turn off the fan ', float(mqtt_data["tem"]))
