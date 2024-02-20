# Main File

# Imports
import math
import random

# Here we declare variables
objective = 200000


# Here we start to write code for the functions

# Function to check if a number is prime or not
def is_prime(num):
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    upper_limit = int(math.sqrt(num) + 1)
    for i in range(3, upper_limit, 2):
        if num % i == 0:
            return False
    return True


# Function to calculate fitness
def fitness(num):
    if is_prime(num):
        return abs(num - objective)
    else:
        return abs(num - objective) + 100000000


# Function to generate a random number
def generate_random_number():
    return random.randint(1, 1000000)


# Function to crossover 2 parent numbers
def crossover(parent1, parent2):
    return random.randint(min(parent1, parent2), max(parent1, parent2))


# Function to mutate numbers
def mutate(num, mutation_rate):
    if random.random() < mutation_rate:
        return abs(random.randint(num - 100000, num + 100000))
    return num


# Function to select parents via roulette
def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    selection_probabilities = [fitness / total_fitness for fitness in fitness_values]
    cumulative_probabilities = [sum(selection_probabilities[:i + 1]) for i in range(len(selection_probabilities))]
    selected_parents = []
    for _ in range(2):
        random_value = random.random()
        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if random_value <= cumulative_probability:
                selected_parents.append(population[i])
                break
    return selected_parents


# Function to select the closest prime number
def elite_selection(population, fitness_values):
    index = 0
    aux = 1000000
    for i, element in enumerate(population):
        if is_prime(element):
            if fitness(element) < aux:
                index = i
                aux = fitness(element)
    if index == 0:
        index = fitness_values.index(min(fitness_values))
    return population[index]


# Function to determine parents via tournament
def tournament_selection(population, fitness_values):
    best = elite_selection(population, fitness_values)
    index = 0
    aux = 0
    for i, element in enumerate(population):
        if is_prime(element):
            if fitness(element) > aux:
                index = i
                aux = fitness(element)
    if index == 0:
        index = fitness_values.index(max(fitness_values))
    worst = population[index]
    return best, worst


# Evolutionary Algorithm
def evolutionary_algorithm(population_size, mutation_rate, max_generations, min_fitness):
    population = [generate_random_number() for _ in range(population_size)]
    generation_number = 1

    for generation in range(max_generations):
        fitness_values = [fitness(num) for num in population]
        if min(fitness_values) < min_fitness:
            index = fitness_values.index(min(fitness_values))
            print("The best number:", population[index])
            print("Fitness value:", fitness_values[index])
            print("Number of generations:", generation_number)
            return population, population[index], generation_number
        new_population = []
        elite = elite_selection(population, fitness_values)
        new_population.append(elite)
        while len(new_population) < round(population_size/3):
            parent1, parent2 = tournament_selection(population, fitness_values)
            child1 = crossover(parent1, parent2)
            new_population.append(mutate(child1, mutation_rate))
        while len(new_population) < round((2/3)*population_size):
            parent3, parent4 = roulette_wheel_selection(population, fitness_values)
            child2 = crossover(parent3, parent4)
            new_population.append(mutate(child2, mutation_rate))
        while len(new_population) < population_size:
            new_population.append(generate_random_number())
        population = new_population
        generation_number += 1
    index = fitness_values.index(min(fitness_values))
    print("The best number:", population[index])
    print("Fitness value:", fitness_values[index])
    print("Number of generations:", generation_number)
    return population, population[index], generation_number

print("Objective:", objective)
evolutionary_algorithm(100, 0.3, 1000, 20)

