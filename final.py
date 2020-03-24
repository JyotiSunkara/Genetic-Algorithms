from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os

POPULATION_SIZE = 40
VECTOR_SIZE = 11
MATING_POOL_SIZE = 15
FILE_NAME_READ = 'JSON/new.json'
FILE_NAME_WRITE = 'JSON/new.json'
first_parent = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]

train_factor = 1
fieldNames = ['Generation','Vector','Train Error','Validation Error', 'Fitness']

def where_json(fileName):
    return os.path.exists(fileName)

def write_json(data, filename=FILE_NAME_WRITE): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent = 4) 

def initial_population():
    first_population = [np.copy(first_parent) for i in range(POPULATION_SIZE)]
    for i in range(POPULATION_SIZE-1):
        index = random.randint(0,10)
        first_population[i][index] = random.uniform(-10,10)

    return first_population

def calculate_fitness(population):
    fitness = np.empty((POPULATION_SIZE, 3))

    for i in range(POPULATION_SIZE):
        error = get_errors(SECRET_KEY, list(population[i]))
        # error = [10000000000, 1000000000]
        fitness[i][0] = error[0]
        fitness[i][1] = error[1]
        fitness[i][2] = error[0]*train_factor + error[1]
        # fitness[i] = 6

    pop_fit = np.column_stack((population, fitness))
    pop_fit = pop_fit[np.argsort(pop_fit[:,-1])]
    return pop_fit

def create_mating_pool(population_fitness):
    population_fitness = population_fitness[np.argsort(population_fitness[:,-1])]
    mating_pool = population_fitness[:MATING_POOL_SIZE]
    return mating_pool

def mutation(child):
    mutation_index = random.randint(0, VECTOR_SIZE-1)
    # if mutation_index < 7:
    #     child[1] = random.uniform(9.5, 10)
    # if mutation_index < 7:
    #     vary = 1 + random.uniform(-0.12, 0.12)
    #     rem = child[mutation_index]*vary
    #     if abs(rem) <= 10:
    #         child[mutation_index] = rem
    vary = 0
    if mutation_index == 1:
        vary = 1 + random.uniform(-0.005, 0)
    
    elif mutation_index == 2:
        vary = 1 + random.uniform(0.01, 0.04)
    
    elif mutation_index == 3:
        vary = 1 + random.uniform(-0.005, 0.005)
    
    elif mutation_index == 4:
        vary = 1 + random.uniform(0.0009, 0.008)

    elif mutation_index == 5:
        vary = 1 + random.uniform(0.009, 0.01)

    elif mutation_index == 6:
        vary = 1 + random.uniform(0, 0.009)

    elif mutation_index == 7:
        vary = 1 + random.uniform(-0.009, 0)

    elif mutation_index == 8:
        vary = 1 + random.uniform(0.0009, 0.009)

    elif mutation_index == 9:
        vary = 1 + random.uniform(-0.009, -0.004)
    
    else:
        vary = 1 + random.uniform(0.0009, 0.001)
    
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
    parents_fitness = parents_fitness[:5]
    children_fitness = children_fitness[:35]
    generation = np.concatenate((parents_fitness, children_fitness))
    generation = generation[np.argsort(generation[:,-1])]
    return generation



def main():
    # population = initial_population()
    # population_fitness = calculate_fitness(population)
    # population_fitness = # LOAD FROM CSV
    # with open('clean_36.json','r+') as f:
    #     population_fitness = np.array(json.loads(f.read())['population'])
    # print(population_and_fitness[0])
    num_generations = 8
    # offset = 0

    if where_json(FILE_NAME_READ):
        with open(FILE_NAME_READ) as json_file:
            data = json.load(json_file)
            population = [dict_item["Vector"] for dict_item in data["Storage"][-40:]]
            train = [dict_item["Train Error"] for dict_item in data["Storage"][-40:]]
            valid = [dict_item["Validation Error"] for dict_item in data["Storage"][-40:]]
            offset = [dict_item["Generation"] for dict_item in data["Storage"][-1:]]
            # fitness = [dict_item["Fitness"] for dict_item in data["Storage"][-100:]]
            # print(fitness)
            # print(train, valid)
            fitness = [(train_factor*train[i] + valid[i]) for i in range(40)]
            population_fitness = np.column_stack((population, train, valid, fitness))
            population_fitness = population_fitness[np.argsort(population_fitness[:,-1])]
            # print(population_fitness[:,-1])
    else:
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
            # print(population[i].tolist())
            # if i == 0 or i == 1:
            #     submit_status = submit(SECRET_KEY, population[i].tolist())
            #     assert "submitted" in submit_status
            with open(FILE_NAME_WRITE) as json_file:
                data = json.load(json_file)
                temporary = data["Storage"]
                # print(i)
                rowDict = { "Generation": generation + 1 + int(list(offset)[0]), 
                            "Vector": population[i].tolist(), 
                            "Train Error": fitness[i][0], 
                            "Validation Error": fitness[i][1],
                            "Fitness": fitness[i][2]}
                temporary.append(rowDict)
            write_json(data)

if __name__ == '__main__':
    main() 