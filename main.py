import random 
#Generar numero al azar entre 1 - 1 millon
def generate_random_number(lower_bound, upper_bound):
    return random.randint(lower_bound, upper_bound)

#Buscar impar mas cercano
def find_nearest_odd(number):
    if number % 2 == 0:
        return number - 1
    else:
        return number

#Mejor aptitud para evaluar la cercania de un numero a otro
def fitness(target, number):
    return abs(target - number)

#Metodo Ruleta
def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    selection_probs = [fitness / total_fitness for fitness in fitness_values]
    selected_individual = random.choices(population, weights=selection_probs)[0]
    return selected_individual
#Metodo Torneo
def tournament_selection(population, fitness_values, tournament_size=3):
    tournament_candidates = random.sample(list(zip(population, fitness_values)), tournament_size)
    winner = min(tournament_candidates, key=lambda x: x[1])
    return winner[0]

#Metodo Elitista
def elitist_selection(population, fitness_values, elite_percentage=0.1):
    elite_size = max(1, int(len(population) * elite_percentage))
    elite_indices = sorted(range(len(fitness_values)), key=lambda x: fitness_values[x])[:elite_size]
    elite_population = [population[i] for i in elite_indices]
    return random.choice(elite_population)

#Crossover (al ser numeros enteros lo que hace es separalos en digitos depende de la cantidad de digitos,
#selecciona un punto para hacer el corte, despues el crossover para al final converitrlos en un valor entero)
def crossover(parent1, parent2):
    
    parent1_digits = [int(digit) for digit in str(parent1)]
    parent2_digits = [int(digit) for digit in str(parent2)]
    
    
    crossover_point = random.randint(1, min(len(parent1_digits), len(parent2_digits)) - 1)
    
    
    child1_digits = parent1_digits[:crossover_point] + parent2_digits[crossover_point:]
    child2_digits = parent2_digits[:crossover_point] + parent1_digits[crossover_point:]
    
    
    child1 = int("".join(map(str, child1_digits)))
    child2 = int("".join(map(str, child2_digits)))
    
    return child1, child2

#Funcion de algoritmo evolutivo
def evolutionary_algorithm(target, population_size, max_generations, selection_method="roulette", mutation_rate=0.2, mutation_function=None):
    population = [generate_random_number(1, 100000) for _ in range(population_size)]
    generations = 0
    while generations < max_generations:
        fitness_values = [fitness(target, find_nearest_odd(individual)) for individual in population]
        if 0 in fitness_values:  # Si ya encontramos un numero impar, terminamos
            index = fitness_values.index(0)
            return find_nearest_odd(population[index])
        
        # Seleccion de  los 3 metodos
        if selection_method == "roulette":
            parent1 = roulette_wheel_selection(population, fitness_values)
            parent2 = roulette_wheel_selection(population, fitness_values)
        elif selection_method == "tournament":
            parent1 = tournament_selection(population, fitness_values)
            parent2 = tournament_selection(population, fitness_values)
        elif selection_method == "elitist":
            parent1 = elitist_selection(population, fitness_values)
            parent2 = elitist_selection(population, fitness_values)
        
        # Crossover
        offspring1, offspring2 = crossover(parent1, parent2)
        
        # Mutacion
        for i in range(len(population)):
            if random.random() < mutation_rate and mutation_function:
                population[i] = mutation_function(population[i])
        
        generations += 1
    
    # Si no encontramos un numero impar en el numero maximo de generaciones, retornamos el mejor candidato encontrado
    best_individual_index = fitness_values.index(min(fitness_values))
    return find_nearest_odd(population[best_individual_index])

# Uso del algoritmo evolutivo
if __name__ == "__main__":
    target_number = generate_random_number(1, 1000000)
    result = evolutionary_algorithm(target_number, population_size=10, max_generations=10, selection_method="roulette")
    print("Numero objetivo:", target_number)
    print("Numero impar mas cercano (ruleta):", result)

    result = evolutionary_algorithm(target_number, population_size=10, max_generations=10, selection_method="tournament")
    print("Numero impar mas cercano (torneo):", result)

    result = evolutionary_algorithm(target_number, population_size=10, max_generations=10, selection_method="elitist")
    print("Numero impar mas cercano (elitista):", result)