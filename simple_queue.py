from pseudorandom import get_randoms 
from heap import Heap
from event import Event
from tabulate import tabulate
from sys import argv

ARRIVAL = 'arrival'
DEPARTURE = 'departure'

class Queue:

    def __init__(self, servers, capacity, arrival_time, departure_time, seed, first_arrival=0, rounds=10):
        # C
        self.servers = servers
        # K
        self.capacity = capacity

        # Global time
        self.time = 0

        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.first_arrival = first_arrival

        self.size = 0
        self.scheduler = Heap()

        self.states = [0 for _ in range(capacity + 1)]
        self.losses = 0

        self.randoms = get_randoms(rounds, seed)

        self.table = []

    
    def simulate(self):
        self.schedule_arrival(self.first_arrival)
        self.update_table()

        while self.randoms:
            event = self.scheduler.poll()

            if event.type == ARRIVAL:
                self.arrival(event.time)

            if event.type == DEPARTURE:
                self.departure(event.time)
            
            self.update_table(event.type)
    
    
    def arrival(self, time):
        self.mark_time(time)

        if self.size < self.capacity:
            self.size += 1
            if self.size <= self.servers:
                waiting = self.random(self.departure_time)
                self.schedule_departure(self.time + waiting)
        else:
            self.losses += 1

        self.schedule_arrival(self.time + self.random(self.arrival_time))
    

    def departure(self, time):
        self.mark_time(time)

        self.size -= 1
        if self.size >= self.servers:
            waiting = self.random(self.departure_time)
            self.schedule_departure(self.time + waiting)
        
    
    def mark_time(self, time):
        duration = time - self.time
        self.states[self.size] += duration       
        self.time = time

    
    def schedule_arrival(self, time):
        event = Event(time, ARRIVAL)
        self.scheduler.add(event)

    
    def schedule_departure(self, time):
        event = Event(time, DEPARTURE)
        self.scheduler.add(event)


    def random(self, base):
        start, end = base
        random = self.randoms.pop() 
        return round((end - start) * random + start, 4)
            

    def update_table(self, event='-'):
        line = [event, self.size, self.time, *self.states]
        self.table.append(line)


    def generate_table(self):
        headers = ['event', 'size', 'time'] + ['s' + str(i) for i in range(self.capacity + 1)]
        with open('result', 'w') as result_file:
            result_file.write(tabulate(self.table, tablefmt='orgtbl', headers=headers))


    def get_results(self):
        probabilities = [(state / self.time) * 100 for state in self.states]
        return self.states, probabilities, self.losses