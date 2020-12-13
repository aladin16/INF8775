import sys
import numpy as np
import time

load_file = np.loadtxt('./cout_transition.txt', dtype=int)
cout_transition = load_file.reshape((24, 5, 24, 5))

def get_melody_data(path):
    melody = []
    with open(path) as f:
        next(f)
        for line in f: 
            for value in line.split():
                x = int(value)
                melody.append(x)
    return melody

def process_greedy(melody):
    melody_len = len(melody)
    solution = []
    total_cost = 0

    transitions = [cout_transition[melody[0], :, melody[1], :]]
    minimal_cost = np.argmin(transitions)
    d_1 = int(minimal_cost / 5)
    d_2 = minimal_cost - 5 * d_1
    minimal_transition = transitions[0][d_1][d_2]

    solution.append(d_1)
    solution.append(d_2)
    total_cost += minimal_transition

    for k in range(2, melody_len):
        best_finger = np.argmin(cout_transition[melody[k - 1]]
                               [solution[k - 1]][melody[k]])
        minimal_transition = cout_transition[melody[k - 1]][solution[k - 1]][melody[k]][best_finger]

        solution.append(best_finger)
        total_cost += minimal_transition

    return total_cost, solution

def run():
    current_path = sys.argv[2] # Path de l'exemplaire'''
    melody = get_melody_data(current_path)
    
    start = time.time()
    total_cost, solution = process_greedy(melody)
    end = time.time()

    options = sys.argv[1:]
    if '-c' in options: # On imprime les nombres triés    
        print(*solution)
    if '-p' in options: # On imprime les nombres triés    
        print(total_cost)
    if '-t' in options: # On imprime le temps d_1'exécution
        print((end-start)*1000)

if __name__ == '__main__':
    run()
