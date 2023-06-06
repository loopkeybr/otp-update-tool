import logging
import subprocess
import os
import time
import json
from src.backend import iot_network


global clientHandler

def update_loopkey_lock(gw_serial, lock_serial, version):
    print("Serial: " + gw_serial)
    print("Version: " + version)

    current_path=os.path.dirname(os.path.realpath(__file__))
    dfu_gw_esp_path=current_path+'/../../'

    result = subprocess.run([dfu_gw_esp_path + 'dfu_gw_esp/scripts/dfu_nrf.sh', '-t', gw_serial, '-l', '-v', version, '-s', 
                             lock_serial], stdout=subprocess.PIPE, text = True,)
    # print(result.stdout.splitlines()[-1])
    return

def update_gateway_NRF(gw_serial, version):
    # print("Serial: " + gw_serial)
    # print("Version: " + version)
    result = subprocess.run(['dfu_gw_esp/scripts/dfu_nrf.sh', '-t', gw_serial, '-g', '-f', '-v', version], stdout=subprocess.PIPE, text = True,)
    print(result.stdout.splitlines()[-1])
    return

def update_gateway_ESP(gw_serial, version, server_name, current_version):
    print("Serial: " + gw_serial)
    print("Version: " + version)
    print("Server: " + server_name)

    # print("Aqui", current_version[0])
    ans = versionCompare(current_version[0], '2.6.6')
    if ans >= 0:
        print("Esp update new method")
        result = subprocess.run(['dfu_gw_esp/scripts/dfu_nrf.sh', '-t', gw_serial, '-e', '-v', version], stdout=subprocess.PIPE, text = True,)
        print(result.stdout.splitlines()[-1])
    else:
        print("Esp update old method")
        for m in range(5):
            result = subprocess.run(['sh', 'dfu_gw_esp/scripts/send_ota.sh', gw_serial, version, server_name], stdout=subprocess.PIPE, text = True,)
            print(result.stdout.splitlines()[-1])
            if 'Checksum verified. Flashing and rebooting now' in result.stdout:
                return
        print("Error Updating: Too many attempts")
        return


    


class EventsListening:
    class DfuAns:
        def __init__(self, serial, error, progress):
            self.serial = serial
            self.error = error
            self.progress = progress
    
    def connect(self):
        self.client_handler = iot_network.connect_mqtt()

    def __init__(self, callback):
        self.client_handler = iot_network.connect_mqtt()
        self.client_handler.loop(timeout=2)
        self.client_handler.subscribe('backend/g/+/targetDfu')
        self.client_handler.on_message = self.on_message
        self.callback = callback

    def loop(self):
        self.client_handler.loop()

    def on_message(self,client, userdata, msg):
        payload_str=msg.payload.decode()

        if not '_topic' in payload_str:
            return
        if not 'error' in payload_str:
            return
        if not 'progress' in payload_str:
            return

        payload_json=json.loads(payload_str)
        topic=payload_json['_topic']
        error=payload_json['error']
        progress=payload_json['progress']
        serial = topic.split('/')[3]

        # print(f"Received `{payload_str}` from `{msg.topic}` topic")
        
        dfu_msg = self.DfuAns(serial, error, progress)

        # print(serial)
        # print(error)
        # print(progress)
        # print(f"Received `{payload}` from `{msg.topic}` topic")

        self.callback(dfu_msg)


    