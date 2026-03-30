# You are tasked with finding the maximum value of the function f(x)=x²-3x+4, where x is an integer between 0 and 15. 
# To solve this, you decide to implement a Genetic Algorithm (GA). 
# The algorithm will represent potential values of x as binary chromosomes of 4 bits
# It will maintain a population of 4 individuals.   
#     Encode a random initial population of 4 chromosomes in binary form. 
#     Decode each chromosome into its decimal value and compute its fitness using the function f(x). 
#     Perform one round of selection, crossover, mutation (probability of 0.1) 
#     Identify the best chromosome after this generation and provide its decimal value and fitness.

n = 4
mutateRate = 0.1

import random

def convertX (ind):
    return int(ind, 2)

def createIndividual():
    ind = ""
    for i in range(n):
        ind += str(random.randint(0,1))
    return ind

def computeFitness(ind):
    x = convertX(ind)
    res = x*x
    res -= 3*x
    res += 4
    return res

def selectParents(population, fitness):
    paired = list(zip(population, fitness))
    paired.sort(key=lambda x:x[1], reverse=True)

    sorted = []
    for ind, _ in paired:
        sorted.append(ind)
    
    return sorted[:n // 2]

def crossover(parent1, parent2):
    point = random.randint(1, n - 2)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(child):
    idx = random.randint(0, n - 1)
    if child[idx] == '1':
        return child[:idx] + '0' + child[idx+1:] 
    else: 
        return child[:idx] + '1' + child[idx+1:] 

def geneticAlgo ():
    # population
    population = []
    for i in range(n):
        population.append(createIndividual())

    # computing fitness 
    fitnessScores = []
    for ind in population:
        fitnessScores.append(computeFitness(ind))


    # selection
    parents = selectParents(population, fitnessScores)

    # crossover
    newPopulation = []
    for i in range(n):
        child = crossover(random.choice(parents), random.choice(parents))

        # mutation
        if random.random() < 0.1:
            child = mutate(child)
        
        newPopulation.append(child)
    
    population = newPopulation

    bestChromosome = None
    bestFitness = float('-inf')

    for ind in population:
        if computeFitness(ind) > bestFitness:
            bestChromosome = ind
            bestFitness = computeFitness(ind)
    
    return bestChromosome, bestFitness

sol, f = geneticAlgo()
x = convertX(sol)
print(f"Best chromosome: {sol}  Decimal Value: {x}  Fitness Value: {f}")