#!/bin/bash

set -e
lote="$(echo $1 | head -c 7)"
# echo $lote
link_air=`python3 scripts/get_link.py gateway $lote esp_firmware $2`
# echo $link_air

cd app/
wget $link_air -O package.zip -q
unzip -o -qq package
# if [ $lote = 'LLKGAAD' ] 
# then
#     filename='lk_gateway_firmware_ESP8266_0251_BOARD_MINI.bin'
# else
#     filename='lk_gateway_firmware_ESP8266_0251_BOARD_MINI_TLSR8251.bin'
# fi
filename=`unzip -qq -u -l package | grep -oE '[^ ]+$'`
# echo $filename
cd ..

./scripts/send_ota.py --bin app/$filename --id $1 --broker "a3apacvpactifn-ats.iot.sa-east-1.amazonaws.com" --port 8883 --ssl SSL --ca_cert cert/root-CA.crt --cli_cert cert/*-certificate.pem.crt --cli_key cert/*-private.pem.key --mqtt_id $MQTT_SERVER_NAME
