class cardclass(object):

    def __init__(self, value, family):
        self.value = value
        self.family = family

    def getfamily(self):
        return self.family

    def getvalue(self):
        return self.value

    def __eq__(self, other):
        """Check equality between two cards."""
        return self.getvalue() == other.getvalue() and self.getfamily() == other.getfamily()

    def samefamily(self, other):
        """Check if two cards belong to the same family."""
        return self.getfamily() == other.getfamily()

    def undefined(self):
        """Check if a card is completely undefined."""
        return self.getvalue() == None and self.getfamily() == None

    def __str__(self):
        return str(self.value) + " from the family of " + str(self.family)

class playerclass(object):

    def __init__(self):
        """Create a hand with four undefined cards"""
        self.hand = 4 * [cardclass(None, None)]

    def gethand(self):
        return self.hand

    def __str__(self):
        res = ""
        for c in self.gethand():
            res.append(c.__str__() + '\n')
        return res

    def assign_card(self, newcard, new=False):
        done = False
        hand = self.gethand()
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

    def check_family(self, family):
        hand = self.gethand()
        for i in range(len(hand)):
            card = hand[i]
            if card.getfamily() == family:
                return True
        for i in range(len(hand)):
            card = hand[i]
            if card.undefined():
                self.hand[i] = cardclass(None, family)
                return True
        return False

    def remove_card(self, card):
        self.hand.remove(card)

    def iswin(self):
        # TODO
        return False

    def __str__(self):
        res = ""
        for card in self.hand:
            res += card.__str__() + "\n"
        return res
