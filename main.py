from scheduler import Scheduler
from pseudorandom import random_generator
from q import Queue, ARRIVAL
from tabulate import tabulate

rands = [0.9921,0.0004,0.5534,0.2761,0.3398,0.8963,0.9023,0.0132,0.4569,0.5121,0.9208,0.0171,0.2299,0.8545,0.6001,0.2921]

q2 = Queue(servers=1, capacity=3, arrival_time_range=None, departure_time_range=[3,5], connections=None, name='Q2')
q1 = Queue(servers=2, capacity=3, arrival_time_range=[2,3], departure_time_range=[2,5], connections=[(q2, 1)], name='Q1')

queues = [
    q1,
    q2
]
scheduler = Scheduler(
    queues=queues,
    randoms=iter(rands)
)

scheduler.schedule(2.5, ARRIVAL, q1)

scheduler.simulate()

for queue in queues:
    queue.generate_table()
    # todo print results