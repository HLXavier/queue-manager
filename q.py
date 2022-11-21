from tabulate import tabulate
from typing import Any

ARRIVAL = 'arrival'
DEPARTURE = 'departure'


class Queue:

    def __init__(
        self,
        servers: int,
        capacity: int | None,
        arrival_time_range: tuple[float, float] | None,
        departure_time_range: tuple[float, float],
        connections: list[tuple['Queue', float]],
        name: str,
        output_table: bool
    ):
        self.servers = servers
        self.capacity = capacity

        self.arrival_time_range = arrival_time_range
        self.departure_time_range = departure_time_range

        self.connections: list[tuple['Queue', float]] = connections
        self.name = name

        self.size = 0

        # set externally by Scheduler
        self.scheduler: 'Scheduler' = None  # type: ignore


        self.last_table_update_time = 0
        self.losses = 0
        self.state_durations: list[float] = [0]
        self.table: list[Any] = []
        self.event_count = 0
        self.transfer_count = [0, 0, 0]

        self.output_table = output_table
    

    def handle_event(self, type: str):
        self.update_table(type)

        if type == ARRIVAL:
            self.arrival()
        elif type == DEPARTURE:
            self.departure()
    

    def arrival(self):
        if self.capacity == None or self.size < self.capacity:
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
        
        try:
            next = self.choose_next()
            if next:
                self.scheduler.schedule_immediate(ARRIVAL, next)
            
        except StopIteration:
            print(f'failed to transfer from {self.name}')
            pass

    def choose_next(self):
        if len(self.connections) < 1:
            return None

        # if len(self.connections) == 1:
        #     # self.scheduler.get_random((0, 1))
        #     return self.connections[0][0]
        
        rand = self.scheduler.get_random((0, 1))
        acc_prob = 0
        for i in range(len(self.connections)):
            queue, prob = self.connections[i]
            if rand >= acc_prob and rand <= acc_prob + prob:
                self.transfer_count[i] += 1
                return queue
            
            acc_prob += prob
        
        self.transfer_count[2] += 1

    def update_table(self, event):
        duration = self.scheduler.curr_time - self.last_table_update_time
        self.last_table_update_time = self.scheduler.curr_time

        if self.size < len(self.state_durations):
            self.state_durations[self.size] += duration
        else:
            self.state_durations.append(duration)

            # sanity check just to be sure
            if len(self.state_durations) - 1 != self.size:
                raise Exception('state_durations got corrupted')

        if self.output_table:
            line = [event, self.size, self.scheduler.curr_time, *self.state_durations]
            if self.event_count < len(self.table):
                self.table[self.event_count] = line
            else:
                self.table.append(line)

        self.event_count += 1

    def generate_table(self):
        if self.output_table == False:
            return
        
        headers = ['event', 'size', 'time'] + ['s' + str(i) for i in range(len(self.state_durations))]
        print('generating tables...')
        with open('outputs/' + self.name + '.txt', 'w') as result_file:
            result_file.write(tabulate(self.table, tablefmt='orgtbl', headers=headers))


    def get_probabilities(self):
        return [(state / self.scheduler.curr_time) * 100 for state in self.state_durations]


    def print_statisticss(self):
        probabilities = self.get_probabilities()

        state_names = [i for i in range(len(self.state_durations))]

        table = list(zip(state_names, probabilities, self.state_durations))
        
        print(f'\nResults for {self.name}:')
        print(tabulate(table, headers=['State', 'Probability', 'Time',], floatfmt='0.2f'))
        print(f'Avg losses: {self.losses}')
        if self.arrival_time_range != None:
            print(f'Arrival: {self.arrival_time_range[0]}..{self.arrival_time_range[1]}')
        else:
            print(f'Arrival: -')

        print(f'Departure: {self.departure_time_range[0]}..{self.departure_time_range[1]}')
        print(f'Servers: {self.servers}')
        if self.capacity != None:
            print(f'Capacity: {self.capacity}')
        else:
            print(f'Capacity: -')

        print('Connections:')
        for conn in self.connections:
            print(f'To {conn[0].name} ({conn[1]})')

        
        self.generate_table()
        total_transfers = sum(self.transfer_count)
        # print(f'total transfers: {total_transfers}')
        # print(f'transfers: {[count / total_transfers for count in self.transfer_count]}')


