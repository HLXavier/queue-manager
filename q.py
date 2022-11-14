from tabulate import tabulate
from typing import Union


ARRIVAL = 'arrival'
DEPARTURE = 'departure'


class Queue:

    def __init__(
        self,
        servers: int,
        capacity: int,
        arrival_time_range: tuple[float, float] | None,
        departure_time_range: tuple[float, float],
        connections: Union[list['Queue'], None],
        name: str
    ):
        self.servers = servers
        self.capacity = capacity

        self.arrival_time_range = arrival_time_range
        self.departure_time_range = departure_time_range

        self.connections = connections
        self.name = name

        self.size = 0
        self.scheduler: 'Scheduler' = None # set externally by Scheduler


        self.last_table_update_time = 0
        self.losses = 0
        self.state_durations = [0] * (capacity + 1)
        self.table = []

        self.normalize_connection_probs()
    

    def handle_event(self, type: str):
        self.update_table(type)

        if type == ARRIVAL:
            self.arrival()
        elif type == DEPARTURE:
            self.departure()
    

    def arrival(self):
        if self.size < self.capacity:
            self.size += 1
            if self.size <= self.servers:
                self.scheduler.schedule_range(self.departure_time_range, DEPARTURE, self)
        else:
            self.losses += 1
        
        if self.arrival_time_range:
            self.scheduler.schedule_range(self.arrival_time_range, ARRIVAL, self)
    

    def departure(self):
        self.size -= 1
        if self.size >= self.servers:
            self.scheduler.schedule_range(self.departure_time_range, DEPARTURE, self)
        
        if self.connections:
            try:
                next = self.choose_next()
                self.scheduler.schedule_immediate(ARRIVAL, next)
            except StopIteration:
                pass
        

    def choose_next(self):
        if len(self.connections) == 1:
            return self.connections[0][0]
        
        rand = self.scheduler.get_random([0, 1])
        acc_prob = 0
        for i in range(len(self.connections)):
            queue, prob = self.connections[i]
            if rand >= acc_prob and rand <= acc_prob + prob:
                return queue
            
            acc_prob += prob



    def normalize_connection_probs(self):
        if self.connections is None:
            return
        
        total_prob = sum([prob for queue, prob in self.connections])
        self.connections = [(queue, prob/total_prob) for queue, prob in self.connections]

    def update_table(self, event):
        duration = self.scheduler.curr_time - self.last_table_update_time
        self.last_table_update_time = self.scheduler.curr_time
        self.state_durations[self.size] += duration     

        line = [event, self.size, self.scheduler.curr_time, *self.state_durations]
        self.table.append(line)


    def generate_table(self):
        headers = ['event', 'size', 'time'] + ['s' + str(i) for i in range(self.capacity + 1)]
        with open(self.name + '.txt', 'w') as result_file:
            result_file.write(tabulate(self.table, tablefmt='orgtbl', headers=headers))


    def get_results(self):
        probabilities = [(state / self.scheduler.curr_time) * 100 for state in self.state_durations]
        return probabilities, self.losses


