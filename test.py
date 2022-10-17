from base_queue import Queue
from simple_queue import SimpleQueue


queue = Queue(1, 3, [1, 2], [3, 6])
simple = SimpleQueue(queue, first_arrival=2)
simple.simulate()
simple.generate_table()