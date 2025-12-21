import random
from string import ascii_letters
from utils.Constants import Constants
from utils.TextUtils import TextUtils
from model.Individual import Individual

"""
This class represents a population of individuals for a genetic algorithm.
It includes methods for generating the population, calculating fitness, performing crossover, and natural selection.
@author carmelolg
"""

class Population:
    population = []
    constants = Constants()

    def get_population(self) -> map:
        """
        Returns the current population of individuals.
        :return: List of Individual objects representing the population.
        """
        return self.population

    # Never used in this case
    def population_fitness(self):
        """
        Updates the fitness of all individuals in the population.
        """
        self.population = map(lambda x: TextUtils.perform_fitness(x), self.population)

    def sort(self):
        """
        Sorts the population based on fitness in ascending order.
        """
        self.population.sort(key=lambda x: x.fitness)

    def generate(self, n):
        """
        Generates a random population of individuals.
        :param n: Number of individuals to generate.
        """
        for i in range(n):
            word_generated = ''
            for j in range(self.constants.max_length):
                word_generated = word_generated + random.choice(ascii_letters + ' ')
            self.population.append(Individual(word_generated, TextUtils.fitness(word_generated)))

    def crossover(self, x, y) -> Individual:
        """
        Performs crossover between two individuals to create a new individual.
        :param x: First parent Individual.
        :param y: Second parent Individual.
        :return: New Individual created from the crossover of x and y.
        """
        word_x = x.word
        word_y = y.word
        half = int(self.constants.max_length / 2)

        new = word_x[:half] + word_y[half:]

        return Individual(new, TextUtils.fitness(new))

    def natural_selection(self):
        """
        Performs natural selection by retaining only the fittest individuals in the population.
        """
        self.sort()
        self.population = self.population[:self.constants.population_number]
