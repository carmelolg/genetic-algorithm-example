import contextlib
import io
import random
import unittest

from main import build_algorithm, main, parse_args
from phrase import DEFAULT_TARGET, PhraseProblem


class PhraseProblemTests(unittest.TestCase):

    def test_fitness_is_hamming_distance(self):
        problem = PhraseProblem('abcdefgh', alphabet='abcdefghX')
        self.assertEqual(problem.fitness('abcdefgh'), 0)
        self.assertEqual(problem.fitness('abcdefgX'), 1)
        self.assertEqual(problem.fitness('XXXXXXXX'), 8)

    def test_random_genomes_use_the_alphabet_and_target_length(self):
        problem = PhraseProblem('hello', alphabet='helo')
        genome = problem.random_genome(random.Random(0))
        self.assertEqual(len(genome), 5)
        self.assertTrue(set(genome) <= set('helo'))
        self.assertIn(problem.random_gene(random.Random(0)), 'helo')

    def test_target_must_be_reachable(self):
        with self.assertRaises(ValueError):
            PhraseProblem('hello!', alphabet='helo')
        with self.assertRaises(ValueError):
            PhraseProblem('')

    def test_default_target_is_reachable(self):
        PhraseProblem(DEFAULT_TARGET)  # must not raise


class CommandLineTests(unittest.TestCase):

    def run_main(self, *argv):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            result = main(list(argv))
        return result, out.getvalue()

    def test_defaults(self):
        args = parse_args([])
        self.assertEqual(args.solution, DEFAULT_TARGET)
        self.assertEqual(args.population, 1000)
        engine = build_algorithm(args)
        self.assertEqual(engine.population_size, 1000)
        self.assertEqual(engine.max_generations, 50000)

    def test_finds_the_phrase(self):
        result, output = self.run_main('--solution', 'hello world', '--population', '200', '--seed', '42')
        self.assertEqual(result.best.genome, 'hello world')
        self.assertEqual(result.stopped_by, 'TargetFitness')
        self.assertIn("best: 'hello world'", output)

    def test_same_seed_same_run(self):
        first, _ = self.run_main('--solution', 'hello', '--population', '50', '--seed', '7')
        second, _ = self.run_main('--solution', 'hello', '--population', '50', '--seed', '7')
        self.assertEqual([s.best_genome for s in first.history], [s.best_genome for s in second.history])

    def test_stagnation_option(self):
        result, _ = self.run_main('--solution', 'hello', '--population', '4', '--generations', '1000',
                                  '--stagnation', '3', '--mutation-rate', '0', '--seed', '1')
        self.assertIn(result.stopped_by, ('Stagnation', 'TargetFitness'))
        self.assertLess(result.generations, 1000)


if __name__ == '__main__':
    unittest.main()
