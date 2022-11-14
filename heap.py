from typing import TypeVar, Generic

T = TypeVar('T')

class Heap(Generic[T]):

    def __init__(self):
        self.heap: list[T] = []
        self.size = 0


    def add(self, value: T):
        self.size += 1
        self.heap.append(value)
        self.swim(self.size - 1)


    def poll(self) -> T:
        self.size -= 1
        self.swap(0, self.size) 
        value = self.heap.pop()
        self.sink(0)
        return value

    
    def swim(self, pos):
        if pos <= 0: return
        
        father = self.father(pos)
        if self.less(pos, father):
            self.swap(pos, father)
            self.swim(father)
            

    def sink(self, pos):
        left = self.left(pos)
        right = self.right(pos)
        min = left

        if left >= self.size: return 
        if right < self.size and self.less(right, left): 
            min = right
        
        if self.less(min, pos):
            self.swap(min, pos)
            self.sink(min)

    
    def swap(self, pos1, pos2):
        self.heap[pos1], self.heap[pos2] = self.heap[pos2], self.heap[pos1]
    

    def less(self, pos1, pos2):
        return self.heap[pos1].time < self.heap[pos2].time

    
    def father(self, pos):
        return (pos - 1) // 2


    def left(self, pos):
        return pos * 2 + 1


    def right(self, pos):
        return pos * 2 + 2

    
    def __str__(self):
        return str(self.heap)
