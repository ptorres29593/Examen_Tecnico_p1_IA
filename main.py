# Main File

# Imports
import math


# Here we declare variables

# Here we start to write code for the functions

# Function to check if a number is prime or not
def is_prime(x):
    if x % 2 == 0:
        return False
    upper_limit = int(math.sqrt(x) + 1)
    for i in range(3, upper_limit, 2):
        if x % i == 0:
            return False
    return True

# Function to calculate fitness

# Function to generate a random number

# Function to crossover 2 parent numbers

# Function to mutate numbers

# Function to select parents via roulette

# Function to select parents via elite specimens

# Evolutionary Algorithm
