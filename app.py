from airtable import Airtable
import json
import os
import sys
import re
import requests
import time
# from multiprocessing import Process
import multiprocessing
import subprocess
from subprocess import check_output

server = 'Server_update_1'
def is_gateway_online(id):
    url = "https://api.loopkey.com.br/bckf/getGateways?gatewayIds=" + id
    payload={}
    auth = os.environ['LK_BACKEND_AUTHORIZATION']
    headers = {
    'Authorization': auth,
    'Content-Type': 'application/x-www-form-urlencoded'
    }   
    response = requests.request("GET", url, headers=headers, data=payload)
    try:

        json_answer = json.loads(response.text)
        if 'gateways' in json_answer:
            return json_answer['gateways'][0]['online']
        else:
            return False
    except:
        return False

def get_gateway_version(serial):
    out = check_output(["scripts/version_get_gw", serial])
    return out.decode("utf-8").split("\n")
 
def update_gateway_ESP(gw_serial, version, server_name):
    print("Serial: " + gw_serial)
    print("Version: " + version)
    print("Server: " + server_name)
    for m in range(5):
        result = subprocess.run(['sh', 'scripts/send_ota.sh', gw_serial, version, server_name], stdout=subprocess.PIPE, text = True,)
        if 'Checksum verified. Flashing and rebooting now' in result.stdout:
            print("Atualizado!")
            return
    return

def update_gateway_NRF(gw_serial, version):
    # print("Serial: " + gw_serial)
    # print("Version: " + version)
    result = subprocess.run(['scripts/dfu_specific_nrf.sh', '-g', gw_serial, '-f', '-v', version], stdout=subprocess.PIPE, text = True,)
    return

path = os.path.dirname(os.path.abspath(__file__))

stable_version_complete_nrf = os.environ['STABLE_VERSION_NRF']
stable_version_complete_tlsr = os.environ['STABLE_VERSION_TLSR']
stable_version_nrf = [stable_version_complete_nrf.split(".stable",1)[0], stable_version_complete_nrf.split("stable_",2)[1]]
stable_version_tlsr = [stable_version_complete_tlsr.split(".stable",1)[0], stable_version_complete_tlsr.split("stable_",2)[1]]
print('Versão nrf: ' + ' '.join(stable_version_nrf))
print('Versão tlsr: ' + ' '.join(stable_version_tlsr))

airtable = Airtable(os.environ['AIRTABLE_BASE_ID2'], 'Table 1', os.environ['AIRTABLE_API_KEY'])
records = airtable.get_all()
for i in range(len(records)):
    # See if gateway is online
    if 'Update_select' in records[i]['fields']:
        if is_gateway_online(records[i]['fields']['Id']) == True:
            print("Online!")
            print(records[i]['fields']['Serial'])
            #Get version
            version = get_gateway_version(records[i]['fields']['Serial'])
            print(version)
            if(version[0] == ''):
                continue
            #Update gw list
            fields = {'ESP_version': version[0], 'NRF_version': version[1]}
            airtable.update(records[i]['id'], fields)
            #Compare with last stable version
            if 'LLKGAAE' in records[i]['fields']['Serial']:
                if(stable_version_tlsr[0] != version[0]):
                    #Update ESP firmware
                    print("ESP not updated!")
                    update_gateway_ESP(records[i]['fields']['Serial'], stable_version_complete_tlsr, server)
                    if 'Update retries ESP' in records[i]['fields']:
                        num_retries = int(records[i]['fields']['Update retries ESP']) + 1
                    else:
                        num_retries = 1
                    fields = {'Update retries ESP': num_retries}
                    airtable.update(records[i]['id'], fields)
                elif (stable_version_tlsr[1] != version[1]):
                    #Update TLSR/NRF firmware
                    print("TLSR not updated!")
                    update_gateway_NRF(records[i]['fields']['Serial'], stable_version_complete_tlsr)
                    if 'Update retries BLE' in records[i]['fields']:
                        num_retries = int(records[i]['fields']['Update retries BLE']) + 1
                    else:
                        num_retries = 1
                    fields = {'Update retries ESP': 0, 'Update retries BLE': num_retries}
                    airtable.update(records[i]['id'], fields)
                else:
                    fields = {'Update retries ESP': 0, 'Update retries BLE': 0}
                    airtable.update(records[i]['id'], fields)
            elif 'LLKGAAD' in records[i]['fields']['Serial']:
                if(stable_version_nrf[0] != version[0]):
                    #Update ESP firmware
                    print("ESP not updated!")
                    update_gateway_ESP(records[i]['fields']['Serial'], stable_version_complete_nrf, server)
                    if 'Update retries ESP' in records[i]['fields']:
                        num_retries = int(records[i]['fields']['Update retries ESP']) + 1
                    else:
                        num_retries = 1
                    fields = {'Update retries ESP': num_retries}
                    airtable.update(records[i]['id'], fields)
                elif (stable_version_nrf[1] != version[1]):
                    #Update TLSR/NRF firmware
                    print("NRF not updated!")
                    update_gateway_NRF(records[i]['fields']['Serial'], stable_version_complete_nrf)
                    if 'Update retries BLE' in records[i]['fields']:
                        num_retries = int(records[i]['fields']['Update retries BLE']) + 1
                    else:
                        num_retries = 1
                    fields = {'Update retries ESP': 0, 'Update retries BLE': num_retries}
                    airtable.update(records[i]['id'], fields)
                else:
                    fields = {'Update retries ESP': 0, 'Update retries BLE': 0}
                    airtable.update(records[i]['id'], fields)

