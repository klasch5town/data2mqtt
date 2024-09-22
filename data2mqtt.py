#!/usr/bin/python
#

from pi1wire import Pi1Wire, Resolution
from time import sleep
import paho.mqtt.client as mqtt
import configparser
import paho.mqtt.client as mqtt
import argparse
import os
import logging as log

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

    # read sensors into dictionary
    p1w_sensor_list = Pi1Wire().find_all_sensors()

    # read the sensor configuration
    config = configparser.ConfigParser()
    config.read(args.config)
    sensor_dict=dict()
    for item in config.sections():
        if item.find('sensor') >= 0:
            if config[item]['Type']=='11':
                key_value_dict=dict()
                sensor_id = config[item]['ID']
                log.info(sensor_id)
                for key in config[item].keys():
                    key_value_dict[key]=config[item][key]
                    log.info(f"\t{key}={key_value_dict[key]}")
                sensor_dict[sensor_id]=key_value_dict
                log.info(f"{sensor_id} = {key_value_dict['name']}@{key_value_dict['location']}")
    log.info(sensor_dict)

    mqttc.loop_start()

    while True:
        for device in p1w_sensor_list:
            value = device.get_temperature()
            if device.mac_address in sensor_dict.keys():
                device_info=sensor_dict[device.mac_address]
            else:
                device_info={'name':device.mac_address,'location':'default'}
            log.info(f"{device_info['name']}[{device.mac_address}] = {value:.3f}")
            mqttc.publish(f"{device_info['location']}/sensor/temperature/{device_info['name']}", value)
        sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--config', default='sensor.ini',
                        help='configuration file')
    parser.add_argument('-v','--verbose', action='store_true',
                        help='show more output')

    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(level=log.INFO)

    main(args)