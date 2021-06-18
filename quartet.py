#!/usr/bin/env python3

"""
Author: jessijzhao
Date: February 28, 2021

Implements the game Quantenquartett.
"""

import argparse
import random

from tracker import StateTracker


def resolve(code):
    """
    code: tuple representing the result of the action and the responsible player
          - 0 represents a valid action without a win
          - 1 represents a win
          - 2 represents a paradox


    Returns 1 if the game continues, 0 if the game ends. Prints a message if needed.
    """
    code, player = code

    assert(code in (0, 1, 2))

    if code == 0:
        return 1
    elif code == 1:
        print(f"\n{player} won the game.")
        return 0
    else:
        print(f"\n{player} created a paradox.")
        return 0


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('names', metavar='names', type=str, nargs='+',
                        help='player names')
    parser.add_argument('-f', '--familysize', nargs='?', type=int, default=4,
                        help='number of cards in each family')
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

        print (f"This is {player_1}'s turn.")

        while True:
            player_2 = input("Who are you asking? ").lower()
            if player_2 in names and player_2 != player_1:
                break

        family = input("What is the family of the card? ")
        value = input("What is the value of the card? ")
        code = state.update_state(player_1, player_2, family, value, 'q')
        if not resolve(code):
            quit()

        while True:
            response = input(f"{player_2}'s reponse (y/n): ").lower()
            if response in ('y', 'n'):
                break

        code = state.update_state(player_1, player_2, family, value, response)
        if not resolve(code):
            quit()

        if response == 'n':
            player_1 = player_2

if __name__ == '__main__':
    main()
