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

### Variation One
The fitness corresponding to that vector is calculated as <br>
`Train Error * Train Factor  + Validation Error`

```python
for i in range(POPULATION_SIZE):
    error = get_errors(SECRET_KEY, list(population[i]))
    fitness[i] = error[0]*train_factor + error[1]
```
This was done so that the weight for the validation error would be higher than that for the train error so that the model does not begin to overfit to the training set.

### Variation Two

The fitness corresponding to that vector is calculated as <br>
`Train Error + Validation Error`
```python
for i in range(POPULATION_SIZE):
    error = get_errors(SECRET_KEY, list(population[i]))
    fitness[i] = error[0] + error[1]
```
This was done when the train error became significantly large  indicating that the vectors in the population were no longer overfit to the training set. Hance, the train error is also fully considered to be a part of the  fitness value.

### Variation Three

The fitness corresponding to that vector is calculated as <br>
`| Train Error  - Validation Error |`
```python
for i in range(POPULATION_SIZE):
    error = get_errors(SECRET_KEY, list(population[i]))
    fitness[i] = abs(error[0] - error[1])
```

This is done when the train error and the validation errors became close to each other. This fitness function ensured the selection of vectors that showed the least variation of error between the training and validation sets.

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
    
Then the offsprings are calculated as follows: 

![offsprings](./images/offspring.png)

## Mutation

For the vector, at every index a mutation is decided to be performed with a probability of `3/11`.
Then, the `vary` value is set to be a random float in the range `[-0.01, 0.01] + 1`. Finally, `vary` is multiplied to the float at the chosen index iff the multiplication results in a float within valid range. Else the value at the chosen index is set to a float in the range `[-1, 1]`.

```python
for i in range(VECTOR_SIZE):
    mutation_prob = random.randint(0, 10)
    if mutation_prob < 3:
        vary = 1 + random.uniform(-0.01, 0.01)
        rem = child[i]*vary
        if abs(rem) <= 10:
            child[i] = rem
```
## Heuristics

### Parameters Used/ Changed Whenever Shradha Felt Like It

`POPULATION_SIZE = 30` <br>
`MATING_POOL_SIZE = 10`<br>
`TRAIN_FACTOR = 0.8`<br>
`FROM_PARENTS = 4`<br>
`n_c = 2`<br>
`num_generations = 10`<br>
 
 // Shradha takes over here