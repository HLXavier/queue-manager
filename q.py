from tabulate import tabulate
from typing import Any
from event import Event

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

        self.output_table = output_table
        self.next_universe_event: Event | None = None
    

    def handle_event(self, event: Event):
        self.update_table(event.type)

        prev = self.size

        if event.type == ARRIVAL:
            self.arrival(event)
        elif event.type == DEPARTURE:
            self.departure()
        else:
            raise Exception(f'Unknown event type {event.type}')

    def arrival(self, event: Event):
        if self.capacity == None or self.size < self.capacity:
            self.size += 1
            if self.size <= self.servers:
                self.scheduler.schedule_range(self.departure_time_range, DEPARTURE, self)
        else:
            self.losses += 1
        
        if self.arrival_time_range and (self.next_universe_event == None or event == self.next_universe_event):
            self.next_universe_event = self.scheduler.schedule_range(self.arrival_time_range, ARRIVAL, self)
    

    def departure(self):
        self.size -= 1
        if self.size >= self.servers:
            self.scheduler.schedule_range(self.departure_time_range, DEPARTURE, self)
        
        try:
            next = self.choose_next()
            if next:
                self.scheduler.schedule_immediate(ARRIVAL, next)
            
        except StopIteration:
            pass

    def choose_next(self):       
        rand = self.scheduler.get_random((0, 1))
        acc_prob = 0
        for i in range(len(self.connections)):
            queue, prob = self.connections[i]
            if rand >= acc_prob and rand <= acc_prob + prob:
                return queue
            
            acc_prob += prob

    def update_table(self, event):
        duration = self.scheduler.curr_time - self.last_table_update_time
        self.last_table_update_time = self.scheduler.curr_time

        if self.size < len(self.state_durations):
            self.state_durations[self.size] += duration
        else:
            self.state_durations.append(duration)

            # sanity check just to be sure
            if len(self.state_durations) - 1 != self.size:
                print(self.state_durations)
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

        table = list(zip(state_names, self.state_durations, probabilities))
        
        print(f'\n## Results for {self.name}:')
        print(tabulate(table, headers=['State', 'Time', 'Probability'], floatfmt='0.2f'))
        print(f'Losses: {self.losses}')

        print(f'\n## Configs for {self.name}:')

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
            print(f' - To {conn[0].name} ({conn[1]})')

        print('=================================')
        print()

        self.generate_table()


