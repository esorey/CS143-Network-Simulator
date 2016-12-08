from event import Event
import constants

class EventQueue:
    def __init__(self):
        '''
        Event Queue is a priority queue of Event objects that are sorted
        based on their time property when they are enqueued.
        '''
        self.currentTime = 0    # Current time
        self.eventList = []     # Sorted queue of events

    def dequeue(self):
        '''
            Returns the next chronological event (event with the smallest 
            time property).
        '''
        if constants.debug: 
            print("Event is getting dequeued")
            print("\tevent: %s" %self.eventList[0].event_type)

        ret_event = self.eventList[0]   # Get event to dequeue
        del self.eventList[0]           # Remove this event from queue

        self.currentTime = ret_event.time   # Update current time
        return ret_event                    # And return this event

    def enqueue(self, event):
        '''
            Enqueues the passed event to the event_queue.
        '''
        # Determine index to insert event based on time property
        ind_to_insert = self.getIndextoInsert(event.time)

        if constants.debug: 
            print("Currently Enqueueing...")
            print("\tInserting at index: %s" % ind_to_insert)
            print("\tInserting time: %s " % event.time)
            print("\tInserting event type: %s" % event.event_type)

        # Insert/enqueue event
        self.eventList.insert(ind_to_insert, event)  

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
            return 0                #   at index 0

        # If the value is smaller than the first element in the array, insert
        #   element at the beginning of the queue
        if event_time < self.eventList[0].time:
            return 0

        # If the value is greater than or equal to the last element in the
        #   array, insert it at the end
        if event_time >= self.eventList[-1].time:
            return self.getSize()

        left = 0
        right = self.getSize()

        # Binary search for index to insert
        while True:
            m = (left + right)//2       # Get index between left and right
            event_m = self.eventList[m] # Get the event at this middle index

            if right - left == 1:       # If left and right are adjacent
                return right            # Insert element between them

            # Otherwise narrow the interval
            elif event_time >= event_m.time:
                left = m
            elif event_time < event_m.time:
                right = m

            # If the event_time is the same as event_m time, insert event
            #   after all events with the same time
            elif event_time == event_m.time:
                ret_ind = m+1
                while self.eventList[ret_ind].time == event_time:
                    ret_ind += 1

                return ret_ind



