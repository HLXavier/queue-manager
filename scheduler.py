from q import Queue
from heap import Heap
from typing import Iterator, Union
from event import Event
from math import inf
from tabulate import tabulate

class Scheduler:

    def __init__(self, queues: list[Queue], randoms: Iterator[float], output_table: bool, randoms_limit: float):
        self.queues = queues
        self.randoms = randoms

        self.curr_time = 0
        self.heap = Heap[Event]()
        self.consumed_randoms = 0
        self.history: list[Event] = []
        self.output_table = output_table 
        self.randoms_limit = randoms_limit
    
    def simulate(self):
        for queue in self.queues:
            queue.scheduler = self

        while self.heap.size > 0 and self.consumed_randoms < self.randoms_limit:
            event = self.heap.poll()

            if event.time < self.curr_time:
                raise Exception('time travelling!')

            self.curr_time = event.time

            event.target.handle_event(event.type)
        
        for queue in self.queues:
            queue.print_statisticss()

        self.generate_table()

    def schedule_range(self, time_range: tuple[float, float], type: str, target: Queue):
        try:
            time = self.curr_time + self.get_random(time_range)
            self.add(Event(time, type, target))
        except StopIteration:
            print(f'Failed to schedule {type} {target.name}')
            pass

    def schedule_immediate(self, type: str, target: Queue):
        self.add(Event(self.curr_time, type, target))
    
    def schedule(self, time: float, type: str, target: Queue):
        self.add(Event(time, type, target))

    def add(self, e: Event):
        if self.output_table:
            self.history.append(e)
        
        self.heap.add(e)

    def get_random(self, time_range: tuple[float, float]):
        start, end = time_range
        random = next(self.randoms)
        self.consumed_randoms += 1
        return round((end - start) * random + start, 4)

    def generate_table(self):
        if self.output_table == False:
            return
        
        headers = ['event', 'target', 'time']
        print('generating scheduler table...')
        self.history.sort(key=lambda e: e.time)
        with open('outputs/scheduler.txt', 'w') as result_file:
            result_file.write(tabulate([(e.type, e.target.name, e.time) for e in self.history], tablefmt='orgtbl', headers=headers))