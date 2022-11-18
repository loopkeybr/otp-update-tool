from airtable import Airtable
import json
import os
import sys
import re
import requests
import wget
import cloudinary
import cloudinary.uploader
import cloudinary.api

path = os.path.dirname(os.path.abspath(__file__))

# if __name__ == "__main__":
if sys.argv[1] == 'gateway':
    table = 'Gateway_mini'
elif sys.argv[1] == 'loopkey':
    table = 'Table 1'

lote = sys.argv[2]
version = sys.argv[4]

# print(lote)
airtable = Airtable(os.environ['AIRTABLE_BASE_ID1'], table, os.environ['AIRTABLE_API_KEY'])
records = airtable.search('Lote', lote, fields='Versao')
# records = airtable.get_all()
# print(records)



found = 0
for i in range(len(records)):
    if ('Versao' in records[i]['fields']) and records[i]['fields']['Versao'] == version:
        version = records[i]['fields']['Versao']
        id = records[i]['id']
        found=1
if (found != 1):
    sys.exit("Error: Version don't exits for this batch!")



# print(id)
    
records = airtable.search('Lote', lote)
# print(records)
for i in range(len(records)):
    if records[i]['id'] == id:
        if sys.argv[1] == 'gateway':
            if sys.argv[3] == 'esp_firmware':
                long_url = (records[i]['fields']['App'][0]['url'])
            elif sys.argv[3] == 'esp_bin':
                long_url = (records[i]['fields']['App(bin)'][0]['url'])
            elif sys.argv[3] == 'nrf_firmware':
                long_url = (records[i]['fields']['Aux App(tar)'][0]['url'])
            elif sys.argv[3] == 'nrf_boot':
                long_url = (records[i]['fields']['Aux Boot(tar)'][0]['url'])
        elif sys.argv[1] == 'loopkey':
            if sys.argv[3] == 'app':
                long_url = (records[i]['fields']['App(tar)'][0]['url'])
            elif sys.argv[3] == 'one_internal':
                long_url = (records[i]['fields']['Lk One Internal'][0]['url'])
            elif sys.argv[3] == 'combo':
                long_url = (records[i]['fields']['Combo'][0]['url'])                   
            elif sys.argv[3] == 'man_hex':
                long_url = (records[i]['fields']['Manufacture Hex'][0]['url'])  
            elif sys.argv[3] == 'firm_avr':
                long_url = (records[i]['fields']['Firmware Avr'][0]['url'])          
            elif sys.argv[3] == 'data_fix':
                long_url = (records[i]['fields']['Data Fix(tar)'][0]['url'])          


response = wget.download(long_url, "lk_gateway.tar")

cloudinary.config( 
  cloud_name = os.environ['CLOUDINARY_CLOUD_NAME'], 
  api_key = os.environ['CLOUDINARY_API_KEY'], 
  api_secret = os.environ['CLOUDINARY_API_SECRET'] 
)

up = cloudinary.uploader.upload("lk_gateway.tar", resource_type = 'raw', use_filename = True, overwrite = True)
os.remove("lk_gateway.tar")
print('https://' + up["url"][7:])
