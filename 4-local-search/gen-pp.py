import random

def convertString (individual):
    idx = 1
    x = 0
    for i in range(5):
        if (individual[i] == '1'):
            x += idx
        
        idx *= 2
    
    return x

def createIndividual(n):
    ind = ""
    for i in range(n):
        ind += str(random.randint(0, 1))
    
    return ind

def computeFitness(individual):
    x = convertString(individual)
    ans = x * x
    ans += x

    return ans

def selectParents(population, fitnessScores):
    paired = list(zip(population, fitnessScores))
    paired.sort(key=lambda x:x[1], reverse=True)

    sorted = []
    for ind in paired:
        sorted.append(ind[0])
    
    return sorted[:popSize // 2]

def crossover(parent1, parent2, n):
    point = random.randint(1, n - 2)
    child = parent1[:point] + parent2[point:]

    return child

def mutate(individual, n):
    idx = random.randint(0, n - 1)
    if individual[idx] == '0':
        individual = individual[:idx] + '1' + individual[idx+1:]
    else:
        individual = individual[:idx] + '0' + individual[idx+1:]

    return individual

n = 5
popSize = 15
maxGenerations = 10
mutateRate = 0.1

def genAlgo ():
    # population
    population = []
    for i in range(popSize):
        population.append(createIndividual(n))

    prevBest = None
    streak = 0
    convergence = False
    for generation in range(maxGenerations):    
        # computing fitness
        fitnessScores = []
        for pop in population:
            fitnessScores.append(computeFitness(pop))

        bestFitness = max(fitnessScores)
        print(f"Maximum f(x) for Generation {generation}: {bestFitness}")
        if bestFitness == prevBest:
            streak += 1
        else:
            streak = 1
            prevBest = bestFitness

        if streak == 4:
            # convergence
            convergence = True
            break

        # selection
        parents = selectParents(population, fitnessScores)

        # crossover
        newPopulation = []
        for i in range(popSize):
            child = crossover(random.choice(parents), random.choice(parents), n)

            # mutation
            if random.random() < mutateRate:
                child = mutate(child, n)

            newPopulation.append(child)
        
        population = newPopulation

    maxValue = float('-inf')
    bestIndividual = None
    
    for ind in population:
        if computeFitness(ind) > maxValue:
            maxValue = computeFitness(ind)
            bestIndividual = ind

    return bestIndividual, maxValue, convergence

solution, maxValue, conv = genAlgo()     
if solution is not None:
    x = convertString(solution)
    if conv:
        print(f"After Convergence - Maximum x Value: {x} - String: {solution}")
    else:
        print(f"After Max Generations - Maximum x Value: {x} - String: {solution}")