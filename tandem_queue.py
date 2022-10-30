from scheduler import Scheduler
from tabulate import tabulate


ARRIVAL = 'arrival'
TRANSITION = 'transition'
DEPARTURE = 'departure'


class TandemQueue:

    def __init__(self, queue1, queue2, first_arrival=0, rounds=10, seed=1234):
        self.scheduler = Scheduler(rounds, seed)

        self.queue1 = queue1
        self.queue2 = queue2
        self.queue1.scheduler = self.scheduler
        self.queue2.scheduler = self.scheduler

        self.first_arrival = first_arrival

        self.states1 = [0] * (self.queue1.capacity + 1)
        self.states2 = [0] * (self.queue2.capacity + 1)
        self.table1 = []
        self.table2 = []
    

    def simulate(self):
        self.scheduler.first_arrival(self.first_arrival)

        while self.scheduler.randoms:
            event = self.scheduler.pop()
            self.scheduler.update_time(event.time)

            if event.type == ARRIVAL:
                self.update_table(event.time, self.table1, self.states1, self.queue1.size, event.type)
                self.queue1.arrival(next=TRANSITION)
                self.scheduler.schedule(self.queue1.arrival_time_range, ARRIVAL)

            if event.type == TRANSITION:
                self.update_table(event.time, self.table1, self.states1, self.queue1.size, event.type)
                self.update_table(event.time, self.table2, self.states2, self.queue2.size, event.type)
                self.queue1.departure(next=TRANSITION)
                self.queue2.arrival()

            if event.type == DEPARTURE:
                self.update_table(event.time, self.table2, self.states2, self.queue2.size, event.type)
                self.queue2.departure()      
            

    def update_table(self, time, table, states, queue_size, event='-'):
        duration = time - self.scheduler.time
        states[queue_size] += duration 
        line = [event, queue_size, self.scheduler.time, *states]
        table.append(line)


    def generate_table(self, table, queue, number):
        headers = ['event', 'size', 'time'] + ['s' + str(i) for i in range(queue.capacity + 1)]
        with open(f'tandem_queue_result{number}', 'w') as result_file:
            result_file.write(tabulate(table, tablefmt='orgtbl', headers=headers))


    def get_results(self, states):
        probabilities = [(state / self.scheduler.time) * 100 for state in states]
        return states, probabilities, self.queue.losses
