# Quantum Quartet

Helper tool for card game "Quantenquartett" (German for "quantum quartet").

Given complete history of actions, will tell players when game ending conditions (i.e. paradox or win) occur.

## Contents

- [rules.md](rules.md) contains the rules for the game

- [quartet.py](quartet.py) runs the game

- [tracker.py](tracker.py) implements representation and manipulation of the game state

- [run_tests.sh](run_tests.sh) runs all tests in [tests](tests)


## Usage

```
usage: quartet.py [-h] (-d | -e) input output
```

Requires Python 3.6+.
