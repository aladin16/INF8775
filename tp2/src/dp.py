import sys
import time
import numpy as np

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

def process_dp(melody):
    melody_len = len(melody)
    J = np.zeros((melody_len, 5), dtype = int)
    F = np.zeros((melody_len, 5), dtype = int)
    k = melody_len-2

    while k >= 0:
        for d_1 in range(5):
            fingers_cost = []
            for d_2 in range(5):
                fingers_cost.append(cout_transition[melody[k], d_1, melody[k+1], d_2] + J[k+1][d_2])
            min_cost = np.argmin(fingers_cost)
            F[k][d_1] = min_cost 
            J[k][d_1] = fingers_cost[min_cost]
        k-= 1
    min_cost = np.argmin(J[0])
    total_cost = J[0][min_cost]
    solution = []

    for k in range(melody_len):
        solution.append(min_cost)
        min_cost = F[k][min_cost]

    return total_cost, solution



def run():
    melody_path = sys.argv[2] # Path de l'exemplaire'''
    melody = get_melody_data(melody_path)
    
    start = time.time()
    total_cost, solution = process_dp(melody)
    end = time.time()

    options = sys.argv[1:]
    if '-c' in options: # On imprime les nombres triés    
        print(*solution)
    if '-p' in options: # On imprime les nombres triés    
        print(total_cost)
    if '-t' in options: # On imprime le temps d'exécution
        print((end-start)*1000)


if __name__ == '__main__':
    run()