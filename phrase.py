"""The phrase problem, built on GALib: evolve random strings into a target phrase.

@author carmelolg
"""
from string import ascii_letters

from carmelolg.galib import Problem

DEFAULT_TARGET = 'Happy Birthday Mr. Manu De Leo! from a genetic algorithm to you :-)'
# DEFAULT_TARGET = 'I\'m produced by a genetic algorithm!'
DEFAULT_ALPHABET = ascii_letters + " '!?*&.:;,-()"


class PhraseProblem(Problem[str]):
    """A genome is a string as long as the target; its fitness is the Hamming distance to the target
    (number of wrong characters), so lower is better and 0 means the phrase has been found."""

    maximize = False

    def __init__(self, target: str = DEFAULT_TARGET, alphabet: str = DEFAULT_ALPHABET):
        if not target:
            raise ValueError("the target phrase must not be empty")
        missing = sorted(set(target) - set(alphabet))
        if missing:
            raise ValueError(f"the target contains characters that are not in the alphabet: {''.join(missing)!r}")
        self.target = target
        self.alphabet = alphabet

    def random_genome(self, rng) -> str:
        return "".join(rng.choice(self.alphabet) for _ in self.target)

    def random_gene(self, rng) -> str:
        return rng.choice(self.alphabet)

    def fitness(self, genome: str) -> int:
        return sum(a != b for a, b in zip(genome, self.target, strict=True))
