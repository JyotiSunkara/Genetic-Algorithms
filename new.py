from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
from csv import DictWriter

POPULATION_SIZE = 100
VECTOR_SIZE = 11
MATING_POOL_SIZE = 20
first_parent = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]

def initial_population():
    first_population = [np.copy(first_parent) for i in range(POPULATION_SIZE)]
    for i in range(POPULATION_SIZE-1):
        index = random.randint(0,10)
        first_population[i][index] = random.uniform(-10,10)

    return first_population

def calculate_fitness(population):
    fitness = np.empty(POPULATION_SIZE)

    j = 100
    for i in range(POPULATION_SIZE):
        # error = get_errors(SECRET_KEY, list(population[i]))
        # fitness[i] = error[0]*0.7 + error[1]
        fitness[i] = j
        j-=1

    pop_fit = np.column_stack((population, fitness))
    pop_fit = pop_fit[np.argsort(pop_fit[:,-1])]
    return pop_fit

def mating_pool(population_fitness):
    mating_pool = population_fitness[:MATING_POOL_SIZE]
    return mating_pool

def mutation(child):
    mutation_index = random.randint(0, VECTOR_SIZE)
    child[mutation_index] = random.uniform(-10,10)
    return child

def crossover(parent1, parent2):
    crossover_point = random.randint(0, VECTOR_SIZE)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def create_children(mating_pool):

    mating_pool = mating_pool[:, :-1]
    children = []
    for i in range(POPULATION_SIZE):
        parent1 = mating_pool[random.randint(0, MATING_POOL_SIZE)]
        parent2 = mating_pool[random.randint(0, MATING_POOL_SIZE)]
        child = crossover(parent1, parent2)
        child = mutation(child)
        children.append(child)

    return children 

def new_generation(parents_fitness, children):
    children_fitness = calculate_fitness(children)
    children_fitness = children_fitness[:80]
    generation = np.concatenate(parents_fitness, children_fitness)
    return generation



def main():
    population = initial_population()
    population_fitness = calculate_fitness(population)

    num_generations = 3
    for generation in range(num_generations):   
        
        mating_pool = mating_pool(population_fitness)
        children = create_children(mating_pool)
        population_fitness = new_generation(mating_pool, children)

if __name__ == '__main__':
    main()