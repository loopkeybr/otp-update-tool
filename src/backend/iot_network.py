import os
import logging
from paho.mqtt import client as mqtt_client

def connect_mqtt():

    # /dfu_gw_esp/cert/$MQTT_SERVER_NAME/cert-public.pem.key
    broker='a3apacvpactifn-ats.iot.sa-east-1.amazonaws.com'
    port=8883

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client_id = os.environ['MQTT_2_SERVER_NAME']
    current_path=os.path.dirname(os.path.realpath(__file__))
    cert_path=current_path+'/../../cert/'
    cert_certificate_path=cert_path+client_id+'/cert-certificate.pem.crt'
    cert_private_path=cert_path+client_id+'/cert-private.pem.key'
    cert_public_path=cert_path+client_id+'/cert-public.pem.key'
    cert_root_ca_path=cert_path+client_id+'/root-CA.crt'

    # print(cert_certificate_path)
    # print(cert_private_path)
    # print(cert_root_ca_path)

    client = mqtt_client.Client(client_id)
    client.tls_set(
        ca_certs=cert_root_ca_path,
        certfile=cert_certificate_path,
        keyfile=cert_private_path
    )
    client.on_connect = on_connect
    print('Chegou')
    client.connect(broker, port)
    # client.loop_forever()
    # client.loop()
    # loop()

    return client

