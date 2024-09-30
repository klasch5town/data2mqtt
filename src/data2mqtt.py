#!/usr/bin/python
#

import paho.mqtt.client as mqtt
import configparser
import argparse
import os
import logging
from simple_log import log
from time import sleep
from c_1wireTemp import c_1wireTemp
from c_collector import c_collector

credentials_ini=os.path.join(os.environ['HOME'],".data2mqtt","credentials.ini")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    log.info(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def main(args):
    credentials = configparser.ConfigParser()
    try:
        with open(credentials_ini, 'r') as fh:
            credentials.read_file(fh)
    except:
        log.info(f'Could not read {credentials_ini}')
        credentials['MQTT']={'user':'','password':'','host_url':'localhost'}
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.username_pw_set(credentials['MQTT']['user'],credentials['MQTT']['password'])

    log.info(f"try to connect to {credentials['MQTT']['host_url']} with user: {credentials['MQTT']['user']}")
    try:
        mqttc.connect(credentials['MQTT']['host_url'], 1883, 60)
    except:
        print('Could not connect to mqtt broker - check your credentials file')
        exit()

    # read the sensor configuration
    config = configparser.ConfigParser()
    config.read(args.config)
    hdl_collector = c_collector()
    for item in config.sections():
        if item.find('sensor') >= 0:
            sensor_handle = None
            if config[item]['Type']=='1w_temp':
                # add one-wire sensor
                log.debug(f"found one-wire sensor: {config[item]['ID']}")
                sensor_handle = c_1wireTemp(
                    config[item]['ID'], 
                    config[item]['Entity'], 
                    config[item]['Name'], 
                    config[item]['Location'] 
                )
            if sensor_handle is None:
                log.debug("failed to add sensor")
                continue
            hdl_collector.addSource(sensor_handle)
            log.info(sensor_handle.info_string())

    mqttc.loop_start()

    print(hdl_collector.HandleList)
    print('-----')
    for item in hdl_collector.HandleList.keys():
        print(hdl_collector.HandleList[item].get_value())

    #print(hdl_collector.ValueList)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--config', default='sensor.ini',
                        help='configuration file')
    parser.add_argument('-v','--verbose', action='store_true',
                        help='show more output')
    parser.add_argument('-d','--debug', action='store_true',
                        help='show debug output')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    main(args)