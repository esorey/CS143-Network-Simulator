class event:
	def __init__(self, event_type, time):
		'''
			event_type - enumerated type that indicates what sort of event 
						 this is 
			time - integer, when the event occurs
		'''
		self.type = event_type
		self.time = time

	def getTime(self):
		return self.time

	def getEventType(self):
		return self.event_type
