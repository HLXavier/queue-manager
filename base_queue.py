from event import Event


ARRIVAL = 'arrival'
DEPARTURE = 'departure'


class Queue:

    def __init__(self, servers, capacity, arrival_time, departure_time):
        self.servers = servers
        self.capacity = capacity

        self.arrival_time = arrival_time
        self.departure_time = departure_time

        self.size = 0
        self.scheduler = None

        self.losses = 0
    
    
    def arrival(self, next=DEPARTURE):
        if self.size < self.capacity:
            self.size += 1
            if self.size <= self.servers:
                self.scheduler.schedule(self.departure_time, next)
        else:
            self.losses += 1
    

    def departure(self, next=DEPARTURE):
        self.size -= 1
        if self.size >= self.servers:
            self.scheduler.schedule(self.departure_time, next)  
