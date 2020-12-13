import sys
import numpy as np
import time
import glouton as greedy
import random

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

def previous_transitions(k, solution, melody, len):
    previous = 0
    if(k > 0):
        previous += cout_transition[melody[k - 1], solution[k - 1], melody[k], solution[k]]
    if(k < len-1):
        previous += cout_transition[melody[k], solution[k], melody[k + 1], solution[k + 1]]
    return previous

def new_transitions(k, d, solution, melody, len):
    new = 0
    if(k > 0):
        new += cout_transition[melody[k - 1], solution[k - 1], melody[k], d]
    if(k < len-1):
        new += cout_transition[melody[k], d, melody[k + 1], solution[k + 1]]
    return new

def process_heuristic(melody, iteration_limit):
    #initialisation avec appel a l'algorithme glouton
    _, solution = greedy.process_greedy(melody)
    n = len(solution)

    interation_counter = 0
    while interation_counter < iteration_limit:
        k = random.randint(0, n-1)
        d = random.randint(0, 4)

        previous = previous_transitions(k, solution, melody, n)  #anciennes transitions 
        new_transition = new_transitions(k, d, solution, melody, n) #nouvelles transitions       

        #verifier si il y a meilleure solution
        if new_transition < previous:
            solution[k] = d

        interation_counter += 1

    total_cost = 0
    for i in range(len(solution) - 1):
        total_cost += cout_transition[melody[i], solution[i], melody[i+1], solution[i+1]]

    return total_cost, solution

def run():
    current_path = sys.argv[2] # Path de l'exemplaire'''
    melody = get_melody_data(current_path)
    
    start = time.time()
    total_cost, solution = process_heuristic(melody, (len(melody)/1000)*100)
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