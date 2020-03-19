from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
from csv import DictWriter
 
first_parent = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]

def appendDict(fileName, dictElements, fieldNames):
    
    with open(fileName, 'a+', newline='') as writeObj:
        dictWriter = DictWriter(writeObj, fieldnames=fieldNames)
        dictWriter.writerow(dictElements)

fieldNames = ['Generation','Vector','Fitness']
POPULATION_SIZE = 100

class Item(object):

    def __init__(self, chromosome): 
        self.chromosome = chromosome  
        self.fitness = self.calcFitness() 

    def calcFitness(self): 
        error = get_errors(SECRET_KEY, self.chromosome.tolist())
        return error[1] 
   
def create_genome():
    genome = np.random.uniform(-10, 10, size = 11)
    return genome

def mate(A, B):
    child = []
    for a, b in zip(A, B):
        probability = random.random()
        if probability < 0.45:
            child.append(a)
        elif probability < 0.90:
            child.append(b)
        else:
            child.append(random.uniform(-10, 10))
    return child

def main():
    global POPULATION_SIZE
    generation = 1
    
    population = [] 

    for X in range(POPULATION_SIZE):
        genome = Item(create_genome())
        population.append(genome)
    found = False
    while not found and generation != 1499:
        population = sorted(population, key = lambda x:x.fitness) 

        if population[0].fitness <= 0:
            found =  True
            break
        
        newGeneration = []
        entry = int((10*POPULATION_SIZE)/100) 
        newGeneration.extend(population[:entry])
        
        mates = int((90*POPULATION_SIZE)/100) 
        for X in range(mates):
            parentOne = random.choice(population[:50])
            parentTwo = random.choice(population[:50])
            child = mate(parentOne, parentTwo)
            newGeneration.append(child)
        
        population = newGeneration

        rowDict = {'Generation': generation, 'Vector': population[0].chromosome, 'Fitness': population[0].fitness}
        appendDict('store.csv', rowDict, fieldNames)
        generation = generation + 1

    rowDict = {'Generation': generation, 'Vector': population[0].chromosome, 'Fitness': population[0].fitness}
    appendDict('store.csv', rowDict, fieldNames)
    submit_status = submit(SECRET_KEY, population[0].chromosome.tolist())
    assert "submitted" in submit_status


if __name__ == '__main__':
    main()
    
