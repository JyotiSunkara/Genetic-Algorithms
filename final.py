from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os

POPULATION_SIZE = 30
VECTOR_SIZE = 11
MATING_POOL_SIZE = 10
FILE_NAME_READ = 'JSON/new.json'
FILE_NAME_WRITE = 'JSON/new.json'
first_parent = [2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                # 0.0000089,
                # 0.12945764086495665,
                # -6.039343877382377,
                # 0.05300478992365601,
                # 0.03633884195379311,
                # 8.039603039599496e-05,
                # -5.9584920882499065e-05,
                # -1.3287444718143218e-07,
                # 3.5467598749854526e-08,
                # 4.406440510633599e-11,
                # -6.9393347593239754e-12


train_factor = 0
fieldNames = ['Generation','Vector','Train Error','Validation Error', 'Fitness']

def where_json(fileName):
    return os.path.exists(fileName)

def write_json(data, filename=FILE_NAME_WRITE): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent = 4) 

def initial_population():
    first_population = [np.copy(first_parent) for i in range(POPULATION_SIZE)]
    for i in range(POPULATION_SIZE):
        index = random.randint(0,10)
        m = random.uniform(0, 0.0006)
        vary = 1 + random.uniform(-m, m)
        rem = first_population[i][index]*vary
        if abs(rem) <= 10:
            first_population[i][index] = rem
        else:
            first_population[i][index] = random.uniform(-1,1)

    return first_population

def calculate_fitness(population):
    fitness = np.empty((POPULATION_SIZE, 3))

    for i in range(POPULATION_SIZE):
        error = get_errors(SECRET_KEY, list(population[i]))
        # error = [10000000000, 1000000000]
        fitness[i][0] = error[0]
        fitness[i][1] = error[1]
        fitness[i][2] = abs(error[0]*train_factor + error[1])
        # fitness[i] = 6

    pop_fit = np.column_stack((population, fitness))
    pop_fit = pop_fit[np.argsort(pop_fit[:,-1])]
    return pop_fit

def create_mating_pool(population_fitness, t, v):
    population_fitness = population_fitness[np.argsort(population_fitness[:,-1])]
    mating_pool = population_fitness[:MATING_POOL_SIZE]
    return mating_pool

def mutation(child):
    mutation_index = random.randint(0, VECTOR_SIZE-1)
    m = random.uniform(0, 0.005)
    vary = 1 + random.uniform(-m, m)
    rem = child[mutation_index]*vary
    if abs(rem) <= 10:
        child[mutation_index] = rem
    return child
    

def crossover(parent1, parent2):

    child = np.empty(VECTOR_SIZE)
    crossover_point = random.randint(0, VECTOR_SIZE)
    child[:crossover_point] = parent1[:crossover_point]
    child[crossover_point:] = parent2[crossover_point:]
    return child

def create_children(mating_pool):
    mating_pool = mating_pool[:, :-3]
    children = []
    for i in range(POPULATION_SIZE):
        parent1 = mating_pool[random.randint(0, MATING_POOL_SIZE-1)]
        parent2 = mating_pool[random.randint(0, MATING_POOL_SIZE-1)]
        child = crossover(parent1, parent2)
        child = mutation(child)
        children.append(child)

    return children 

def new_generation(parents_fitness, children):
    children_fitness = calculate_fitness(children)
    parents_fitness = parents_fitness[:8]
    children_fitness = children_fitness[:22]
    generation = np.concatenate((parents_fitness, children_fitness))
    generation = generation[np.argsort(generation[:,-1])]
    return generation



def main():
    # population = initial_population()
    # population_fitness = calculate_fitness(population)
    # population_fitness = # LOAD FROM CSV

    num_generations = 10
    offset = 0

    if where_json(FILE_NAME_READ):
        with open(FILE_NAME_READ) as json_file:
            data = json.load(json_file)
            population = [dict_item["Vector"] for dict_item in data["Storage"][-40:]]
            train = [dict_item["Train Error"] for dict_item in data["Storage"][-40:]]
            valid = [dict_item["Validation Error"] for dict_item in data["Storage"][-40:]]
            offset = [dict_item["Generation"] for dict_item in data["Storage"][-1:]]
            fitness = [abs(train_factor*train[i] + valid[i]) for i in range(40)]
            population_fitness = np.column_stack((population, train, valid, fitness))
            population_fitness = population_fitness[np.argsort(population_fitness[:,-1])]
    
        data = {"Storage": []}
        with open(FILE_NAME_WRITE, 'w') as writeObj:
            json.dump(data, writeObj)

    for generation in range(num_generations):   

        mating_pool = create_mating_pool(population_fitness)
        children = create_children(mating_pool)
        population_fitness = new_generation(mating_pool, children)

        fitness = population_fitness[:, -3:] 
        population = population_fitness[:, :-3]      
        
        for i in range(POPULATION_SIZE):
            # if i == 0:
            #     submit_status = submit(SECRET_KEY, population[i].tolist())
            #     assert "submitted" in submit_status
            with open(FILE_NAME_WRITE) as json_file:
                data = json.load(json_file)
                temporary = data["Storage"]
                rowDict = { 
                    "Generation": generation + 1 + int(list(offset)[0]), 
                            # "Generation": generation,
                            "Vector": population[i].tolist(), 
                            "Train Error": fitness[i][0], 
                            "Validation Error": fitness[i][1],
                            "Fitness": fitness[i][2]}
                temporary.append(rowDict)
            write_json(data)

if __name__ == '__main__':
    main() 