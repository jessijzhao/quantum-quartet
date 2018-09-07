from classes import *
import random
import sys

# the size of any family
FAMILYSIZE = 4

# whether playorder follows a fixed scheme or depends on the asker/askee
FIXED = False

DEBUG = not False

# functions for debugging
def printstate(players, lib):
    for p in players:
        print (p + "'s hand:")
        print (players[p])
    print (lib)


def assignLast(family):
    """ When only few cards have uncertain owners """
    pass


def checkHands(players, family):
    """ Check that there aren't more than FAMILYSIZE cards of a family """
    count = 0
    for p in players:
        try:
            count += players[p].countFamily(family)
        except KeyError:
            pass
    return count <= FAMILYSIZE


def paradox(name):
    """ Called upon creation of paradox by player name """
    print("Player {} created a paradox.".format(name))
    sys.exit()


def main():

    print("Welcome to Quantum Quartet!")

    # get the number of players
    num = 1
    while num < 3:
        try:
            num = int(input("This game requires at least 3 players. Please enter the number of players: "))
        except ValueError:
            print ("Please enter a valid number.")

    # players: {name: hand} / names: [name]
    players, names = {}, []

    # get players' names
    for i in range(num):
        name = ""
        # ensure name isn't empty or a double
        while name == "" or name in names:
            name = input("Please enter Player {}'s name: ".format(i + 1)).lower()
            if name in names:
                print("Names have to be unique. ", end='')
        # initialize hand for each player
        players[name] = playerhand()
        names.append(name)

    # initialize library
    lib = library(names)

    # cycle through the players until win conditions are met or a paradox happens
    playorder = [random.choice(list(players))]

    for nameQ in playorder:

        profile = players[nameQ]

        # ask questions until person says no
        while True:

            # announce whose turn it is
            print ("This is {}'s turn.".format(nameQ))

            # get a valid name
            while True:
                nameA = input("Who are you asking? ").lower()
                if nameA not in players:
                    print ("Not a valid player name.")
                elif nameA == nameQ:
                    print("You can't ask yourself.")
                else:
                    break

            # get card and check if it is valid
            family = input("What is the family of the card? ")
            value = input("What is the value of the card? ")
            try:
                lib.addCard(family, value, num)
                profile.addFamily(family)
            except ValueError:
                paradox(nameQ)

            # checks for too many None cards
            if not checkHands(players, family):
                paradox(nameQ)

            if lib.isFull(family):
                # assign card to person who has a None card (if applicable)
                pass

            if DEBUG:
                printstate(players, lib)

            # get the answer of the player that was asked
            while True:
                response = input("{}'s reponse (type y or n): ".format(nameA)).lower()
                if response in ["y", "n"]:
                    break

            owners = lib.getOwners(family, value)

            # check whether the answer creates a paradox
            if (response == "n" and owners == [nameA] or
                response == "y" and nameA not in owners):
                paradox(nameA)

            # give card to the player who asked
            if response == "y":
                if len(owners) > 1:
                    players[nameA].assignCard(family, value)
                # change their hands accordingly
                players[nameQ].assignCard(family, value, new=True)
                players[nameA].removeCard(family, value)
                lib.setOwner(family, value, [nameQ])

            if response == "n":
                if nameA in owners:
                    # remove the askee from list of potential owners
                    owners.remove(nameA)
                    lib.setOwner(family, value, owners)
                    # if only one owner left, assign card to them
                    if len(owners) == 1:
                        owner = owners[0]
                        players[owner].assignCard(family, value)

            if not checkHands(players, family):
                paradox(nameA)

            if DEBUG:
                printstate(players, lib)

            # if they negated or the player won, stop this player's turn
            if response == "n" or profile.iswin():
                playorder.append(nameA)
                break

        # check if win conditions were met
        if profile.iswin():
            print("Player {} won with the family of {}".format(nameQ, family))
            break


if __name__ == "__main__":
    main()


