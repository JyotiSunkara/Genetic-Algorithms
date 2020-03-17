from client_moodle import get_errors, submit
import numpy as np
import random 

'''
1. Randomly initialize populations P
2. Determine fitness of population
3. Until convergence repeat:
      a. Select parents from population
      b. Crossover and generate new population
      c. Perform mutation on new population
      d. Calculate fitness for new population
'''
POPULATION_SIZE = 100

# 1) Idk how we should be 
#   using the fact that the vector given is overfit

class Item(object):

    def __init__(self, chromosome): 
        self.chromosome = chromosome  
        self.fitness = self.calcFitness() 

    '''Target is unknown, but when target is reached 
    fitness must be least, that is zero'''
    def calcFitness(self): 
        error = get_errors('dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC', self.chromosome.tolist())
        '''Returning validation set error as fitness'''
        return error[1] 
        # 2) Idk what we are supposed to do with training set error
   
'''Valid numbers are in the range -10 to 10'''
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
    
    '''List of 100 items where each Item is a vector and its fitness'''
    population = [] 

    for X in range(POPULATION_SIZE):
        genome = Item(create_genome())
        population.append(genome)
    found = False
    while not found and generation != 1499:
        '''Sort by fitness'''
        population = sorted(population, key = lambda x:x.fitness) 

        #3) Not sure if fitness should be equivalent to validation set error and also if error can infact reach 0. Must check.
        if population[0].fitness <= 0:
            found =  True
            break
        
        '''10 percent directly enters new generation'''
        newGeneration = []
        entry = int((10*POPULATION_SIZE)/100) 
        newGeneration.extend(population[:entry])
        
        '''Top 50 percent mates to get new generation'''
        mates = int((90*POPULATION_SIZE)/100) 
        for X in range(mates):
            parentOne = random.choice(population[:50])
            parentTwo = random.choice(population[:50])
            child = mate(parentOne, parentTwo)
            newGeneration.append(child)
        
        population = newGeneration
        generation = generation + 1

    submit_status = submit('dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC', population[0].chromosome.tolist())
    assert "submitted" in submit_status


if __name__ == '__main__':
    main()
    
#4) Idk how to continue learning over all the days we have, as in we should be storing results 
# so that the vector becomes better right? We should probably keep the last population in a file? 
