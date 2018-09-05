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
            else:
                raise ValueError

        # add value, if appropriate
        if value not in self.lib[family]:
            if len(self.lib[family]) < 4:
                self.lib[family][value] = self.names
            else:
                raise ValueError


    def getOwners(self, family, value):
        """ Gets owners of a given card """
        return self.lib[family][value]

    def setOwner(self, family, value, names):
        self.lib[family][value] = names

    def __str__(self):
        res = "library:\n"
        for family in self.lib:
            for value in self.lib[family]:
                res += value + " in the family of " + family + " has owners " + ' '.join(self.lib[family][value]) + "\n"
        return res

class newhand(object):
    """
    Keeps track of cards in a player's hand.
    Implementation: {family: [values], None: int}
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

    def assignCard(self, family, value, new=False):
        """Assigns card to player's hand"""
        if new:
            if family not in self.hand:
                self.hand[family] = [value]
            else:
                self.hand[family].append(value)
        else:
            self.addFamily(family)
            val = self.hand[family]
            if None in val:
                val.remove(None)
                val.append(value)
            elif len(val) < 4 and self.hand[None] > 0:
                val.append(value)
                self.hand[None] -= 1
            else:
                raise ValueError

    def __str__(self):
        res = ""
        for family in self.hand:
            if family == None:
                res += str(self.hand[family]) + " undefined\n"
            else:
                for value in self.hand[family]:
                    res += str(value) + " in the family of " + str(family) + "\n"
        return res

    def removeCard(self, family, value):
        """ Deletes an existing card from hand"""
        self.hand[family].remove(value)

    def iswin(self):
        """ Checks if winnning conditions have been met by player """
        for fam in self.hand:
            if fam != None and len(self.hand[fam]) == 4:
                return True
        return False
