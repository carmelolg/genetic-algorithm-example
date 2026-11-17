"""Command line entry point: evolves random strings towards a target phrase with galib.

@author carmelolg
"""
import argparse

from carmelolg.galib import GeneticAlgorithm, PrintProgress, Result, Stagnation, TargetFitness
from carmelolg.galib.operators import Tournament

from phrase import DEFAULT_TARGET, PhraseProblem


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Genetic algorithm that evolves random strings towards a target phrase.')
    p.add_argument('--solution', default=DEFAULT_TARGET, help='target phrase')
    p.add_argument('--population', type=int, default=1000, help='population size')
    p.add_argument('--generations', type=int, default=50000, help='maximum number of generations')
    p.add_argument('--tournament', type=int, default=3, help='tournament size for parent selection')
    p.add_argument('--mutation-rate', type=float, default=None, help='per-gene mutation probability (default: 1/length)')
    p.add_argument('--stagnation', type=int, default=None, help='stop after N generations without improvement')
    p.add_argument('--seed', type=int, default=None, help='random seed for reproducible runs')
    p.add_argument('--plot', action='store_true', help='plot fitness and diversity at the end (needs matplotlib)')
    return p.parse_args(argv)


def build_algorithm(args: argparse.Namespace) -> GeneticAlgorithm:
    problem = PhraseProblem(args.solution)
    stop = [TargetFitness(0)]
    if args.stagnation is not None:
        stop.append(Stagnation(args.stagnation))
    return GeneticAlgorithm(
        problem,
        population_size=args.population,
        max_generations=args.generations,
        selection=Tournament(args.tournament),
        mutation_rate=args.mutation_rate,
        stop=stop,
        callbacks=[PrintProgress(in_place=True)],
        seed=args.seed,
    )


def main(argv=None) -> Result:
    args = parse_args(argv)
    result = build_algorithm(args).run()
    print(f'best: {result.best.genome!r} ({result.best.fitness:g} wrong characters) '
          f'after {result.generations} generations, stopped by {result.stopped_by}')
    if args.plot:
        from carmelolg.galib.plot import plot_history
        plot_history(result)
    return result


if __name__ == '__main__':
    main()
