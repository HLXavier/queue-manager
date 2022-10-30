from heap import Heap
from event import Event
from pseudorandom import get_randoms


ARRIVAL = 'arrival'


class Scheduler:

    def __init__(self, rounds, seed):
        self.time = 0
        self.heap = Heap()
        # self.randoms = get_randoms(rounds, seed)
        self.randoms = [0.9921, 0.0004, 0.5534, 0.2761, 0.3398, 0.8963, 0.9023, 0.0132, 0.4569, 0.5121, 0.9208, 0.0171, 0.2299, 0.8545, 0.6001, 0.2921]


    def random(self, time_range):
        start, end = time_range
        random = self.randoms.pop(0) 
        return round((end - start) * random + start, 4)


    def first_arrival(self, time):
        event = Event(time, ARRIVAL)
        self.heap.add(event)
        
    
    def schedule(self, time_range, type):
        if self.randoms:
            waiting = self.random(time_range)
            event = Event(self.time + waiting, type)
            self.heap.add(event)

    
    def pop(self):
        return self.heap.poll()


    def update_time(self, time):
        self.time = time