class Event:
    def __init__(self, time, type):
        self.time = time
        self.type = type 
    
    def __str__(self):
        return f'time: {self.time}, type: {self.type}'
        