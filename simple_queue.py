from scheduler import Scheduler
from base_queue import Queue
from tabulate import tabulate


ARRIVAL = 'arrival'
DEPARTURE = 'departure'


class SimpleQueue:

    def __init__(self, queue, first_arrival=0, rounds=10, seed=1234):
        self.scheduler = Scheduler(rounds, seed)
        self.queue = queue
        self.queue.scheduler = self.scheduler

        self.first_arrival = first_arrival
        
        self.states = [0 for _ in range(self.queue.capacity + 1)]
        self.table = []

    
    def simulate(self):
        self.scheduler.first_arrival(self.first_arrival)
        self.update_table()

        while self.scheduler.randoms:
            event = self.scheduler.pop()
            self.mark_time(event.time)

            if event.type == ARRIVAL:
                self.queue.arrival()
                self.scheduler.schedule(self.queue.arrival_time, ARRIVAL)

            if event.type == DEPARTURE:
                self.queue.departure()
            
            self.update_table(event.type)
        
    
    def mark_time(self, time):
        duration = time - self.scheduler.time
        self.scheduler.update_time(time)
        self.states[self.queue.size] += duration       
            

    def update_table(self, event='-'):
        line = [event, self.queue.size, self.scheduler.time, *self.states]
        self.table.append(line)


    def generate_table(self):
        headers = ['event', 'size', 'time'] + ['s' + str(i) for i in range(self.queue.capacity + 1)]
        with open('simple_queue_result', 'w') as result_file:
            result_file.write(tabulate(self.table, tablefmt='orgtbl', headers=headers))


    def get_results(self):
        probabilities = [(state / self.scheduler.time) * 100 for state in self.states]
        return self.states, probabilities, self.queue.losses
