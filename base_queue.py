from tabulate import tabulate


ARRIVAL = 'arrival'
DEPARTURE = 'departure'


class Queue:

    def __init__(self, servers, capacity, arrival_time_range, departure_time_range):
        self.servers = servers
        self.capacity = capacity

        self.arrival_time_range = arrival_time_range
        self.departure_time_range = departure_time_range

        self.size = 0
        self.scheduler = None

        self.losses = 0
    
    
    def arrival(self, next=DEPARTURE):
        if self.size < self.capacity:
            self.size += 1
            if self.size <= self.servers:
                self.scheduler.schedule(self.departure_time_range, next)
        else:
            self.losses += 1
    

    def departure(self, next=DEPARTURE):
        self.size -= 1
        if self.size >= self.servers:
            self.scheduler.schedule(self.departure_time_range, next)  
