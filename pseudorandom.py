import time

m = 2**32
a = 134775813
c = 1

def get_random(x):
    return (a * x + c) % m

def get_randoms(amount=1):
    x = int(time.time())
    randoms = []

    for _ in range(amount):
        next = x / m
        randoms.append(next)
        x = get_random(x)
    
    return randoms
    