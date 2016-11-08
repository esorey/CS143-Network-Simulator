from enum import Enum


class event:
	class event_type(Enum):
		pckt_rcv = 1
		pckt_send = 2
		pckt_drop = 3
		flow_start = 4
	def __init__(self, ev_type, time):
		'''
			event_type - enumerated type that indicates what sort of event 
						 this is 
			time - integer, when the event occurs
		'''
		self.event_type = ev_type
		self.time = time

	def getTime(self):
		return self.time

	def getEventType(self):
		return self.event_type
