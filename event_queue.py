class event_queue:
	def __init__(self, event):
		'''
			Need some way to hold events
		'''

	def dequeue(self):
		'''
			return most recently enqueued event (sort by time property of
			events)
		'''

	def enqueue(self, event):
		'''
			enqueue the event
			maybe sort here? or sort in dequeue? based on time property
		'''

	def isempty(self):
		'''
			return self.data == []
		'''
