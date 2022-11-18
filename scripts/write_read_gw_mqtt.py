#!/usr/bin/python3

import paho.mqtt.client as mqtt
import os
import sys
import argparse
import datetime
import hashlib
import base64
import time
import ssl
import re
import queue


topic = ""
#inTopic = topic + "in"
inTopic = "cmd/gateway"
#outTopic = topic + "out"
outTopic = "msg/gateway"
send_topic = ""
name=""
passw=""
serial=""
msg_out=""

flag_timeout = 0

q = queue.Queue();

def regex(pattern, txt, group):
    group.clear()
    match = re.search(pattern, txt)
    if match:
        if match.groupdict():
            for k,v in match.groupdict().items():
                group[k] = v
        else:
            group.extend(match.groups())
        return True
    return False

def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))
    # print(inTopic)
    client.subscribe(inTopic)
    # print(msg_out)
    send_data(client)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic)
    print(msg.payload.decode('utf-8'))
    global flag_timeout
    flag_timeout=0


def send_data(client):

    client.publish(outTopic, msg_out)
    return

def main():
    global inTopic, outTopic, name, passw, send_topic
    parser = argparse.ArgumentParser()
    parser.add_argument("--mqtt_id", help="Mqtt Id");
    parser.add_argument("--broker", help="MQTT broker");
    parser.add_argument("--port", help="MQTT broker port");
    parser.add_argument("--user", help="MQTT broker user");
    parser.add_argument("--password", help="MQTT broker password");
    parser.add_argument("--ssl", help="MQTT broker SSL support");
    parser.add_argument("--topic", help="MQTT mesh topic base (default: {}".format(topic))
    parser.add_argument("--intopic", help="MQTT mesh in-topic (default: {}".format(inTopic))
    parser.add_argument("--outtopic", help="MQTT mesh out-topic (default: {}".format(outTopic))
    parser.add_argument("--ca_cert", help=("Specific CA certificate"))
    parser.add_argument("--cli_cert", help=("Specific Client certificate"))
    parser.add_argument("--cli_key", help=("Specific Client key"))
    parser.add_argument("--serial", help=("Serial"))
    parser.add_argument("--msg", help=("Msg"))
    parser.add_argument("--timeout", help=("Timeout"))
    args = parser.parse_args()
    
    if args.topic:
        inTopic = args.topic + "in"
        outTopic = args.topic + "out"
    if args.intopic:
        inTopic = args.intopic
    if args.outtopic:
        outTopic = args.outtopic

    if args.serial:
        serial = args.serial

    # print("Sending to topic: {}".format(send_topic))
    # print("Listening to topic: {}".format(outTopic))

    if not args.broker:
        args.broker = "127.0.0.1"
    if not args.port:
        args.port = 1883

    if args.user:
       name = args.user
    if args.password:
       passw = args.password

    client = mqtt.Client(client_id=args.mqtt_id)
    if args.ssl:
       client.tls_set(ca_certs=args.ca_cert, certfile=args.cli_cert, keyfile=args.cli_key, cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    if (args.user) or (args.password):
        client.username_pw_set(name,passw)

    if args.timeout:
        time_sleep = args.timeout
    else:
        time_sleep = 6

    global msg_out
    if args.msg:
        msg_out=args.msg


    # print("Client_id: " + args.mqtt_id)
    # print("Broker: " + args.broker)
    # print("Port: " + args.port)
    # print("Ssl: " + args.ssl)
    # # print("inTopic: " + args.intopic)
    # # print("outTopic: " + args.outtopic)
    # print("CA: " + args.ca_cert)
    # print("Cert: " + args.cli_cert)
    # print("Key: " + args.cli_key)

    # print("Msg: " + msg_out)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.broker, int(args.port), 60)
    client.loop_start()

    # send_data(client, args.msg)

    global flag_timeout
    flag_timeout=time_sleep*100

    while flag_timeout > 0:
        time.sleep(0.01) # wait
        flag_timeout -= 1

    client.loop_stop()
    client.disconnect()
main()
