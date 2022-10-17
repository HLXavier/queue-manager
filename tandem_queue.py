from scheduler import Scheduler


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

    
    def simulate(self):
        self.queue1.schedule_arrival(self.first_arrival)
        # update table

        while self.scheduler.randoms:
            event = self.scheduler.pop()
            self.scheduler.update_time(event.time)

            if event.type == ARRIVAL:
                self.queue1.arrival(next=TRANSITION)
                self.scheduler.schedule(self.queue.arrival_time, ARRIVAL)

            if event.type == TRANSITION:
                self.queue1.departure(next=TRANSITION)
                self.queue2.arrival()

            if event.type == DEPARTURE:
                self.queue2.departure()
            
            # update table
