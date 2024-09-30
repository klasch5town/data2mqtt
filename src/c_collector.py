#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shark
#
# Created:     14.04.2014
# Copyright:   (c) shark 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from simple_log import log

class c_collector:
	"""My collector-class - it will collect data from all sensors in the handle-list."""
	def __init__(self):
		self.HandleList = {}
		self.ValueList = {}
		self.ChangedFlag = False

	def setValue(self, _ID, _Value):
		"""for call-back functions"""
		log.info("Got value from [" + _ID + "]: "+str(_Value))
		self.ValueList[_ID] = _Value
		self.ChangedFlag = True

	def getValueString(self):
		ValueString = ""
		for Item in self.HandleList:
			ValueString += str(self.ValueList[Item]) + "\t"
		return ValueString
	
	def getHeaderString(self):
		HeaderString = ""
		for Item in self.HandleList:
			HeaderString += self.HandleList[Item].Label + "\t"
		return HeaderString

	def printValues(self):
		print(self.getValueString())

	def addSource(self, _hSource):
		self.HandleList[_hSource.ID] = _hSource
		self.ValueList[_hSource.ID] = None

	def listSources(self):
		for Item in self.HandleList:
			outString = "ID = " + self.HandleList[Item].ID
			outString += "\tLabel = " + self.HandleList[Item].Label
			outString += "\tObject = " + str(self.HandleList[Item])
			print(outString)

	def pollValues(self):
		self.ChangedFlag = False
		for Item in self.HandleList:
			Value = self.HandleList[Item].getValue()
			if Value != self.ValueList[Item]:
				self.ChangedFlag = True
				log.info(Value)
			self.ValueList[Item] = Value

if __name__ == '__main__':
	from time import sleep
	from c_1wireTemp import c_1wireTemp
	from tinkerforge.ip_connection import IPConnection
	from c_tf_distanceUS import c_distanceUS

	log.basicConfig(level=log.INFO)

	hColl = c_collector()

	#HOST = "localhost"
	HOST = "192.168.150.191"
	PORT = 4223
	UID_DistanceUS = "n1j" # Change to your UID

	ipcon = IPConnection() # Create IP connection
	ipcon.connect(HOST, PORT) # Connect to brickd
	# Don't use device before ipcon is connected
	hDistance = c_distanceUS(UID_DistanceUS, "mm", "Wasserspiegel")
	hDistance.setup(ipcon)
	hColl.addSource(hDistance)
	
	hAbluft = c_1wireTemp("10000802c5aeb7", "C", "Abluft")
	hColl.addSource(hAbluft)

	#Counter = 0
	while(True):
		hColl.pollValues()
		if hColl.ChangedFlag:
			log.info(hColl.getValueString())
		#Counter += 1
		sleep(60)

	#input('Press key to exit\n') # Use input() in Python 3
	ipcon.disconnect()
