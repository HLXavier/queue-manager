from pseudorandom import random_generator

randoms = random_generator(100000)



def get_random(time_range: tuple[float, float]):
    start, end = time_range
    random = next(randoms)
    return round((end - start) * random + start, 4)

connections = [(0, 0.4), (1, 0.1)]

def next_conn():
    rand = get_random((0, 1))
    acc_prob = 0
    for i in range(len(connections)):
        queue, prob = connections[i]
        if rand >= acc_prob and rand <= acc_prob + prob:
            return queue
        
        acc_prob += prob
    
    return 2


counts = [0, 0, 0]

for _ in range(10000):
    selected: int = next_conn()
    counts[selected] += 1

print(counts[0] / 10000)
print(counts[1] / 10000)
print(counts[2] / 10000)