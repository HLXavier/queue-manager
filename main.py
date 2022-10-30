from simple_queue import SimpleQueue 
from base_queue import Queue
from sys import argv
import json
from tabulate import tabulate

if len(argv) < 2:
    print('Missing setup json argument')

file = open(argv[1], 'r')
setup = json.load(file)

executions = len(setup["seeds"])

def element_wise_sum(a, b):
    return [sum(x) for x in zip(a, b)]

accumulated_state_durations = [0 for _ in range(setup["capacity"] + 1)]
accumulated_probabilities = [0 for _ in range(setup["capacity"] + 1)]
accumulated_losses = 0

for i in range(executions):
    base = Queue(setup["servers"], setup["capacity"], setup["arrival"], setup["departure"],)
    queue = SimpleQueue(base, seed=setup["seeds"][i], first_arrival=setup["first"], rounds=setup["rounds"])
    queue.simulate()
    queue.generate_table()
    state_durations, probs, losses = queue.get_results()

    accumulated_state_durations = element_wise_sum(state_durations, accumulated_state_durations)
    accumulated_probabilities = element_wise_sum(probs, accumulated_probabilities)
    accumulated_losses += losses

avg_state_durations = [acc_duration / executions for acc_duration in accumulated_state_durations]
avg_probabilities = [acc_prob / executions for acc_prob in accumulated_probabilities]
avg_losses = accumulated_losses / executions


state_names = [i for i in range(len(avg_state_durations) + 1)]

table = list(zip(state_names, avg_state_durations, avg_probabilities))

print('Settings:')
print(json.dumps(setup, indent=2))

print('\nResults:')
print(tabulate(table, headers=['State', 'Avg time', 'Avg probability'], floatfmt='0.2f'))
print(f'Avg losses: {avg_losses}')
