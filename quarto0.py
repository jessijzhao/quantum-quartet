from itertools import cycle

def paradox(name):
    print ("Game End: A paradox has been created by {}.".format(name))

class cardclass(object):

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.owners = names

    def getsuit(self):
        return self.suit

    def getvalue(self):
        return self.value

    def getowners(self):
        return self.owners

    def __eq__(self, other):
        """Check equality between two cards."""
        return self.getvalue() == other.getvalue() and self.getsuit() == other.getsuit()

    def samesuit(self, other):
        """Check if two cards belong to the same suit."""
        return self.getsuit() == other.getsuit()

    def undefined(self):
        """Check if a card is completely undefined."""
        return self.getvalue() == None and self.getsuit() == None

    def remove_owner(self, name):
        self.owners.remove(name)

    def set_owner(self, name):
        self.owners = [name]

    def __str__(self):
        return str(self.value) + " in the category of " + str(self.suit)

class playerclass(object):

    def __init__(self, name):
        """Create a hand with four undefined cards"""
        self.name = name
        self.hand = 4 * [cardclass(None, None)]

    def gethand(self):
        return self.hand

    def getname(self):
        return self.name

    def __str__(self):
        res = ""
        for c in self.gethand():
            res.append(c.__str__() + '\n')
        return res

    def add_card(self, card):
        self.hand.append(card)

    def assign_card(self, newcard):
        done = False
        hand = self.gethand()
        for i in range(len(hand)):
            card = hand[i]
            if card.value == None and card.samesuit(newcard):
                self.hand[i] = newcard
                done = True
        if done == False:
            for i in range(len(hand)):
                card = hand[i]
                if card.undefined():
                    self.hand[i] = newcard
                    done = True
        if done == False:
            paradox()

    def remove_card(self, card):
        self.cards.remove(card)

    def iswin(self):
        None


FAMILYSIZE = 4

# pregame:
print("Welcome to Quantum Quarto!")

# get the number of players and their names
num = 1
while num < 3:
    num = int(input("This game requires at least 3 players. Please enter the number of players: "))

players, names, library = [], [], {}

for i in range(num):
    name = input("Please enter Player {}'s name: ".format(i + 1)).lower()
    player = playerclass(name)
    players.append(player)
    names.append(name)

# cycle through the players until win conditions are met or a paradox happens
for player in cycle(players):

    # announce whose turn it is
    nameQ = player.getname().capitalize()
    print ("This is {}'s turn.".format(nameQ))

    # ask questions until person says no
    while True:

        # get a valid name
        while True:
            nameA = input("Who are you asking? ").lower()
            if nameA not in names:
                print ("Not a valid player name.")
            elif nameA == player.getname():
                print("You can't ask yourself.")
            else:
                break

        suit = input("What is the category of the card? ")
        # if all suits have already been defined, and the given suit is not within them
        if suit not in library and len(library) == num:
            pradox(nameQ)
        # add the suit if applicable
        elif len(library) < num:
            library[suit] = []
        # if the player can't ask for this suit due to hand constraints



        value = input("What is the value of the card? ")
        # if all values in this suit have already been defined, and the given value is not within them
        if value not in library[suit] and len(library[suit]) >= FAMILYSIZE:
            pradox(nameQ)
        # add the value to the suit and create the card if applicable
        elif len(library[suit]) < 4:
            library[suit].append(value)
            card = cardclass(value, suit)

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



        # give card to the player
        if response == "y":
            card.set_owner(nameQ)
            # change their hands accordingly



        # if they negated or the player won, stop this player's turn
        if response == "no" or player.iswin():
            break

    # check if win conditions were met
    if player.iswin():
        break




