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
from operator import itemgetter
import logging
import threading

from src.backend import backend_commands
from src.backend import iot_api
from src.utils import util_version

server = os.environ['MQTT_SERVER_NAME']

path = os.path.dirname(os.path.abspath(__file__))

versions_database = Airtable(os.environ['AIRTABLE_BASE_ID2'], 'Model Versions', os.environ['AIRTABLE_API_KEY'])
versions_records = versions_database.get_all()


airtable = Airtable(os.environ['AIRTABLE_BASE_ID2'], 'Locks Main', os.environ['AIRTABLE_API_KEY'])
records = airtable.get_all()

lock_versions_database = Airtable(os.environ['AIRTABLE_BASE_ID1'], 'Table 1', os.environ['AIRTABLE_API_KEY'])
lock_versions_records = lock_versions_database.get_all()

def set_state_complete():
    fields = {'LastGatewaySaw':'', 'GatewayType':'', 'Status':'Complete', 'Update_select':None}
    set_record_fields(i, fields)

def set_state_not_started():
    fields = {'LastGatewaySaw':'', 'GatewayType':'', 'Status':'Not Started'}
    set_record_fields(i, fields)


def set_record_fields(index, fields):
    airtable.update(records[index]['id'], fields)
    for i in fields:
        records[index]['fields'][i] = fields[i]

def set_record_field(index, field, value):
    set_record_fields(index, {field:value})

def get_try_count(index):
    tries = 0
    if 'Update retries Main' in records[i]['fields']:
        tries = records[i]['fields']['Update retries Main']
    return tries

def increase_try_count(index):
    tries = get_try_count(index) + 1
    set_record_field(index, 'Update retries Main', tries)

def verify_all_complete():
    for i in range(len(records)):
        if 'Update_select' in records[i]['fields']:
            return False
    return True



def event_callback(dfu_msg):
    print(dfu_msg.serial)
    print(dfu_msg.error)
    print(dfu_msg.progress)

    if(dfu_msg.error == 0 or dfu_msg.error == 50):
        print("Ready to update")
    else:
        return
    
    dfu_msg.error
    
    #Search for record that have the gateway to send dfu_jump command
    for i in range(len(records)):
        if 'Update_select' in records[i]['fields']:

            # print(records[i]['fields'])

            #Find the batch version to update
            batch = util_version.find_batch_version_update(versions_records, records[i]['fields']['Serial'])
            if(batch == False):
                print("Batch version not found!")
                continue

            #Verify if lock have a gateway point
            if 'LastGatewaySaw' not in records[i]['fields']:
                # print("LastGateway not setted!")
                continue
            if records[i]['fields']['LastGatewaySaw'] != dfu_msg.serial:
                # print("LastGateway different of event serial!")
                continue

            #Verify database version
            if 'Main_version' in records[i]['fields']:
                if not util_version.version_clean_compare_v1_fewer_v2(records[i]['fields']['Main_version'], batch['Version Main']):
                    # print("Database version not fewer!")
                    continue

            
            # if 'Progress' in records[i]['fields']:
            #     if records[i]['fields']['Progress'] != dfu_msg.progress:
            #         print("Saiu6")
            #         continue


            #Save progress
            fields = {'Progress':str(dfu_msg.progress)}
            set_record_fields(i, fields)

            # if(dfu_msg.progress == 100):
            #     print("Complete")
            #     set_state_complete() 
            #     return

            #Verify if Status is preparing
            if records[i]['fields']['Status'] != 'Preparing':
                # print("Status not Preparing")
                continue
            

            # version = backend_commands.get_lock_version(records[i]['fields']['Serial'])

            # print(version['version'])
            # print(batch['Version Main'])

            # if not version:
            #     continue

            #Verify if current version is below than update version
            # if not util_version.version_clean_compare_v1_fewer_v2(version['version'], batch['Version Main']):
            #     fields = {'Main_version': version['version'], 'Aux_version': version['internalVersion'], 'LastGatewaySaw':''}
            #     airtable.update(records[i]['id'], fields)
            #     return
            
            #Change Status to Updating
            print('Updating')
            fields = {'Status':'Updating'}
            set_record_fields(i, fields)
            # backend_commands.send_to_dfu_mode(records[i]['fields']['Id'])


def verify_gateway_in_use(lock_serial, lock_gateway):
    for i in range(len(records)):
        if 'Update_select' in records[i]['fields']:
            if 'LastGatewaySaw' not in records[i]['fields']:
                continue
            if records[i]['fields']['LastGatewaySaw'] == lock_gateway:
                if records[i]['fields']['Serial'] == lock_serial:
                    continue
                return True
    return False

