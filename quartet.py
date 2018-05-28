from classes import *
import random

FAMILYSIZE = 4

def main():

    # pregame:
    print("Welcome to Quantum Quarto!")

    # get the number of players and their names
    num = 1
    while num < 3:
        num = int(input("This game requires at least 3 players. Please enter the number of players: "))

    players, library, names = {}, {}, []

    for i in range(num):
        name = input("Please enter Player {}'s name: ".format(i + 1)).lower()
        players[name] = playerclass()
        names.append(name)

    # cycle through the players until win conditions are met or a paradox happens
    playorder = [random.choice(list(players))]
    for nameQ in playorder:

        # announce whose turn it is
        print ("This is {}'s turn.".format(nameQ))

        # ask questions until person says no
        while True:

            # get a valid name
            while True:
                nameA = input("Who are you asking? ").lower()
                if nameA not in players:
                    print ("Not a valid player name.")
                elif nameA == nameQ:
                    print("You can't ask yourself.")
                else:
                    break

            family = input("What is the family of the card? ")
            # if all families have already been defined, and the given family is not within them
            if family not in library and len(library) == num:
                pradox(nameQ)
            # add the family if applicable
            elif len(library) < num:
                library[family] = []
            # if the player can't ask for this family due to hand constraints



            value = input("What is the value of the card? ")
            # if all values in this family have already been defined, and the given value is not one of them
            if value not in library[family] and len(library[family]) >= FAMILYSIZE:
                pradox(nameQ)
            # add the value to the family and create the card if applicable
            elif len(library[family]) < 4:
                library[family].append(value)
                card = cardclass(value, family, names)

            # get the answer of the player that was asked
            while True:
                response = input("{}'s reponse (type y or n): ".format(nameA)).lower()
                if response in ["y", "n"]:
                    break

            # check whether the answer creates a paradox
            if (response == "n" and card.getowners() == [nameA] or
                response == "y" and nameA not in card.getowners()):
                paradox(nameA)

            # remove the askee from list of owners
            if response == "n":
                card.remove_owner(nameA)
                # if only one owner left, assign card to them
                if len(card.getowners()) == 1:
                    hand = players[card.getowners()[0]]
                    hand.assign_card(card)

            # give card to the player who asked
            if response == "y":
                card.set_owner(nameQ)
                # change their hands accordingly
                players[nameQ].add_card(card)
                players[nameA].remove_card(card)

            # if they negated or the player won, stop this player's turn
            if response == "no" or player.iswin():
                break

        # check if win conditions were met
        if player.iswin():
            break


if __name__ == "__main__":
    main()




