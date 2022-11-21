import yaml
from yaml.loader import FullLoader
from q import Queue, ARRIVAL
from scheduler import Scheduler
from pseudorandom import random_generator

def read_config(path: str):
    with open(path) as f:
        data = yaml.load(f, Loader=FullLoader)

        queues: list[Queue] = []

        for queue_name in data['queues']:
            queue_config = data['queues'][queue_name]

            servers = queue_config['servers']
            departure = (queue_config['minService'], queue_config['maxService'])

            capacity = None
            if 'capacity' in queue_config:
                capacity = queue_config['capacity']

            arrival = None
            if 'minArrival' in queue_config and 'maxArrival' in queue_config:
                arrival = (queue_config['minArrival'], queue_config['maxArrival'])

            q = Queue(
                name=queue_name,
                servers=servers,
                capacity=capacity,
                arrival_time_range=arrival,
                departure_time_range=departure,
                connections=[],
                output_table=False
            )

            queues.append(q)

        
        for conn in data['network']:
            source = next(q for q in queues if q.name == conn['source'])
            target = next(q for q in queues if q.name == conn['target'])
            probability = conn['probability']

            source.connections.append((target, probability))


        scheduler = Scheduler(queues=queues, randoms=random_generator(data['random_count']), output_table=False, randoms_limit=data['random_count'])
        # scheduler = Scheduler(queues=queues, randoms=iter([0.2176,0.0103,0.1109,0.3456,0.9910,0.2323,0.9211,0.0322,0.1211,0.5131,0.7208,0.9172,0.9922,0.8324,0.5011,0.2931]))

        for queue_name in data['arrivals']:
            q = next(q for q in queues if q.name == queue_name)
            time = data['arrivals'][queue_name]

            scheduler.schedule(time, ARRIVAL, q)

        return scheduler
    
