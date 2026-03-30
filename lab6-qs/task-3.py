"""
Genetic Algorithm for Class Timetable Generation:

Problem:
- Schedule 5 courses taught by 5 teachers over 5 days, 5 time slots per day.
- Constraints:
    1. A teacher cannot teach more than one class at the same time.
    2. Each course must appear exactly 3 times per week.
    3. No teacher should have more than 3 consecutive classes.

Chromosome Representation:
- Each chromosome encodes a complete timetable (5x5)
- Genes represent individual class assignments.

- Repeat for 200 generations.
- Track best timetable and its fitness (lowest penalty).
"""

import random

n = 5   # 5 teachers, 5 courses, 5 days, 5 slots per day
maxGenerations = 200
populationSize = 50
mutationChance = 0.1

def create_individual():
    timetable = []
    for day in range(n):
        dayTimetable = []
        for slot in range(n):
            dayTimetable.append(None)
        timetable.append(dayTimetable)

    nonEmpty = 15
    slotIndices = random.sample(range(n * n), nonEmpty)

    for index in slotIndices:
        day = index // n      
        slot = index % n      
        teacher = random.randint(0, n - 1)
        course = random.randint(0, n - 1)
        timetable[day][slot] = (teacher, course)

    return timetable

def computeFitness(timetable):
    penalty = 0

    # course constraint (exactly 3 times per week)
    courseCount = {}
    for day in timetable:
        for slot in day:
            if slot is None:
                continue
            t, c = slot
            courseCount[c] = courseCount.get(c, 0) + 1

    for c in courseCount:
        penalty += abs(courseCount[c] - 3)

    # no more than 3 consecutive classes constraint
    for day in timetable:
        lastTeacher = None
        streak = 0

        for slot in day:
            if slot is None:
                continue
            t, c = slot

            if t == lastTeacher:
                streak += 1
            else:
                streak = 1

            if streak > 3:
                penalty += 1

            lastTeacher = t

    return penalty

def selectParents(population, fitnessScores):
    paired = list(zip(population, fitnessScores))
    paired.sort(key = lambda x: x[1])

    sortedPopulation = []
    for individual, fitness in paired:
        sortedPopulation.append(individual)

    return sortedPopulation[:len(population) // 2]
    
def crossover(parent1, parent2):
    point = random.randint(1, n - 2)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(timetable):
    day = random.randint(0, n - 1)
    slot = random.randint(0, n - 1)
    t = random.randint(0, n - 1)
    c = random.randint(0, n - 1)

    timetable[day][slot] = (t, c)

    return timetable



def geneticAlgo ():
    # population
    population = []
    for i in range(populationSize):
        population.append(create_individual())

    
    for generation in range(maxGenerations):
        # computing fitness (lesser means better)
        fitnessScores = []
        for i in population:
            fitnessScores.append(computeFitness(i))

        bestFitness = min(fitnessScores)
        print(f"Least Penalty for Generation {generation}: {bestFitness}")
        if  bestFitness == 0: 
            break
        
        # selection
        parents = selectParents(population, fitnessScores)

        # crossover
        newPopulation = []
        for i in range(populationSize):
            child = crossover(random.choice(parents), random.choice(parents))
                    
            # mutation
            if random.random() < mutationChance:
                child = mutate(child)

            newPopulation.append(child)

        population = newPopulation

    bestTimetable = None
    bestPenalty = float('inf')

    for timetable in population:
        if computeFitness(timetable) == 0:
            bestTimetable = timetable
            bestPenalty = 0

    return bestTimetable, bestPenalty

bestTimetable, bestPenalty = geneticAlgo()

if bestTimetable and bestPenalty == 0:
    print(f"\nBest Timetable (Penalty: {bestPenalty}):\n")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    dayIndex = 0
    for day in bestTimetable:
        print(f"{days[dayIndex]}:")
        dayIndex += 1

        slotNumber = 1
        for slot in day:
            if slot is None:
                print(f"  Slot {slotNumber}: Free")
            else:
                teacher, course = slot
                print(f"  Slot {slotNumber}: Teacher {teacher} - Course {course}")
            slotNumber += 1

        print()
else:
    print("No Timetable within the constraints could be found!")