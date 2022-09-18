import time

m = 2**32
a = 134775813
c = 1

def get_random(x):
    return (a * x + c) % m

def get_randoms(amount=1, seed=int(time.time())):
    x = seed
    randoms = []

    for _ in range(amount):
        next = x / m
        randoms.append(next)
        x = get_random(x)
    
    return randoms
    