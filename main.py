import random

# Define el n�mero objetivo
target_number = int(input("Ingresa el n�mero:"))

# Funci�n para verificar si un n�mero es primo
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Funci�n para generar un n�mero primo aleatorio dentro de un rango espec�fico
def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

# Funci�n para seleccionar dos padres aleatorios
def select_parents(population):
    return random.sample(population, 2)

# Funci�n para ejecutar el algoritmo evolutivo
def evolutionary_algorithm(population_size, max_generations):
    population = [generate_prime(1, 1000000) for _ in range(population_size)]
    generation_number = 0

    while generation_number <= max_generations:
        parents = select_parents(population)
        child1, child2 = parents  # No hay crossover ni mutaci�n, ya que estamos tratando con primos

        # Reemplazar los dos peores individuos de la poblaci�n con los hijos
        population.remove(max(population, key=lambda x: abs(x - target_number)))
        population.remove(max(population, key=lambda x: abs(x - target_number)))
        population.extend([child1, child2])
        
        # Comprobar si se ha encontrado una soluci�n perfecta
        if target_number in population:
            return target_number, generation_number

        generation_number += 1

    # Si no se encuentra una soluci�n perfecta, se devuelve el n�mero primo m�s cercano al objetivo
    return min(population, key=lambda x: abs(x - target_number)), generation_number

# Ejecutar el algoritmo evolutivo
result, generation_number = evolutionary_algorithm(population_size=10, max_generations=100)
print("N�mero primo m�s cercano al", target_number, "encontrado:", result)
print("N�mero de generaciones:", generation_number)