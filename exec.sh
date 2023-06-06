#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

# create certificate files for dfu_gw_esp lib

mkdir -p dfu_gw_esp/cert/$MQTT_SERVER_NAME

echo $MQTT_CERTIFICATE_B64 | base64 --decode > $SCRIPTPATH/dfu_gw_esp/cert/$MQTT_SERVER_NAME/cert-certificate.pem.crt
echo $MQTT_PRIVATE_KEY_B64 | base64 --decode > $SCRIPTPATH/dfu_gw_esp/cert/$MQTT_SERVER_NAME/cert-private.pem.key
# echo $MQTT_PUBLIC_KEY_B64 | base64 --decode > $SCRIPTPATH/dfu_gw_esp/cert/$MQTT_SERVER_NAME/cert-public.pem.key
echo $MQTT_ROOT_CA_B64 | base64 --decode > $SCRIPTPATH/dfu_gw_esp/cert/$MQTT_SERVER_NAME/root-CA.crt
export MQTT_CLIENT_ID=$MQTT_SERVER_NAME 

#create certificates to monitor mqqt events

mkdir -p cert/$MQTT_2_SERVER_NAME
echo $MQTT_2_CERTIFICATE_B64 | base64 --decode > $SCRIPTPATH/cert/$MQTT_2_SERVER_NAME/cert-certificate.pem.crt
echo $MQTT_2_PRIVATE_KEY_B64 | base64 --decode > $SCRIPTPATH/cert/$MQTT_2_SERVER_NAME/cert-private.pem.key
# echo $MQTT_2_PUBLIC_KEY_B64 | base64 --decode > $SCRIPTPATH/cert/$MQTT_2_SERVER_NAME/cert-public.pem.key
echo $MQTT_2_ROOT_CA_B64 | base64 --decode > $SCRIPTPATH/cert/$MQTT_2_SERVER_NAME/root-CA.crt
export MQTT_2_CLIENT_ID=$MQTT_2_SERVER_NAME 

python3 -u app.py
exit
