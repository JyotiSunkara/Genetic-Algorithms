from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os
import itertools

POPULATION_SIZE = 7
VECTOR_SIZE = 11
MATING_POOL_SIZE = 5
FROM_PARENTS = 3
FILE_NAME_WRITE = 'diagram.json'
overfit_vector = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
first_parent = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

TRAIN_FACTOR = 1
fieldNames = ['Generation','Vector','Train Error','Validation Error', 'Fitness']

def where_json(fileName):
    return os.path.exists(fileName)

def write_json(data, filename = FILE_NAME_WRITE): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent = 4) 

def initial_population():
    first_population = [np.copy(first_parent) for i in range(POPULATION_SIZE)]
    
    for i in range(POPULATION_SIZE):
        for index in range(VECTOR_SIZE):
            vary = 0
            mutation_prob = random.randint(0, 10)
            if mutation_prob < 3:
                vary = 1 + random.uniform(-0.01, 0.01)
                rem = overfit_vector[index]*vary

                if abs(rem) < 10:
                    first_population[i][index] = rem
                elif abs(first_population[i][index]) >= 10:
                    first_population[i][index] = random.uniform(-1,1)

    return first_population

def calculate_fitness(population):
    fitness = np.empty((len(population), 3))

    for i in range(len(population)):
        error = get_errors(SECRET_KEY, list(population[i]))
        # error = [10000000000, 1000000000]
        fitness[i][0] = error[0]
        fitness[i][1] = error[1]
        fitness[i][2] = abs(error[0]*TRAIN_FACTOR + error[1]) 

    pop_fit = np.column_stack((population, fitness))
    pop_fit = pop_fit[np.argsort(pop_fit[:,-1])]
    return pop_fit

def create_mating_pool(population_fitness):
    population_fitness = population_fitness[np.argsort(population_fitness[:,-1])]
    mating_pool = population_fitness[:MATING_POOL_SIZE]
    return mating_pool

def mutation(child):

    for i in range(VECTOR_SIZE):
        mutation_prob = random.randint(0, 10)
        if mutation_prob < 3:
            vary = 1 + random.uniform(-0.7, 0.7)
            rem = child[i]*vary
            if abs(rem) <= 10:
                child[i] = rem
    return child
        

def crossover(parent1, parent2):

    child1 = np.empty(11)
    child2 = np.empty(11)

    u = random.random() 
    n_c = 2
        
    if (u < 0.5):
        beta = (2 * u)**((n_c + 1)**-1)
    else:
        beta = ((2*(1-u))**-1)**((n_c + 1)**-1)


    parent1 = np.array(parent1)
    parent2 = np.array(parent2)
    child1 = 0.5*((1 + beta) * parent1 + (1 - beta) * parent2)
    child2 = 0.5*((1 - beta) * parent1 + (1 + beta) * parent2)

    # print(child1)
    # print(child2)
    # print((parent1 + parent2)/2)
    # print((child1 + child2)/2)

    return child1, child2

def create_children(mating_pool):
    mating_pool = mating_pool[:, :-3]
    children = []
    parents = [[],[]]
    for i in range( int(POPULATION_SIZE/2)):
        parent1 = mating_pool[random.randint(0, MATING_POOL_SIZE-1)]
        parent2 = mating_pool[random.randint(0, MATING_POOL_SIZE-1)]
        child1, child2 = crossover(parent1, parent2)
        
        # child1 = mutation(child1)
        # child2 = mutation(child2)
        parents[0].append(parent1)
        parents[1].append(parent2)
        children.append(child1)
        
        parents[0].append(parent1)
        parents[1].append(parent2)
        children.append(child2)

        parents = np.array(parents).tolist()
        children = np.array(children).tolist()

        

    # print(parents[0])
    # print(parents[1])
    # print(children)
    parents_children = np.column_stack((parents[0], parents[1], children))

    # print()
    # print(parents_children)
    # print()
    # print()
    return parents_children, children 


def new_generation(parents_fitness, children):
    children_fitness = calculate_fitness(children)
    parents_fitness = parents_fitness[:FROM_PARENTS]
    children_fitness = children_fitness[:(POPULATION_SIZE-FROM_PARENTS)]
    generation = np.concatenate((parents_fitness, children_fitness))
    generation = generation[np.argsort(generation[:,-1])]
    return generation

def mutate_children(children):
    for child in children:
        child = mutation(child)
    return children

def main():



    population = initial_population()
    population = np.array(population).tolist()
    population_fitness = calculate_fitness(population)

    num_generations = 10

    data = {"Trace": []}
    outDict = {
        "Generation": 1,
        "Population": population
    }

    # print(population)

    for generation in range(num_generations):   

        mating_pool = create_mating_pool(population_fitness)
        parents_children, children = create_children(mating_pool)
        mutated_children = mutate_children(children)
        # print(len(parents_children))
        # print((len(mutated_children)))
        population_fitness = new_generation(mating_pool, mutated_children)
        # for item in population_fitness:

        fitness = population_fitness[:, -3:] 
        population = population_fitness[:, :-3]      
        # print(population)
        children = np.array(children).tolist()
        mutated_children = np.array(mutated_children).tolist()
        if generation == 0:
            index = 1
            temporary = []
            for (pc, mc) in zip(parents_children, mutated_children):
                firstDict = {}
                firstDict["Child Number"] = index
                firstDict["Parent One"] = pc[:11].tolist()
                firstDict["Parent Two"] = pc[11:22].tolist()
                firstDict["After Crossover"] = pc[-11:].tolist()
                firstDict["After Mutation"] = np.array(mc).tolist()
                index = index + 1

                temporary.append(firstDict)
                # print(temporary)
                # print()
                # print(firstDict)
            outDict["Details"] = temporary
            outDict["Mating Pool"] = mating_pool.tolist()
            outDict["Children"] = children
            outDict["Mutated Children"] = mutated_children
            data["Trace"].append(outDict)
            write_json(data)
            
        else:
            with open(FILE_NAME_WRITE) as writeObj:
                data = json.load(writeObj)
                temporary = data["Trace"]
                rowDict = {
                    "Generation": generation + 1,
                    "Population": population.tolist(),
                }

                holding = []
                index = 1
                for (pc, mc) in zip(parents_children, mutated_children):
                    inDict = {}
                    inDict["Child Number"] = index
                    inDict["Parent One"] = pc[:11].tolist()
                    inDict["Parent Two"] = pc[11:22].tolist()
                    inDict["After Crossover"] = pc[-11:].tolist()
                    inDict["After Mutation"] = np.array(mc).tolist()
                    index = index + 1

                    holding.append(inDict)
                rowDict["Details"] = holding
                rowDict["Mating Pool"] = mating_pool.tolist()
                rowDict["Children"] = children
                rowDict["Mutated Children"] = mutated_children
                temporary.append(rowDict)
            write_json(data)

if __name__ == '__main__':
    main() 