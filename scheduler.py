from q import Queue
from heap import Heap
from typing import Iterator, Union
from event import Event
from math import inf

class Scheduler:

    def __init__(self, queues: list[Queue], randoms: Iterator[float]):
        self.queues = queues
        self.randoms = randoms

        self.curr_time = 0
        self.heap = Heap[Event]()
    
    def simulate(self):
        for queue in self.queues:
            queue.scheduler = self

        while self.heap.size > 0:
            event = self.heap.poll()
            self.curr_time = event.time

            event.target.handle_event(event.type)
        
        for queue in self.queues:
            queue.print_statisticss()

    def schedule_range(self, time_range: tuple[float, float], type: str, target: Queue):
        try:
            time = self.curr_time + self.get_random(time_range)
            self.heap.add(Event(time, type, target))
        except StopIteration:
            pass

    def schedule_immediate(self, type: str, target: Queue):
        self.heap.add(Event(self.curr_time, type, target))
    
    def schedule(self, time: float, type: str, target: Queue):
        self.heap.add(Event(time, type, target))

    def get_random(self, time_range: tuple[float, float]):
        start, end = time_range
        random = next(self.randoms)
        return round((end - start) * random + start, 4)