from classes import *
import random

# the size of any family
FAMILYSIZE = 4
# whether playorder follows a fixed scheme or depends on the asker/askee
FIXED = False

def paradox(name):
    print("Player {} created a paradox.".format(name))

def main():

    print("Welcome to Quantum Quartet!")

    # players: {name: hand} / library: {family: {value: owners}} / names: [name]
    players, library, names = {}, {}, []

    # get the number of players
    num = 1
    while num < 3:
        try:
            num = int(input("This game requires at least 3 players. Please enter the number of players: "))
        except ValueError:
            print ("Please enter a valid number.")

    # get players' names
    for i in range(num):
        name = ""
        # ensure name isn't empty or a double
        while name == "" or name in names:
            name = input("Please enter Player {}'s name: ".format(i + 1)).lower()
            if name in names:
                print("Names have to be unique. ", end='')
        # initialize hand for each player
        players[name] = playerclass()
        # also remember name TODO FIX THIS (names = keys of dict players)
        names.append(name)


    # cycle through the players until win conditions are met or a paradox happens
    # TODO: have two modes for either fixed or flexible order
    playorder = [random.choice(list(players))]

    for nameQ in playorder:

        profile = players[nameQ]

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
                paradox(nameQ)
            # add the family if applicable
            elif len(library) < num:
                library[family] = {}
            # if the player can't ask for this family due to hand constraints
            if not profile.check_family(family):
                paradox(nameQ)

            value = input("What is the value of the card? ")
            # if all values in this family have already been defined, and the given value is not one of them
            if value not in library[family] and len(library[family]) >= FAMILYSIZE:
                paradox(nameQ)
            # add owners and value to family and create card if applicable
            elif len(library[family]) < 4:
                library[family][value] = names
                print(library)
                card = cardclass(value, family)

            # TESTING
            for p in players:
                print (p)
                print (players[p].__str__())

            # get the answer of the player that was asked
            while True:
                response = input("{}'s reponse (type y or n): ".format(nameA)).lower()
                if response in ["y", "n"]:
                    break

            owners = library[family][value]
            # IS THIS MUTABLE? YES

            # check whether the answer creates a paradox
            if (response == "n" and owners == [nameA] or
                response == "y" and nameA not in owners):
                paradox(nameA)

            # remove the askee from list of owners
            if response == "n":
                # if only one owner left, assign card to them
                if len(owners) == 2:
                    owners = nameQ
                    hand = players[nameQ]
                    hand.assign_card(card)
                else:
                    owners.remove(nameA)

            # give card to the player who asked
            if response == "y":
                if len(owners) > 1:
                    players[nameA].assign_card(card)
                owners = nameQ
                # change their hands accordingly
                players[nameQ].assign_card(card, new=True)
                players[nameA].remove_card(card)

            # TESTING
            for p in players:
                print (p)
                print (players[p].__str__())

            # if they negated or the player won, stop this player's turn
            if response == "n" or profile.iswin():
                if FIXED:
                    #TODO
                # the next person to ask is the askee
                else:
                    playorder.append(nameA)
                break

        # check if win conditions were met
        if profile.iswin():
            print("Player {} won with the family of {}".format(nameQ, family))
            break


if __name__ == "__main__":
    main()


