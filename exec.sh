#!/bin/bash

# create certificate files

mkdir -p dfu_gw_esp/cert/$MQTT_SERVER_NAME
mkdir -p app
echo $MQTT_CERTIFICATE_B64 | base64 --decode > /dfu_gw_esp/cert/$MQTT_SERVER_NAME/cert-certificate.pem.crt
echo $MQTT_PRIVATE_KEY_B64 | base64 --decode > /dfu_gw_esp/cert/$MQTT_SERVER_NAME/cert-private.pem.key
echo $MQTT_PUBLIC_KEY_B64 | base64 --decode > /dfu_gw_esp/cert/$MQTT_SERVER_NAME/cert-public.pem.key
echo $MQTT_ROOT_CA_B64 | base64 --decode > /dfu_gw_esp/cert/$MQTT_SERVER_NAME/root-CA.crt
export MQTT_CLIENT_ID=$MQTT_SERVER_NAME 

python3 -u app.py
exit