def get_version_app_url(serial, version):
    for i in range(len(lock_versions_records)):
        if 'Enable' not in lock_versions_records[i]['fields']:
            continue

        if version not in lock_versions_records[i]['fields']['Versao']:
            # print(lock_versions_records[i])
            continue

        if lock_versions_records[i]['fields']['Lote'] not in serial:
            continue

        if not ('App' in lock_versions_records[i]['fields']) :
            return False
        
        if not lock_versions_records[i]['fields']['App'][0]:
            return False

        return lock_versions_records[i]['fields']['App'][0]['url']
    return False

event_listening = iot_api.EventsListening(event_callback)

# Variável de controle para parar a thread
thread_running = True

def thread_loop():
    print("Thread Start")
    
    while thread_running:
        event_listening.loop()

    print("Thread Finish")

x = threading.Thread(target=thread_loop)
x.start()

while True:
    
    versions_records = versions_database.get_all()
    records = airtable.get_all()
    lock_versions_records = lock_versions_database.get_all()

    # event_listening.connect()
    for i in range(len(records)):
        # See if gateway is online
        if 'Update_select' in records[i]['fields']:
            if not ('Id' in records[i]['fields']) :
                # print("Not selected to update!")
                set_state_not_started()
                continue

            #Find the batch version to update
            batch = util_version.find_batch_version_update(versions_records, records[i]['fields']['Serial'])
            if(batch == False):
                print("Batch version not found!")
                set_state_not_started()
                continue

            # print(batch)

            # print(records[i]['fields']['Serial'])

            #Verify database version
            if 'Main_version' in records[i]['fields']:
                print(records[i]['fields']['Main_version'])
                print(batch['Version Main'])


                if(util_version.version_clean_compare_v1_fewer_v2(records[i]['fields']['Main_version'], batch['Version Main']) == 0 ):
                    print("Version is equal update version!")
                    set_state_complete()
                    continue
                elif(util_version.version_clean_compare_v1_fewer_v2(records[i]['fields']['Main_version'], batch['Version Main']) != -1):
                    print("Version update not valid!")
                    continue
            else:
                set_state_not_started()

            version = backend_commands.get_lock_version(records[i]['fields']['Serial'])
            if version:
                print("Version Found")
                fields = {'Main_version': version['version'], 'Aux_version': version['internalVersion']}
                set_record_fields(i, fields)
                if(util_version.version_clean_compare_v1_fewer_v2(records[i]['fields']['Main_version'], batch['Version Main']) == 0):
                    set_state_complete()
                    continue

            #Get better gateway that is seeing
            gw=backend_commands.get_better_gateway_by_device(records[i]['fields']['Serial'])
            if(gw == False):
                print('Gateway not Found!')
                continue
            # if (gw['transport'] != "awsIot"):
            #     print("Gateway option not supported!")
            #     continue

            # print(gw)

            if records[i]['fields']['Status'] == 'Updating':
                
                if(get_try_count(i)%10 == 0):
                    set_state_not_started()
                    continue
                increase_try_count(i)
                print("Aqui1")
                if (gw['name'] != 'DfuTarg'):
                    print("Lock isn't on dfu mode!")
                    backend_commands.send_to_dfu_mode(records[i]['fields']['Id'])
                
                print(gw['name'])
                iot_api.update_loopkey_lock(records[i]['fields']['LastGatewaySaw'], records[i]['fields']['Serial'], batch['Version Main'])
                continue

            # print(version)

            print(records[i]['fields']['Serial'])
            # print(gw['gatewaySerial'])
            if verify_gateway_in_use(records[i]['fields']['Serial'], gw['gatewaySerial']):
                print("Gateway already in use!")
                continue

            #Mark gateway as in use
            fields = {'LastGatewaySaw':gw['gatewaySerial'], 'GatewayType':gw['transport']}
            set_record_fields(i, fields)

            if (gw['transport'] == "websocket"):
                increase_try_count(i)
                print("Updating websocket!")
                url = get_version_app_url(records[i]['fields']['Serial'], batch['Version Main'])
                if url == False:
                    print("Not valid url320 Millicores found!")
                    set_state_not_started()
                    continue

                print('Updating')
                fields = {'Status':'Updating'}
                set_record_fields(i, fields)
                response = backend_commands.send_lock_update_firmware_by_websocket(records[i]['fields']['Serial'], url)
                set_state_not_started()
                continue

            if (gw['transport'] != "awsIot"):
                print("Gateway option not supported!")
                continue

            print("Send command dfu to gateway")
            iot_api.update_loopkey_lock(gw['gatewaySerial'], records[i]['fields']['Serial'], batch['Version Main'])

            print("Preparing")
            fields = {'Status':'Preparing'}
            set_record_fields(i, fields)

            if 'Update retries Main' in records[i]['fields']:
                num_retries = int(records[i]['fields']['Update retries Main']) + 1
            else:
                num_retries = 1
            fields = {'Update retries Main': num_retries}
            set_record_fields(i, fields)

    if verify_all_complete() == True:
        break
        

    print("Sleeping")
    time.sleep(120)
    print("Wake")
    
print("Finish")
thread_running=False
# x.join()
exit()