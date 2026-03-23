"""
Genetic Algorithm works with a population of candidate solutions.
Over generations, better solutions evolve using selection, crossover, and mutation.

1. Population: Set of candidate solutions.
2. Individual (Chromosome): One solution (e.g., N-Queens board).
3. Fitness Function: Measures how good a solution is.
4. Selection: Choose best individuals as parents.
5. Crossover: Combine parents to create children.
6. Mutation: Randomly modify individuals to maintain diversity.

N-Queens Representation:

- State = list of size N
  Example: [1, 3, 0, 2]
  Index = row
  Value = column (ensures one queen per row)

Fitness Function:
- Counts NON-attacking pairs of queens.
- Maximum pairs = n(n-1)/2
- Fitness = non-attacking pairs / total pairs
- Goal: Fitness = 1.0 (perfect solution)

1. Initialize a random population.
2. Evaluate fitness of each individual.
3. Repeat until solution found or max generations reached:
    a. Select best individuals (parents).
    b. Apply crossover to generate new population.
    c. Apply mutation randomly.
    d. Replace old population with new one.
4. Return the best solution found.
"""

# 1. Setup
import random

n = 8
population_size = 10
mutation_rate = 0.1
max_generations = 100

# 2. Fitness Function (fitness = ratio of non-attacking pairs)
def calculate_fitness(individual):
    non_attacking_pairs = 0
    total_pairs = n * (n - 1) // 2
    
    for i in range(n):
        for j in range(i + 1, n):
            if (individual[i] != individual[j] and
                abs(individual[i] - individual[j]) != abs(i - j)):
                non_attacking_pairs += 1
    
    return non_attacking_pairs / total_pairs

# 3. Create Initial Population (generates a valid chromosome (no column duplicates))
def create_random_individual():
    return random.sample(range(n), n)

