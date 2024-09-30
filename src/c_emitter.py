#!/bin/python
#
#
from simple_log import log

class c_emitter:
	"""
	This class is for sensors that can 'emit' data.
	"""

	def __init__(self, device_id, entity = "", label = "", location=""):
		self.ID = device_id
		self.Entity = entity
		self.Label = label
		self.Location = location

	def info_string(self):
		return f"ID: {self.ID}\tlabel: {self.Label}\tlocation: {self.Location}"
