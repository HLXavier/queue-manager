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
                connections=[]
            )

            queues.append(q)

        
        for conn in data['network']:
            source = next(q for q in queues if q.name == conn['source'])
            target = next(q for q in queues if q.name == conn['target'])
            probability = conn['probability']

            source.connections.append((target, probability))


        scheduler = Scheduler(queues=queues, randoms=random_generator(data['random_count']))

        for queue_name in data['arrivals']:
            q = next(q for q in queues if q.name == queue_name)
            time = data['arrivals'][queue_name]

            scheduler.schedule(time, ARRIVAL, q)
        
        return scheduler
    
