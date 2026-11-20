import random
import textdistance
from utils.Constants import Constants

"""
@author carmelolg
"""

class TextUtils:

    @staticmethod
    def mutation(x):
        """
        Performs a mutation on the given individual by randomly changing one character in its word.
        :param x: Individual object to mutate.
        """
        constants = Constants()
        tmp_word = list(x.word)
        tmp_word[random.randint(0, len(x.word) - 1)] = random.choice(constants.all_chars)
        x.word = "".join(tmp_word)
        x.fitness = TextUtils.fitness(x.word)

    @staticmethod
    def fitness(word) -> int:
        """
        Calculates the fitness of a given word by comparing it to the solution using Hamming distance.
        :param word: The word to evaluate.
        :return: The Hamming distance between the word and the solution.
        """
        constants = Constants()
        return textdistance.hamming(word, constants.solution)

    # Never used in this case
    @staticmethod
    def perform_fitness(x):
        """
        Updates the fitness of an individual based on its word.
        :param x: Individual object whose fitness needs to be updated.
        """
        x.fitness = TextUtils.fitness(x.word)