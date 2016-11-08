from event import getTime
class event_queue:
    def __init__(self):
        '''
            itemList is a list of events that is sorted (as elements are 
                added) in order of each event's time property
        '''
        # Global time variable
        self.eventList = [];

    def dequeue(self):
        '''
            Returns the event with the smallest time property
            The function gets the first event in the eventList, removes it
            from the list, and returns it
        '''
        ret_event = self.eventList[0]   # Get event to dequeue
        del self.eventList[0]           # Remove this event from queue

        # Update global time
        return ret_event                # And return this event

    def enqueue(self, event):
        '''
            Enqueues the passed event to the event_queue.
            The function enqueues the event by inserting it into the list of
            events in order of the time the event should be executed.
        '''
        # Determine index to insert event based on time property
        ind_to_insert = self.getIndextoInsert(self, event.getTime())

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

        if len(self.eventList) == 0:     # If the list is empty, insert element  
            return 0                    #   at index 0

        left = 0
        right = len(self.eventList)-1

        while True:
            m = (left + right)//2       # Get index between left and right
            event_m = self.eventList[m] # Get the event at this middle index

            if right - left <= 1:       # If left and right are adjacent
                return right            # Insert element at right index

            # Otherwise narrow the interval
            elif event_time > event_m.getTime():
                left = m
            elif event_time < event_m.getTime():
                right = m

            # If the event_time is the same as event_m time, insert event
            #   next to middle element
            elif event_time == event_m.getTime():
                return m+1

