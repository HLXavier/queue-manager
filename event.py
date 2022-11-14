from q import Queue

class Event:
    def __init__(self, time: float, type: str, target: Queue):
        self.time = time
        self.type = type
        self.target = target
    
    def __str__(self):
        return f'time: {self.time}, type: {self.type}'
        