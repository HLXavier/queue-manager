import time
from typing import Iterator

m = 2**32
a = 134775813
c = 1

def get_random(x):
    return (a * x + c) % m

def random_generator(limit: int) -> Iterator[float]:
    x = time.time()
    randoms = []

    for _ in range(limit):
        next = x / m
        randoms.append(next)
        x = get_random(x)
        # print(_)
        yield next
    
def get_randoms(amount=1, seed=int(time.time())):
    x = seed
    randoms = []

    for _ in range(amount):
        next = x / m
        randoms.append(next)
        x = get_random(x)
    
    return randoms
    