# 4. Selection (select top 50% individuals)
def select_parents(population, fitness_scores):
    # pair each individual with its fitness                                        
    paired = list(zip(fitness_scores, population))  # [(fitness, individual), ...]
    paired.sort(reverse=True)  

    sorted_population = []
    for fitness, individual in paired:
        sorted_population.append(individual)

    top_half = sorted_population[:len(population)//2]
    return top_half

# 5. Crossover (single-point crossover with duplicate fix)
def crossover(parent1, parent2):
    point = random.randint(1, n - 2)
    child = parent1[:point] + parent2[point:]
    
    # fix duplicates
    missing = list(set(range(n)) - set(child))
    
    for i in range(len(child)):
        if child.count(child[i]) > 1:
            child[i] = missing.pop()
    
    return child 

# 6. Mutation (swap two positions)
def mutate(individual):
    idx1, idx2 = random.sample(range(n), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# 7. Genetic Algorithm
def genetic_algorithm():
    # population
    population = []
    for i in range(population_size):
        population.append(create_random_individual())
    
    for generation in range(max_generations):
        # computing fitness 
        fitness_scores = []
        for ind in population:
            fitness_scores.append(calculate_fitness(ind))

        best_fitness = max(fitness_scores)
        print(f"Generation {generation}, Best Fitness: {best_fitness}")
        if best_fitness == 1.0: break   # stop if perfect solution found
        
        # selection
        parents = select_parents(population, fitness_scores)
        
        # crossover
        new_population = []
        for i in range(population_size):            
            child = crossover(random.choice(parents), random.choice(parents))
            new_population.append(child)

        # mutation
        for i in range(len(new_population)):
            if random.random() < mutation_rate:
                new_population[i] = mutate(new_population[i])
        
        population = new_population
    
    # return best solution in the final population    
    best_individual = None
    best_score = -1

    for individual in population:
        score = calculate_fitness(individual)
        
        if score > best_score:
            best_score = score
            best_individual = individual

    return best_individual, calculate_fitness(best_individual)

solution, fitness = genetic_algorithm()

print("Best Solution:", solution)
print("Best Fitness:", fitness)

"""
STAFF SCHEDULING
- Goal: Assign staff to shifts while minimizing penalties.

Problem Representation:
- Schedule = 2D matrix
  Rows = staff
  Columns = shifts

  schedule[staff][shift] = 1 → assigned
  schedule[staff][shift] = 0 → not assigned

Fitness Function:
- Lower fitness is better (penalty-based)

Penalties:
1. Understaffed shifts:
   - If assigned staff < required → penalty added

2. Consecutive shifts:
   - If a staff works back-to-back shifts → penalty

1. Initialize random population
2. Evaluate fitness (penalty)
3. Repeat for generations:
    a. Select best individuals (lowest penalty)
    b. Apply crossover to create children
    c. Apply mutation randomly
    d. Replace old population
4. Return best schedule (minimum penalty)
"""

# 1. Setup
import random

num_staff = 5
num_shifts = 21  # 7 days × 3 shifts
max_shifts_per_staff = 7
required_staff_per_shift = 2

population_size = 10
mutation_rate = 0.1
max_generations = 100

# 2. Fitness Function (lower fitness = better schedule)
def evaluate_fitness(schedule):
    penalty = 0

    # (1) Check shift coverage
    for shift in range(num_shifts):
        assigned_count = 0
        for staff in range(num_staff):
            assigned_count += schedule[staff][shift]

        
        if assigned_count < required_staff_per_shift:
            penalty += (required_staff_per_shift - assigned_count) * 10

    # (2) Check consecutive shifts
    for staff in range(num_staff):
        for shift in range(num_shifts - 1):
            if schedule[staff][shift] == 1 and schedule[staff][shift + 1] == 1:
                penalty += 5

    return penalty

# 3. Create Random Schedule
def create_random_schedule():    
    schedule = []
    for staff in range(num_staff):
        row = []
        for shift in range(num_shifts):
            row.append(0)
        schedule.append(row)

    for staff in range(num_staff):
        assigned = random.sample(
            range(num_shifts),
            random.randint(3, max_shifts_per_staff)
        )
        for shift in assigned:
            schedule[staff][shift] = 1

    return schedule

# 4. Selection (select top 50% (lowest penalty))
def select_parents(population, fitness_scores):
    paired = list(zip(fitness_scores, population))  # [(fitness, individual), ...]
    paired.sort()  # sort by fitness ascending (lower penalty is better)

    # extract only the individuals
    sorted_population = []
    for fitness, individual in paired:
        sorted_population.append(individual)

    top_half = sorted_population[:len(population)//2]
    return top_half

# 5. Crossover (single-point crossover per staff row)
def crossover(parent1, parent2):
    point = random.randint(0, num_shifts - 1)
    
    child = []
    for i in range(num_staff):
        first_part = parent1[i][:point]
        second_part = parent2[i][point:]
        staff_child = first_part + second_part
        
        child.append(staff_child)
    
    return child

# 6. Mutation (swap two shifts for one staff)
def mutate(schedule):
    staff = random.randint(0, num_staff - 1)
    s1, s2 = random.sample(range(num_shifts), 2)
    
    schedule[staff][s1], schedule[staff][s2] = schedule[staff][s2], schedule[staff][s1]
    
    return schedule

# 7. Genetic Algorithm 
def genetic_algorithm():
    # population
    population = []
    for i in range(population_size):
        population.append(create_random_schedule())

    for generation in range(max_generations):
        # computing fitness
        fitness_scores = []
        for schedule in population:
            fitness_scores.append(evaluate_fitness(schedule))
        
        best_fitness = min(fitness_scores)
        print(f"Generation {generation}, Best Fitness: {best_fitness}")

        # selection
        parents = select_parents(population, fitness_scores)

        # create new population
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)

            if random.random() < mutation_rate:
                child = mutate(child)

            new_population.append(child)

        population = new_population

    # return best schedule in the final population       
    best_schedule = None
    min_score = float('inf')

    for schedule in population:
        score = evaluate_fitness(schedule)

        if score < min_score:
            min_score = score
            best_schedule = schedule

    return best_schedule, min_score

solution, fitness = genetic_algorithm()

print("\nBest Schedule (Staff x Shifts):")
i = 0
for row in solution:
    print(f"Staff {i+1}: {row}")
    i += 1

print("Best Fitness (Penalty):", fitness)