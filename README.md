# Genetic-Algorithms
Given coefficients of features corresponding to an overfit model the task is to apply genetic algorithms in order to reduce the overfitting.

## Summary

- Initialize a population
- Determine fitness of population
- Until convergence repeat the following:
    - Select parents from the population
    - Crossover to generate children vectors
    - Generate new population
    - Perform mutation on new population
    - Calculate fitness for new population

Each population contains multiple individuals where each individual represents a point in search space and possible solution.

Every individual is a vector of size `11` with `11` floating point values in the range of `[-10, 10]`

### Selection 
The idea is to give preference to the individuals with good fitness scores and allow them to pass there genes to the successive populations.

### Crossover 
This represents mating between individuals to generate new individuals. Two individuals are selected using selection operator and combined in some way to generate children individuals

### Mutation
The idea is to insert random genes in offspring to maintain the diversity in population to avoid the premature convergence. 

### Algorithm Used

The first population is created using the following vector: 

```python
first_parent = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```

`POPULATION_SIZE` copies of this vector are made. All of these vectors are mutated to generate a population.

For each vector, at every index a mutation is decided to be performed with a probability of `3/11`.
Then, the `vary` value is set to be a random float in the range `[-0.01, 0.01] + 1`. Finally, `vary` is multiplied to the float at the chosen index iff the multiplication results in a float within valid range. Else the value at the chosen index is set to a float in the range `[-1, 1]`

```python
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
```

The fitness of the population is an arithmetic combination of the train error and the validation error.

The mating pool is selected from the population by sorting the population based on its fitness and then selecting `MATING_POOL_SIZE` number of vectors from the top

```python
population_fitness = population_fitness[np.argsort(population_fitness[:,-1])]
mating_pool = population_fitness[:MATING_POOL_SIZE]
return mating_pool
```

The new population is created by choosing `X` top children generated and `POPULATION_SIZE - X` top parents.

```python
children_fitness = calculate_fitness(children)
parents_fitness = parents_fitness[:4]
children_fitness = children_fitness[:26]
generation = np.concatenate((parents_fitness, children_fitness))
generation = generation[np.argsort(generation[:,-1])]
```

## Diagram
// Add diagram

## Fitness
In the fitness function, `get_errors` requests are sent to obtain the train error and validation error for every vector in the population.

The fitness corresponding to that vector is calculated as <br>
`absolute value of 'Train Error * Train Factor  + Validation Error'`

```python
for i in range(POPULATION_SIZE):
    error = get_errors(SECRET_KEY, list(population[i]))
    fitness[i] = abs(error[0]*train_factor + error[1])
```
We changed the value of the `train_factor` from time to time, depending on what our train and validation errors were for that population. This helped us achieve a balance between the train and validation error which were initially very skewed. We kept changing between the following 3 functions according to the requirement of the population (reason for each function mentioned below).
 
### Train factor = 0.7

We started out with `train_factor = 0.7`. This was done to <b>get rid of the overfit </b> as the initial vector had very low train error and more validation error. With our fitness function, we associated less weight to the train error and more to validation error, forcing validation error to reduce yet not allowing train error to shoot up. We also changed it to values <b> 0.6 and 0.5 </b> in the middle to get rid of the overfit faster. <b>0.7</b>, however, worked best as it did not cause train error to rise up suddenly, unlike its lower values.

### Train factor = 1

The fitness function now became a simple sum of train and validation error. <br>
This was done when the train error became significantly large. At this point, we wanted to balance both errors and wanted them to reduce simultaneously so we set the fitness function as their simple sum. 

### Train factor = -1

This was done when the train error and the validation errors each reduced significantly. However the difference between them was still large, despite their sum being small.
So we made the fitness function the absolute difference between the train and validation error. This was done so that the errors would reach a similar value (and hence, generalize well on an unseen dataset).
This function ensured the selection of vectors that showed the least variation of error between the training and validation sets.

## Crossover

### Simulated Binary Crossover

To generate each vector in the new population, two parents are randomly chosen from the mating pool using `random.randint()`. These parents undergo crossover to generate two children. The child vectors are then mutated before appending to the new population.

```python
for i in range( int(POPULATION_SIZE/2)):
    parent1 = mating_pool[random.randint(0, MATING_POOL_SIZE-1)]
    parent2 = mating_pool[random.randint(0, MATING_POOL_SIZE-1)]
    child1, child2 = crossover(parent1, parent2)
```
The entire idea behind simulated binary crossover is to generate two children from two parents, satisfying the following equation. All the while, being able to control the variation between the parents and children using the distribution index value.

