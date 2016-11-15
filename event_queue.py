from event import Event
class EventQueue:
    def __init__(self):
        self.currentTime = 0       # Current time
        self.eventList = []         # List of events (sorted by time property)

    def dequeue(self):
        '''
            Returns the event with the smallest time property
            The function gets the first event in the eventList, removes it
            from the list, and returns it
        '''
        if constants.debug: 
            print("Event is getting dequeued")
            print("\tevent: %s" %self.eventList[0].event_type)
        ret_event = self.eventList[0]   # Get event to dequeue
        del self.eventList[0]           # Remove this event from queue

        # Update time variable
        self.currentTime = ret_event.time
        return ret_event                # And return this event

    def enqueue(self, event):
        '''
            Enqueues the passed event to the event_queue.
            The function enqueues the event by inserting it into the list of
            events in order of the time the event should be executed.
        '''
        # Determine index to insert event based on time property
        ind_to_insert = self.getIndextoInsert(event.time)
        if constants.debug: 
            print("Currently Enqueueing...")
            print("\tInserting at index: %s" % ind_to_insert)
            print("\tInserting time: %s " % event.time)
            print("\tInserting event type: %s" % event.event_type)
        self.eventList.insert(ind_to_insert, event)  # Insert/enqueue event

        return True

    def isempty(self):
        '''
            Returns true if event_queue is empty, false if it is not empty
        '''
        return self.eventList == []

    def getSize(self):
        '''
            Returns the length of the event event_queue
        '''
        return len(self.eventList)

    def getIndextoInsert(self, event_time):
        '''
            This function determines the index at which to insert an event
            into the list based on the event's time property.
            The function returns the index at which to insert the element.
        '''

        if self.getSize() == 0:     # If the list is empty, insert element  
            return 0                   #   at index 0

        # If the value is smaller than the first element in the array
        if event_time < self.eventList[0].time:
            return 0

        # If the value is greater than or equal to the last element in the array
        if event_time >= self.eventList[-1].time:
            return self.getSize()

        left = 0
        right = self.getSize()

        while True:
            m = (left + right)//2       # Get index between left and right
            event_m = self.eventList[m] # Get the event at this middle index

            if right - left == 1:       # If left and right are adjacent
                return right            # Insert element at right index

            # Otherwise narrow the interval
            elif event_time >= event_m.time:
                left = m
            elif event_time < event_m.time:
                right = m

            # If the event_time is the same as event_m time, insert event
            #   next to middle element
            elif event_time == event_m.time:
                return m+1



