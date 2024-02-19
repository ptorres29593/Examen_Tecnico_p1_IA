import random

def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_initial_population(number, pop_size, max_offset=100):
    population = []
    for _ in range(pop_size):
        offset = random.randint(-max_offset, max_offset)
        candidate = number + offset
        while not is_prime(candidate):
            offset = random.randint(-max_offset, max_offset)
            candidate = number + offset
        population.append(candidate)
    return population

def fitness(candidate, target):
    return abs(candidate - target)

def elite_selection(population, target, num_parents):
    population.sort(key=lambda x: fitness(x, target))
    return population[:num_parents]

def roulette_wheel_selection(population, target, num_parents):
    total_inverse_fitness = sum(1 / (fitness(candidate, target) + 1) for candidate in population)
    probabilities = [(1 / (fitness(candidate, target) + 1)) / total_inverse_fitness for candidate in population]
    selected_parents = []
    for _ in range(num_parents):
        selected_parent = random.choices(population, probabilities)[0]
        selected_parents.append(selected_parent)
    return selected_parents


def crossover(parents, num_offspring):
    offspring = []
    for _ in range(num_offspring):
        parent1, parent2 = random.sample(parents, 2)
        if len(str(parent1)) <= 1:  
            crossover_point = 0  
        else:
            crossover_point = random.randint(1, len(str(parent1)) - 1)
        child = int(str(parent1)[:crossover_point] + str(parent2)[crossover_point:])
        offspring.append(child)
    return offspring

def mutation(offspring, mutation_rate, max_offset=10):
    mutated_offspring = []
    for child in offspring:
        if random.random() < mutation_rate:
            offset = random.randint(-max_offset, max_offset)
            mutated_child = child + offset
            while not is_prime(mutated_child):
                offset = random.randint(-max_offset, max_offset)
                mutated_child = child + offset
            mutated_offspring.append(mutated_child)
        else:
            mutated_offspring.append(child)
    return mutated_offspring

def evolutionary_algorithm(target, pop_size=100, num_generations=100, num_parents=10, num_offspring=50, mutation_rate=0.1):
    population = generate_initial_population(target, pop_size)
    for generation in range(num_generations):
        parents = roulette_wheel_selection(population, target, num_parents)
        offspring = crossover(parents, num_offspring)
        mutated_offspring = mutation(offspring, mutation_rate)
        population = parents + mutated_offspring
    best_solution = min(population, key=lambda x: fitness(x, target))
    return best_solution

target_number = 999900
nearest_prime = evolutionary_algorithm(target_number)
print(f"The nearest prime number to {target_number} is {nearest_prime}")