import requests
import os
import logging
import json

def send_raw_command(id, command, cmdSource):
    url = "https://api.loopkey.com.br/bckf/sendRawDoorCommand"

    payload='doorId=' + id + '&command=' + command + '&commandSource=' + cmdSource
    auth = os.environ['LK_BACKEND_AUTHORIZATION']
    headers = {
    'Authorization': auth,
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return True

def send_to_dfu_mode(id):
    return send_raw_command(id,'SkRGVREAAAD2Pw==','ADMIN')


def send_lock_update_firmware_by_websocket(serial, firmwareUrl):
    url = "https://api.loopkey.com.br/bckf/updateDeviceFirmware"

    payload='serial=' + serial + '&firmwareUrl=' + firmwareUrl
    auth = os.environ['LK_BACKEND_AUTHORIZATION']
    headers = {
    'Authorization': auth,
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return True



def get_lock_version(serial):
    import requests

    url = "https://api.loopkey.com.br/bckf/getDeviceFirmwareVersion?serial=" + serial

    payload={}
    auth = os.environ['LK_BACKEND_AUTHORIZATION']
    headers = {
    'Authorization': auth
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if not 'successful' in response.text:
        return False
    
    json_ans = json.loads(response.text)
    
    if(json_ans['successful'] == False):
        return False
    
    return json_ans

def get_gateways_by_device(serial):
    url = "https://api.loopkey.com.br/bckf/getGatewaysByDevice?serialCode=" + serial
    payload={}
    auth = os.environ['LK_BACKEND_AUTHORIZATION']
    print(auth)
    headers = {
    'Authorization': auth,
    'Content-Type': 'application/x-www-form-urlencoded'
    }   
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    try:
        
        json_answer = json.loads(response.text)
        return json_answer
    except:
        return False

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


def get_all_locks_from_corp(id):
    url = "https://api-hml.loopkey.com.br/bckf/corp/doors/status?corpId=" + id
    payload={}
    auth = os.environ['LK_BACKEND_AUTHORIZATION']
    headers = {
    'Authorization': auth,
    'Content-Type': 'application/x-www-form-urlencoded'
    }   
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        json_answer = json.loads(response.text)
        # print(json_answer)
        return json_answer['doorStatus']
    except:
        return False
    
def get_otp_password(doorId, startDateTime, endDateTime, description):
    url = "https://api-hml.loopkey.com.br/bckf/door/otp?doorId=" + str(doorId) + "&startDateTime=" + startDateTime + \
          "&endDateTime=" + endDateTime + "&description=" + description
    payload={}
    auth = os.environ['LK_BACKEND_AUTHORIZATION']
    headers = {
    'Authorization': auth,
    'Content-Type': 'application/x-www-form-urlencoded'
    }   
    response = requests.request("GET", url, headers=headers, data=payload)
    try:

        json_answer = json.loads(response.text)
        return json_answer
    except:
        return False