import requests
import os
import logging
import json

def send_raw_command(id, command, cmdSource):
    lk_server_host = os.environ['LK_BACKEND_HOST']
    url = lk_server_host + "/bckf/sendRawDoorCommand"

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
    lk_server_host = os.environ['LK_BACKEND_HOST']
    url = lk_server_host + "/bckf/updateDeviceFirmware"

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

    lk_server_host = os.environ['LK_BACKEND_HOST']
    url = lk_server_host + "/bckf/getDeviceFirmwareVersion?serial=" + serial

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
    lk_server_host = os.environ['LK_BACKEND_HOST']
    url = lk_server_host + "/bckf/getGatewaysByDevice?serialCode=" + serial
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
    lk_server_host = os.environ['LK_BACKEND_HOST']
    url = lk_server_host + "/bckf/getGateways?gatewayIds=" + id
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
    lk_server_host = os.environ['LK_BACKEND_HOST']
    url = lk_server_host + "/bckf/corp/doors/status?corpId=" + id
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
    lk_server_host = os.environ['LK_BACKEND_HOST']
    url = lk_server_host + "/bckf/door/otp?doorId=" + str(doorId) + "&startDateTime=" + startDateTime + \
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
