from base_queue import Queue
from simple_queue import SimpleQueue
from tandem_queue import TandemQueue


queue = Queue(1, 3, [1, 2], [3, 6])
simple = SimpleQueue(queue, first_arrival=2)
simple.simulate()
simple.generate_table()

queue1 = Queue(2, 3, [2, 3], [2, 5])
queue2 = Queue(1, 3, [], [3, 5])
tandem = TandemQueue(queue1, queue2, first_arrival=2.5)
tandem.simulate()
tandem.generate_table(tandem.table1, tandem.queue1, 1)
tandem.generate_table(tandem.table2, tandem.queue2, 2)