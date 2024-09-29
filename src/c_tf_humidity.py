#!/usr/bin/python
# -*- coding: utf-8 -*-  

from c_emitter import c_emitter
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_humidity import Humidity
import logging as log

class c_tf_humidity(c_emitter):
    def __init__(self, device_id, entity="", label="", location=""):
        hMe = 0
        vCbPeriod = 5000
        hCollector = None
        super().__init__(device_id, entity, label, location)

    def setup(self, _IpConnection, _hCollector = None):
        self.hCollector = _hCollector
        self.hMe = Humidity(self.ID, _IpConnection)

    def cb_barometer(self, humidity):
        if self.hCollector == 0:
            log.info(humidity)
        else:
            self.hCollector.setValue(humidity)

    def startCallback(self):
        self.hMe.set_humidity_callback_period(self.vCbPeriod)
        self.hMe.register_callback(self.hMe.CALLBACK_HUMIDITY, self.cb_barometer)

    def get_humidity(self):
        humidity = self.hMe.get_humidity()
        return humidity

    def getValue(self):
        return self.get_humidity() / 10

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4223
    UID = "fQz" # Change to your UID

    ipcon = IPConnection() # Create IP connection
    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    hdl_barometer = c_barometer(UID, "%", "Luftfeuchte")
    hdl_barometer.setup(ipcon)
    
    if False:
        hdl_barometer.startCallback()
        input('Press key to exit\n') # Use input() in Python 3
    else:
        humidity = hdl_barometer.getValue()
        print(f"{hdl_barometer.Label}: {humidity} {hdl_barometer.Entity}")
    
    ipcon.disconnect()