from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
from csv import DictWriter

POPULATION_SIZE = 100
VECTOR_SIZE = 11
MATING_POOL_SIZE = 10
first_parent = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]

fieldNames = ['Generation','Vector','Train Error','Validation Error', 'Fitness']

def appendDict(fileName, dictElements, fieldNames):
    
    with open(fileName, 'a+', newline='') as writeObj:
        dictWriter = DictWriter(writeObj, fieldnames=fieldNames)
        dictWriter.writerow(dictElements)

def initial_population():
    first_population = [np.copy(first_parent) for i in range(POPULATION_SIZE)]
    for i in range(POPULATION_SIZE-1):
        index = random.randint(0,10)
        first_population[i][index] = random.uniform(-10,10)

    return first_population

def calculate_fitness(population):
    fitness = np.empty((POPULATION_SIZE, 3))

    for i in range(POPULATION_SIZE):
        # error = get_errors(SECRET_KEY, list(population[i]))
        error = [1, 1]
        fitness[i][0] = error[0]
        fitness[i][1] = error[1]
        fitness[i][2] = error[0]*0.7 + error[1]
        # population_errors[i] = error
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
    child[mutation_index] = random.uniform(-10,10)
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
    children_fitness = children_fitness[:90]
    generation = np.concatenate((parents_fitness, children_fitness))
    return generation



def main():
    population = initial_population()
    population_fitness = calculate_fitness(population)

    num_generations = 40
    for generation in range(num_generations):   
        
        mating_pool = create_mating_pool(population_fitness)
        children = create_children(mating_pool)
        population_fitness = new_generation(mating_pool, children)
        
        fitness = population_fitness[:, -3:] 
        population = population_fitness[:, :-3]

        for i in range(POPULATION_SIZE):
            if i == 0 or i == 1 or i == 2:
                submit_status = submit(SECRET_KEY, population[i])
                assert "submitted" in submit_status

            rowDict = {'Generation': generation, 'Vector': population[i], 'Train Error': fitness[i][0], 'Validation Error': fitness[i][1] ,'Fitness': fitness[i][2]}
            appendDict('lmao.csv', rowDict, fieldNames)

if __name__ == '__main__':
    main()