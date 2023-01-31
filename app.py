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

server = os.environ['MQTT_SERVER_NAME']

def versionCompare(v1, v2):
     
    # This will split both the versions by '.'
    arr1 = v1.split(".")
    arr2 = v2.split(".")
    n = len(arr1)
    m = len(arr2)
     
    # converts to integer from string
    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]
  
    # compares which list is bigger and fills
    # smaller list with zero (for unequal delimeters)
    if n>m:
      for i in range(m, n):
         arr2.append(0)
    elif m>n:
      for i in range(n, m):
         arr1.append(0)
     
    # returns 1 if version 1 is bigger and -1 if
    # version 2 is bigger and 0 if equal
    for i in range(len(arr1)):
      if arr1[i]>arr2[i]:
         return 1
      elif arr2[i]>arr1[i]:
         return -1
    return 0
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

def get_gateway_version_once(serial):
    out = check_output(["dfu_gw_esp/scripts/version_get_gw", serial])
    return out.decode("utf-8").split("\n")

def get_gateway_version(serial):
    
    for i in range(3):
        print(f'Try get version: {i}')
        version = get_gateway_version_once(serial)
        if(version[0] != ''):
            return version

    return version
 
def update_gateway_ESP(gw_serial, version, server_name, current_version):
    print("Serial: " + gw_serial)
    print("Version: " + version)
    print("Server: " + server_name)

    # print("Aqui", current_version[0])
    ans = versionCompare(current_version[0], '2.5.1')
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

def update_gateway_NRF(gw_serial, version):
    # print("Serial: " + gw_serial)
    # print("Version: " + version)
    result = subprocess.run(['dfu_gw_esp/scripts/dfu_nrf.sh', '-t', gw_serial, '-g', '-f', '-v', version], stdout=subprocess.PIPE, text = True,)
    print(result.stdout.splitlines()[-1])
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
            try:
                version_db = records[i]['fields']['ESP_version']
                print(f"Version: {version_db}")
            except KeyError:
                version_db = ''
                print("Db not setted")

            if(version[0] == ''):
                print("Continua")
                continue
            #Update gw list
            fields = {'ESP_version': version[0], 'NRF_version': version[1]}
            airtable.update(records[i]['id'], fields)
            #Compare with last stable version
            if 'LLKGAAE' in records[i]['fields']['Serial']:
                if(stable_version_tlsr[0] != version[0]):
                    #Update ESP firmware
                    print("ESP not updated!")
                    update_gateway_ESP(records[i]['fields']['Serial'], stable_version_complete_tlsr, server, version)
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
                    update_gateway_ESP(records[i]['fields']['Serial'], stable_version_complete_nrf, server, version)
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

