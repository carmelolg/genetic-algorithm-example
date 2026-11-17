# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Install: `pip install -r requirements.txt` from the repo root. It installs GALib (`carmelolg-galib`) from PyPI, pinned to the 0.2.x series. `matplotlib` is optional, only for `--plot`.
- Run: `python main.py` from the repo root. Prints one line per generation, updated in place, then the result.
- CLI options: `--solution`, `--population`, `--generations`, `--tournament`, `--mutation-rate`, `--stagnation`, `--seed`, `--plot`. See `python main.py -h`.
- Tests: `python -m unittest discover -s tests -t .` (stdlib `unittest`). Single test: `python -m unittest tests.test_operators.CommandLineTests.test_finds_the_phrase`.
- No linter or build configured. The library has its own repository, tooling and docs: https://github.com/carmelolg/GALib (docs at https://carmelolg.github.io/GALib/).

## Architecture

The project is a thin client of GALib (`from carmelolg.galib import ...`):

- `phrase.py`: `PhraseProblem(Problem[str])` with `maximize = False`; fitness is the Hamming distance to the target (0 = found). The constructor rejects targets containing characters outside the alphabet (they could never be reached). `DEFAULT_TARGET` is the default phrase.
- `main.py`: `parse_args` → `build_algorithm` (maps CLI options onto `GeneticAlgorithm`: `TargetFitness(0)` always, `Stagnation` when `--stagnation` is given, `PrintProgress(in_place=True)`) → `main` runs it and returns the `Result`.

Selection, crossover, mutation, elitism, statistics and reproducibility all come from the library: change behaviour through `GeneticAlgorithm` arguments, not by reimplementing operators here.

## Gotchas

- Run commands from the repo root: tests import `main` and `phrase` as top-level modules.
