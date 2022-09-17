from simple_queue import Queue 


queue = Queue(1, 2, [1, 4], [1, 3], first_arrival=1)
queue.simulate()
queue.generate_table()