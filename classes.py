"""
Keeps track of all cards in the game
Implementation: {family: {value: [(potential) owner(s)]}}
"""
class library(object):

    def __init__(self, names):
        """ Initiates an empty library given a list of player names """
        self.lib = {}
        self.names = names

    def addCard(self, family, value, num):
        """ Given a card, checks if it exists and tries to add it if not """

        # add family, if appropriate
        if family not in self.lib:
            if len(self.lib) < num:
                self.lib[family] = {}

                # add value, if appropriate
                if value not in self.lib:
                    if len(self.lib[family]) < num:
                        self.lib[family][value] = self.names
                    else:
                        raise ValueError
            else:
                raise ValueError

    def exists(self, family, value):
        try:
            return (value in self.lib[family])
        except KeyError:
            return False

    def __str__(self):
        res = ""
        for family in self.lib:
            for value in self.lib[family]:
                res += str(value) + " in the family of " + str(family) + " has owners " + str(lib[family][value])
        return res

class newhand(object):
    """
    Keeps track of cards in a player's hand.
    Implementation: {family: [values], None: num}
    """

    def __init__(self):
        """Create a hand with four undefined cards"""
        self.hand = {None : 4}

    def addFamily(self, family):
        """ Given a family, checks if player can ask for it and notes possession """
        if family not in self.hand:
            if None in self.hand:
                self.hand[None] -= 1
                if self.hand[None] == 0:
                    del self.hand[None]
                self.hand[family] = [None]
            else:
                raise ValueError

    def assign_card(self, newcard, new=False):
        done = False
        hand = self.hand
        for i in range(len(hand)):
            card = hand[i]
            if card.value == None and card.samefamily(newcard):
                self.hand[i] = newcard
                done = True
                break
        if not done:
            for i in range(len(hand)):
                card = hand[i]
                if card.undefined():
                    self.hand[i] = newcard
                    done = True
                    break
        if new:
            if done:
                self.hand.append(cardclass(None, None))
            else:
                self.hand.append(card)

    def __str__(self):
        res = ""
        for family in self.hand:
            if family == None:
                res += str(self.hand[family]) + " undefined" + "\n"
            else:
                for value in self.hand[family]:
                    res += str(value) + " in the family of " + str(family)+ "\n"
        return res

    def remove_card(self, card):
        self.hand.remove(card)

    def iswin(self):
        # TODO
        return False
