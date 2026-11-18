# Genetic Algorithm Example

![Genetic Algorithm Logo](static/logo.svg)

This project evolves a population of random strings towards a target phrase with a genetic algorithm.
It is a small client of [GALib](https://carmelolg.github.io/GALib/), the genetic algorithm library extracted from it
and published on PyPI: the project only describes the problem, the library runs the evolution.

## Features

-   **Problem definition** (`phrase.py`): a genome is a string as long as the target; its fitness is the Hamming distance to the target (number of wrong characters, lower is better).
-   **Evolution** (GALib): tournament selection (size 3 by default), one-point crossover (rate 0.9), per-gene mutation (default probability `1/length`), elitism (the 2 best individuals survive every generation).
-   **Live progress**: one line per generation, updated in place, with best and mean fitness, genetic diversity and the best individual.
-   **Command line options** for the target phrase and the main parameters; reproducible runs with `--seed`; optional plot with `--plot`.

## Requirements

-   Python 3.10+
-   [GALib](https://carmelolg.github.io/GALib/) (`carmelolg-galib` on [PyPI](https://pypi.org/project/carmelolg-galib/)), installed by `requirements.txt`. `--workers` and `--history-every` need a GALib release that includes them.
-   `matplotlib`, only for `--plot`.

## Installation

From the project root:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

| Option | Default | Meaning |
|---|---|---|
| `--solution` | a birthday phrase | target phrase; only letters, spaces and ``'!?*&.:;,-()`` are allowed |
| `--population` | 1000 | population size |
| `--generations` | 50000 | maximum number of generations |
| `--tournament` | 3 | tournament size for parent selection |
| `--mutation-rate` | `1/length` | per-gene mutation probability |
| `--stagnation` | off | stop after N generations without improvement |
| `--seed` | random | seed for reproducible runs |
| `--workers` | off | evaluate each generation with N parallel workers (the phrase is cheap to score, so this is mostly a demo) |
| `--parallel` | `process` | `process` or `thread`, used with `--workers` |
| `--history-every` | 1 | keep the best genome in the history only every N generations (less memory on long runs) |
| `--plot` | off | plot fitness and diversity at the end |

For example:

```bash
python main.py --solution "hello world" --population 500 --seed 42 --plot
```

`--plot` needs `matplotlib` (`pip install matplotlib`). Run the tests with `python -m unittest discover -s tests -t .`.

## Project Structure

-   `phrase.py`: `PhraseProblem`, the GALib `Problem` describing the phrase search, and the default target phrase.
-   `main.py`: the command line entry point; builds the `GeneticAlgorithm` from the options and prints the result.
-   `tests/`: unit tests for the problem and the command line.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License. See the [LICENSE.md](LICENSE.md) file for details.
The GALib library has its own license (Apache-2.0).

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-nd/4.0/)
