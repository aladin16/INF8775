import sys
import time
import numpy as np

def partition(array, start, end):
    pivot = array[start][1]
    low = start + 1
    high = end

    while True:
        # If the current value we're looking at is larger than the pivot
        # it's in the right place (right side of pivot) and we can move left,
        # to the next element.
        # We also need to make sure we haven't surpassed the low pointer, since that
        # indicates we have already moved all the elements to their correct side of the pivot
        while low <= high and array[high][1] >= pivot:
            high = high - 1

        # Opposite process of the one above
        while low <= high and array[low][1] <= pivot:
            low = low + 1

        # We either found a value for both high and low that is out of order
        # or low is higher than high, in which case we exit the loop
        if low <= high:
            array[low][1], array[high][1] = array[high][1], array[low][1]
            # The loop continues
        else:
            # We exit out of the loop
            break

    array[start][1], array[high][1] = array[high][1], array[start][1]

    return high

def quick_sort(array, start, end):
    if start >= end:
        return

    p = partition(array, start, end)
    quick_sort(array, start, p-1)
    quick_sort(array, p+1, end)  

def get_data(path):
    with open(path, 'r') as file:
        for num_line, lines in enumerate(file.readlines()):
            if num_line == 0:
                nombre_sommets, nombre_infectes = map(
                    int, lines.strip().split(' '))
                matrice_adjacence = np.zeros(
                    (nombre_sommets, nombre_sommets), dtype=bool)
            elif num_line > 0 and num_line <= nombre_sommets:
                # Matrice d'adjacence
                matrice_adjacence[num_line-1] = np.fromiter(map(int, lines.strip().split(' ')), bool)
            else:
                # Sommets infectés
                set_infectes = set(map(int, lines.strip().split(' ')))
                # Sommets non infectés
                set_sains = set(range(nombre_sommets)).difference(set_infectes)
    return matrice_adjacence, set_infectes, set_sains, nombre_sommets 

def forward(matrice_adjacence, set_sains, set_infectes, k, nombre_sommets):
    """Simule une itération de contamination
    """

    # Flag d'atteinte du point fixe
    done = False

    # On mémorise les individus sains et infectés à l'itération précédente
    anciens_infectes = set_infectes.copy()
    anciens_sains = set_sains.copy()
    
    for sommet_sain in anciens_sains:
        nb_voisins_infectes = 0
        for node, is_neighbor in enumerate(matrice_adjacence[sommet_sain]):
            if is_neighbor and node in anciens_infectes:
                nb_voisins_infectes += 1
                if nb_voisins_infectes == k:
                    set_sains.remove(sommet_sain)
                    set_infectes.add(sommet_sain)
                    break

    if len(set_infectes) == len(anciens_infectes):
        done = True

    return set_sains, set_infectes, done

def is_valid(matrice_adjacence, set_sains, set_infectes, k, nombre_sommets): 
    # Propagation
    done = False
    is_valid_solution = True
    while not done:
        set_sains, set_infectes, done = forward(matrice_adjacence, set_sains, set_infectes, k, nombre_sommets)
        # Si plus de la moitié de la population est infectée, la solution est invalide
        if len(set_infectes) > nombre_sommets / 2:
            is_valid_solution = False
    return is_valid_solution

def process_algorithm(matrice_adjacence, set_infectes, set_sains, nombre_sommets, k):
    total_neighbors = []
    removed_elements = []

    for j in set_infectes:
        neighbor_counter = 0
        for i in range(nombre_sommets):
            if matrice_adjacence[j][i] == True:
                neighbor_counter+=1
            if i == nombre_sommets-1:
                total_neighbors.append([j, neighbor_counter])

    quick_sort(total_neighbors, 0, len(set_infectes)-1)
    process_counter = 0
    solution_is_valid = False
    edge_found = False
    edge_connection_with_infected_counter = 0
    
    for neighbor in total_neighbors:
        process_counter +=1
        for i in range(nombre_sommets):
            if matrice_adjacence[neighbor[0]][i] == True:
                for s in set_infectes:
                    if i == s:
                        edge_found = True
                    if matrice_adjacence[s][i] == True:
                        edge_connection_with_infected_counter += 1

                if edge_found: 
                    edge_found = False
                    edge_connection_with_infected_counter = 0

                elif edge_connection_with_infected_counter >= 2:
                    removed_elements.append([(neighbor[0],i), False])
                    matrice_adjacence[i][neighbor[0]] = False       
                    matrice_adjacence[neighbor[0]][i] = False
                    edge_connection_with_infected_counter = 0

                if i%(nombre_sommets/2) == 0:
                    if(is_valid(matrice_adjacence, set_sains.copy(), set_infectes.copy(), k, nombre_sommets)):
                        solution_is_valid = True
                        break

        if solution_is_valid:
            break
    
    for element in removed_elements:
        print(str(element[0][0]) + " " + str(element[0][1]))
    continue_algorithm(removed_elements, matrice_adjacence, set_infectes, set_sains, nombre_sommets, k)

def continue_algorithm(removed_elements, matrice_adjacence, set_infectes, set_sains, nombre_sommets, k):
    removed_elements_copy = removed_elements.copy()

    previous_len = len(removed_elements)
    for element in removed_elements_copy:
        matrice_adjacence[element[0][0]][element[0][1]] = True 
        matrice_adjacence[element[0][1]][element[0][0]] = True
        if(is_valid(matrice_adjacence, set_sains.copy(), set_infectes.copy(), k, nombre_sommets)):
            removed_elements.remove(element)

            if previous_len > len(removed_elements):
                previous_len = len(removed_elements)
                print("")
                for ele in removed_elements:
                    print(str(ele[0][0]) + " " + str(ele[0][1]))
        else: 
            matrice_adjacence[element[0][0]][element[0][1]] = False 
            matrice_adjacence[element[0][1]][element[0][0]] = False

def run():
    path = sys.argv[2] # Path de l'exemplaire'''
    k = sys.argv[4]
    matrice_adjacence, set_infectes, set_sains, nombre_sommets = get_data(path)
    process_algorithm(matrice_adjacence, set_infectes, set_sains, nombre_sommets, int(k))
    
    options = sys.argv[1:]
    if '-p' in options: # On imprime les nombres triés   
        x = 1
if __name__ == '__main__':
    run()