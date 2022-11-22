#!/bin/bash

# create certificate files

mkdir -p cert
mkdir -p app
echo $MQTT_CERTIFICATE_B64 | base64 --decode > /cert/cert-certificate.pem.crt
echo $MQTT_PRIVATE_KEY_B64 | base64 --decode > /cert/cert-private.pem.key
echo $MQTT_PUBLIC_KEY_B64 | base64 --decode > /cert/cert-public.pem.key
echo $MQTT_ROOT_CA_B64 | base64 --decode > /cert/root-CA.crt

python3 -u app.py
exit
