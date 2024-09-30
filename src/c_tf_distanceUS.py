#!/usr/bin/python
# -*- coding: utf-8 -*-  

from c_emitter import c_emitter
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_distance_us import DistanceUS
from simple_log import log

class c_tf_distanceUS(c_emitter):
	def __init__(self, device_id, entity="", label="", location=""):
		hMe = 0
		vCbPeriod = 5000
		hCollector = None
		BottomLevel = 310
		super().__init__(device_id, entity, label, location)

	def setup(self, _IpConnection, _hCollector = None):
		self.hCollector = _hCollector
		self.hMe = DistanceUS(self.ID, _IpConnection)

	def cb_distanceUS(self, _Distance):
		if self.hCollector == 0:
			log.info(_Distance)
		else:
			self.hCollector.setValue(_Distance)

	def startCallback(self):
		self.hMe.set_distance_callback_period(self.vCbPeriod)
		self.hMe.register_callback(self.hMe.CALLBACK_DISTANCE, self.cb_distanceUS)

	def getDistance(self):
		distance = self.hMe.get_distance_value()/10
		return distance

	def getValue(self):
		distance = self.getDistance()
		if distance > self.BottomLevel:
			self.BottomLevel = distance
			return 0
		else:
			return (self.BottomLevel - self.getDistance())

if __name__ == "__main__":
	HOST = "localhost"
	PORT = 4223
	UID = "n1j" # Change to your UID

	ipcon = IPConnection() # Create IP connection
	ipcon.connect(HOST, PORT) # Connect to brickd
	# Don't use device before ipcon is connected

	hDistance = c_tf_distanceUS(UID, "cm", "Wasserspiegel")
	hDistance.setup(ipcon)
	
	if True:
		hDistance.startCallback()
		input('Press key to exit\n') # Use input() in Python 3
	else:
		vDistance = hDistance.getValue()
		print("Distance: " + str(vDistance) + hDistance.Entity)
	
	ipcon.disconnect()