<div style="text-align:center;"><img src =./images/logic.png></div>

The crossover is done by choosing a random number in the range `[0, 1)`. The distribution index is assigned its value and then $\beta$ is calculated as follows:

![beta](./images/beta.png)

Distribution index that determines how far children go from parents. The greater its value the closer the children are to parents. The distribution index is a value between `[2, 5]`.

The offsprings are calculated as follows: 

![offsprings](./images/offspring.png)

## Mutation

> Our mutations are probabilistic in nature
For the vector, at every index a mutation is decided to be performed with a probability of `3/11`.
We scale the value at an index by randomly choosing a value between (0.99, 1.01) iff the value after scaling is within the valid (-10, 10) range. The following code does that:

```python
for i in range(VECTOR_SIZE):
    mutation_prob = random.randint(0, 10)
    if mutation_prob < 3:
        vary = 1 + random.uniform(-0.01, 0.01)
        rem = child[i]*vary
        if abs(rem) <= 10:
            child[i] = rem
```

- We chose to scale by a value close to 1 as random mutations such as setting an index to any value between (-10, 10) was not working well. We theorize this is because the overfit vector is close to good results but has just overfit on the training data. Thus, tweaking it slightly gives us improved results. 

- However, we did change these mutations as per the trend of the previous populations. If we observed the errors were not reducing significantly over generations, we increased the mutations to factors such as `1 + random.uniform(-0.1, 0.1)` and `1 + random.uniform(-0.5, 0.5)`. We would experimentally observe which helped us get out of local minimas.

- Sometimes, we even decreased the mutations futher, to reach a finer granularity of our genes. We did this when we were confident we had good vectors that needed more fine tuning. We set the scaling factors between `1 + random.uniform(-0.001, 0.001)` and `1 + random.uniform(-0.007, 0.007)` and experimentally observed which worked best.



## Hyperparameters

### Population size  

The `POPULATION_SIZE` parameter is set to 30.
We initially started out with `POPULATION_SIZE = 100` as we wanted to have sufficient variations in our code. But, we realized that was slowing down the GA and wasting a lot of requests as most of the vectors in a population went unusued. We applied trial and error and found 30 to be the optimal population size where the diversity of population was still maintained.

### Mating pool size

The `MATING_POOL_SIZE` variable is changed between values of 10 and 20. 
We sort the parents by the fitness value and choose the top X (where X varies between 10 to 20 as we set it) that are selected for the mating pool. 

- In case we get lucky or we observe only a few vectors of the population have a good fitness value, we decrease the mating pool size so that we can limit our children to be formed from these high fitness chromosomes only. Also, when we observer that our GA is performing well and do not want unnecessary variations, we limit the mating pool size. 

- When we find our vectors to be stagnating, we increase the mating pool size so that more variations are included in the population as the set of possible parents increases.

### Number of parents passed down to new generation

We varied this variable from 5 to 15. 
- We kept the value small when we were just starting out and were reliant on more variations in the children to get out of the overfit. We did not want to forcefully bring down more parents as that would waste a considerable size of the new population.

- When we were unsure of how our mutations and crossover were performing or when we would change their parameters, we would increase this variable to 15. We did this so that even if things go wrong, our good vectors are still retained in the new generations. This would save us the labour of manually deleting generations in case things go wrong as if there is no improvement by our changes, the best parents from above generations would still be retained and used for mating. 

### Distribution index = 2 to 5

This parameter was applied in the `Simulated Binary Crossover`. It determines how far children go from parents. The greater its value the closer the children are to parents. It varies from 2 to 5.
We changed the Distribution Index value depending on our need. When we felt our vectors were stagnating and needed variation, we changed the value to <b>2, so that the children would have significant variations from their parents</b>. When we saw the errors decreasing steadily, we kept the index as <b>5 so that children would be similar to the parent population, and not too far away</b>.

### Mutation Range 

We varied our mutation range drastically throughout the assignment. 
- We made the variation as little as between factors of (0.997, 1.003) for when we had to fine tune our vectors. We did this when we were confident we had a good vector and excessive mutations were not helping. So we tried mall variations, to get its best features.

- When our vectors would stagnate and reach a local minima - we would mutate extensively to get out of the minima. The factor for multiplication could vary anywhere from (0.9, 1.1) to (0.3, 1.7). 
- We would even assign random numbers at times to make drastic changed when no improvement was shown by the vectors.
- Exact details as to how we did this can be found in the `Mutation` section. 

Exact details are mention in the 'Mutation' section above.

### Cut off range


## Number of iterations to converge 

## Heuristics 

We noticed 