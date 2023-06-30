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
import ast

from src.utils import util_version
from src.backend import back_office_api
from src.backend import airtable_api
from src.utils import util_time


api_key=os.environ['AIRTABLE_API_KEY']

def extract_airtables_bases():
    # Recupera a representação em forma de string da variável de ambiente
    env_var = os.environ.get('AIRTABLE_BASE_IDS')

    # Remove os colchetes do início e do final da string
    env_var = env_var.strip('[]')

    # Divide a string em elementos individuais
    elementos = env_var.split(',')

    # Remove as aspas simples em cada elemento
    elementos = [elemento.strip("'") for elemento in elementos]

    return elementos

def extract_airtables_corps():
    # Recupera a representação em forma de string da variável de ambiente
    env_var = os.environ.get('CORP_BASES')

    # Remove os colchetes do início e do final da string
    env_var = env_var.strip('[]')

    # Divide a string em elementos individuais
    elementos = env_var.split(',')

    # Remove as aspas simples em cada elemento
    elementos = [elemento.strip("'") for elemento in elementos]

    return elementos

def extract_airtables_times():
    # Recupera a representação em forma de string da variável de ambiente
    env_var = os.environ.get('TIME_BASES')

    # Remove os colchetes do início e do final da string
    env_var = env_var.strip('[]')

    # Divide a string em elementos individuais
    elementos = env_var.split(',')

    # Remove as aspas simples em cada elemento
    elementos = [elemento.strip("'") for elemento in elementos]

    return elementos

def set_record_fields(index, fields):
    airtable.update(records[index]['id'], fields)
    for i in fields:
        records[index]['fields'][i] = fields[i]

def set_record_field(index, field, value):
    set_record_fields(index, {field:value})

def verify_door_exists_on_base(door_id, records):
    for i in range(len(records)):
        if 'Id' in records[i]['fields']:
            if(str(door_id) == records[i]['fields']['Id']):
                return records[i]['id']
    return False

bases=extract_airtables_bases()

corps=extract_airtables_corps()

times=extract_airtables_times()



for i_bases in range(len(bases)):
    path = os.path.dirname(os.path.abspath(__file__))

    door_database = Airtable(bases[i_bases], 'Doors', api_key)
    door_records = door_database.get_all()
    

    locks_corp=back_office_api.get_all_locks_from_corp(corps[i_bases])
    
    for i_records in range(len(locks_corp)):
        # print(locks_corp[i])

        # Filtrar portas que não são loopkey
        # print(locks_corp[i]['serialCode'])
        if locks_corp[i_records]['serialCode'][:3] != "LLK" and \
            locks_corp[i_records]['serialCode'][:3] != "TTL" and \
            locks_corp[i_records]['serialCode'][:2] != "TL":
            continue

        # print(locks_corp[i]['id'])
        # print(locks_corp[i]['serialCode'])
        # print(locks_corp[i]['name'])
        # print(locks_corp[i]['siteId'])
        # print(locks_corp[i]['siteName'])


        current_time=util_time.time_current()
        end_time=util_time.time_increment(current_time,int(times[i_bases]))
        
        try:
            otp=back_office_api.get_otp_password(locks_corp[i_records]['id'], current_time, end_time, 'Automatic Generation: ' + current_time)
        except:
            print("An exception has occurred!")
        
        passcode=''
        init=''
        end=''
        time_zone=''

        print(locks_corp[i_records]['id'])
        print(otp)

        if otp != False:
            if 'passcode' in otp:
                passcode=otp['passcode']
            if 'startDateTime' in otp:
                init=otp['startDateTime']
            if 'endDateTime' in otp:
                end=otp['endDateTime']
            if 'timezone' in otp:
                time_zone=otp['timezone']

        fields = {'Id':str(locks_corp[i_records]['id']),
                  'Serial':locks_corp[i_records]['serialCode'],
                  'Nome':locks_corp[i_records]['name'],
                  'Id do Prédio':str(locks_corp[i_records]['siteId']),
                  'Nome do Prédio':locks_corp[i_records]['siteName'],
                  'Senha':passcode,
                  'Início':init,
                  'Fim':end,
                  'TimeZone':time_zone}
        # print(fields)
        
        door_on_database = verify_door_exists_on_base(locks_corp[i_records]['id'], door_records)
        # print(door_on_database)
        if(door_on_database != False):
            door_database.update(door_on_database, fields)
        else:
            door_database.insert(fields)
