#!/usr/bin/env python3

"""
Author: jessijzhao
Date: February 28, 2021

Implements the game Quantenquartett.
"""

import argparse

from tracker import StateTracker
from utils import Actions, ActionType


def resolve(code: int, player: str) -> bool:
    """
    Args:
        code: whether the action is valid, results in a win, or paradox
        player: name of the responsible player

    Returns:
        - True if the game continues
        - False if the game ends.

    Prints a message if needed.
    """
    if code == ActionType.VALID:
        return True
    elif code == ActionType.WIN:
        print(f"\n{player} won the game.")
        return False
    else:
        assert code == ActionType.LOSS
        print(f"\n{player} created a paradox.")
        return False


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "names",
        nargs="+",
        type=str,
        help="player names",
        metavar="names",
    )
    parser.add_argument(
        "-f",
        "--familysize",
        nargs="?",
        default=4,
        type=int,
        help="number of cards in each family",
    )
    args = parser.parse_args()

    print("Welcome to Quantum Quartet!")

    # check validity of provided player names
    names = [name.lower() for name in args.names]
    if len(names) < 3:
        print("This game requires at least three players.")
        quit()
    elif len(set(names)) < 3:
        print("Names must be unique (capitalization notwithstanding).")
        quit()

    # initialize the game state tracker
    state = StateTracker(names, args.familysize)

    # set the starting player
    while True:
        player_1 = input("Who goes first? ").lower()
        if player_1 in names:
            break

    while True:

        print(f"This is {player_1}'s turn.")

        while True:
            player_2 = input("Who are you asking? ").lower()
            if player_2 in names and player_2 != player_1:
                break

        family = input("What is the family of the card? ")
        value = input("What is the value of the card? ")
        code = state.update_state(player_1, player_2, family, value, Actions.QUESTION)
        if not resolve(*code):
            quit()

        while True:
            response = input(f"{player_2}'s reponse (y/n): ").lower()
            if response in (Actions.POSITIVE, Actions.NEGATIVE):
                break

        code = state.update_state(player_1, player_2, family, value, response)
        if not resolve(*code):
            quit()

        if response == "n":
            player_1 = player_2


if __name__ == "__main__":
    main()
