import logging
from src.backend import back_office_api

logging.basicConfig(level=logging.INFO)

def get_lock_version(serial):
    
    for i in range(3):
        logging.info(f'Try get version: {i}')
        version = back_office_api.get_lock_version(serial)
        if(version != False):
            return version

    return False

def get_better_gateway_by_device(serial):
    gateways=back_office_api.get_gateways_by_device(serial)

    if(gateways == False):
        return False
    
    # print(json_answer)
    biggestRssi = sorted(gateways, key=lambda k: k['rssi'], reverse=True)
    # print(biggestRssi[0])

    if not biggestRssi:
        return False
    if len(biggestRssi) == 0:
        return False

    return biggestRssi[0]

def send_to_dfu_mode(id):
    
    for i in range(3):
        logging.info(f'Try send dfu: {i}')
        result = back_office_api.send_to_dfu_mode(id)
        if(result != False):
            return result

    return False

def send_lock_update_firmware_by_websocket(serial, url):
    return back_office_api.send_lock_update_firmware_by_websocket(serial, url)