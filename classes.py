
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
