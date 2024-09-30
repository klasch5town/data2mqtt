#!/usr/bin/python
#
#
from simple_log import log
from c_emitter import c_emitter
from pi1wire import Pi1Wire, Resolution


class c_1wireTemp(c_emitter):
	def __init__(self, sensor_id, entity="", label="", location="default"):
		# read sensors into dictionary
		self.p1w_sensor_list = Pi1Wire().find_all_sensors()
		self.sensor_handle = None
		for device in self.p1w_sensor_list:
			log.debug(device.mac_address)
			if device.mac_address == sensor_id:
				self.sensor_handle = device
				c_emitter.__init__(self,sensor_id, entity, label, location)
				break
		if self.sensor_handle is None:
			log.error(f"{sensor_id} not found!")

	def get_value(self):
		Temperature = self.sensor_handle.get_temperature()
		return format(Temperature,".1f")


if __name__ == '__main__':
	log.basicConfig(level=log.INFO)
	hTemp = c_1wireTemp("10000802c5aeb7","°C","Temperature")
	Temperature = hTemp.getValue()
	print(f"{hTemp.Label}:{Temperature}{hTemp.Entity}")
