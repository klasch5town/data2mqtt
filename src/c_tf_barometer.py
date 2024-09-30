#!/usr/bin/python
# -*- coding: utf-8 -*-  

from c_emitter import c_emitter
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_barometer import Barometer
from simple_log import log

class c_tf_barometer(c_emitter):
    def __init__(self, device_id, entity="", label="", location=""):
        hMe = 0
        vCbPeriod = 5000
        hCollector = None
        super().__init__(device_id, entity, label, location)

    def setup(self, _IpConnection, _hCollector = None):
        self.hCollector = _hCollector
        self.hMe = Barometer(self.ID, _IpConnection)

    def cb_barometer(self, air_pressure):
        if self.hCollector == 0:
            log.info(air_pressure)
        else:
            self.hCollector.setValue(air_pressure)

    def startCallback(self):
        self.hMe.set_air_pressure_callback_period(self.vCbPeriod)
        self.hMe.register_callback(self.hMe.CALLBACK_AIR_PRESSURE, self.cb_barometer)

    def get_air_pressure(self):
        air_pressure = self.hMe.get_air_pressure()
        return air_pressure

    def getValue(self):
        return round(self.get_air_pressure() / 100)

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4223
    UID = "fYc" # Change to your UID

    ipcon = IPConnection() # Create IP connection
    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    hdl_barometer = c_barometer(UID, "hPa", "Luftdruck")
    hdl_barometer.setup(ipcon)
    
    if False:
        hdl_barometer.startCallback()
        input('Press key to exit\n') # Use input() in Python 3
    else:
        air_pressure = hdl_barometer.getValue()
        print(f"Luftdruck: {air_pressure} {hdl_barometer.Entity}")
    
    ipcon.disconnect()