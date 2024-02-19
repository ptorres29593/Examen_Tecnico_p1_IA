import random

class DNA():
    def __init__(self, target, mutation_rate, n_individuals, n_generations):
        # Inicializa los parámetros del algoritmo genético
        self.target = target
        self.mutation_rate = mutation_rate
        self.n_individuals = n_individuals
        self.n_generations = n_generations

    def generate_bit_string(self, length):
        # Genera una cadena de bits aleatoria de la longitud especificada
        return ''.join(random.choice(['0', '1']) for _ in range(length))

    def generate_population(self):
        # Genera la población inicial de cadenas de bits con longitud igual a la del número objetivo
        return [self.generate_bit_string(self.get_binary_length()) for _ in range(self.n_individuals)]

    def get_binary_length(self):
        # Obtiene la longitud de la representación binaria del número objetivo
        return len(bin(self.target)) - 2

    def binary_to_int(self, bit_string):
        # Convierte una cadena de bits a un número entero
        return int(bit_string, 2)

    def fitness(self, bit_string):
        # Calcula la aptitud penalizando más las diferencias alrededor del target
        target_binary = bin(self.target)[2:]
        return sum([abs(int(bit1) - int(bit2)) for bit1, bit2 in zip(bit_string, target_binary)])

    def crossover(self, parent1, parent2):
        # Realiza el cruce entre dos padres para producir dos hijos
        crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, bit_string):
        # Realiza la mutación en la cadena de bits
        mutated_string = ''.join(['1' if random.random() < self.mutation_rate else '0' for _ in range(len(bit_string))])
        return mutated_string

    def roulette_wheel_selection(self, population, fitness_values):
        # Realiza la selección de padres basada en la ruleta
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

    def evolutionary_algorithm(self):
        # Inicializa la población y el número de generaciones
        population = self.generate_population()
        generation_number = 0

        while generation_number < self.n_generations:
            # Calcula la aptitud de cada individuo en la población
            fitness_values = [self.fitness(bit_string) for bit_string in population]

            # Verifica si se ha alcanzado la solución
            if min(fitness_values) == 0:
                index = fitness_values.index(0)
                result_number = self.binary_to_int(population[index])
                return population[index], result_number, generation_number + 1  # Ajuste aquí

            new_population = []

            # Crea la próxima generación
            for _ in range(self.n_individuals // 2):  # Dividir entre 2 para crear parejas de hijos
                selected_parents = self.roulette_wheel_selection(population, fitness_values)
                parent1, parent2 = selected_parents

                # Realiza el cruce y la mutación
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                # Agrega los hijos a la nueva población
                new_population.extend([child1, child2])

            # Actualiza la población para la siguiente generación
            population = new_population
            generation_number += 1

        # Si no se encuentra la solución, devuelve el individuo con menor aptitud
        index = fitness_values.index(min(fitness_values))
        result_number = self.binary_to_int(population[index])
        return population[index], result_number, generation_number or 1  # Modificación aquí


def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def encontrar_primo_cercano(numero):
    if numero < 1 or numero > 1000000:
        return "Por favor, ingrese un número entre 1 y 1,000,000."

    primo_anterior = None
    primo_siguiente = None
    distancia_anterior = float('inf')
    distancia_siguiente = float('inf')

    for i in range(numero - 1, 1, -1):
        if es_primo(i):
            primo_anterior = i
            distancia_anterior = numero - i
            break

    for j in range(numero + 1, 1000001):
        if es_primo(j):
            primo_siguiente = j
            distancia_siguiente = j - numero
            break

    if distancia_anterior <= distancia_siguiente:
        return primo_anterior
    else:
        return primo_siguiente

def main():
    numero_usuario = int(input("Ingrese un número entre 1 y 1,000,000: "))
    target = encontrar_primo_cercano(numero_usuario)

    
    model = DNA(target=target, mutation_rate=0.05, n_individuals=150, n_generations=200)
    result, result_number, generations = model.evolutionary_algorithm()

    
    print(f"Objetivo (primo más cercano): {target}")
    print(f"Resultado encontrado (cadena de bits): {result}")
    print(f"Resultado encontrado (número traducido): {result_number}")
    print(f"Aptitud del resultado: {model.fitness(result)}")
    print(f"Generaciones requeridas: {generations}")

if __name__ == '__main__':
    main()


