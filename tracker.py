"""
Author: jessijzhao
Date: February 28, 2021

Classes to track the game state in Quantenquartett.
"""

import numpy as np
import pandas as pd


class StateTracker:

    def __init__(self, names, familysize):
        self._names = names
        self._cards = []
        self._fsize = familysize
        self._tracker = Tracker(len(names), familysize)

    def update_state(self, p1, p2, fam, val, action):
        """
        p1: id of the player who asks
        p2: id of the player who responds
        fam: family of the card
        val: value of the card
        action: either asking (q), responding yes (y), or no (n)

        Returns the exit code and updates the game state and list of cards.
        """
        if (fam, val) not in self._cards:
            try:
                index = self._cards.index((fam, None))
                self._cards[index] = (fam, val)
            except ValueError:
                self._cards.append((fam, val))
                self._cards += [(fam, None) for i in range(self._fsize-1)]

            families, _ = list(zip(*self._cards))
            if (len(set(families)) > len(self._names) or
                    families.count(fam) > self._fsize):
                return (2, p1)

        card = self._cards.index((fam, val))
        p1, p2 = self._names.index(p1), self._names.index(p2)

        code, p = self._tracker.update_state(p1, p2, card, action)
        return code, self._names[p]


class Tracker:

    def __init__(self, fnum, fsize):
        self._fsize = fsize
        self._fnum = fnum
        self._state = np.ones((fnum * fsize, fnum * fsize), dtype=int)
        self._owners = [i for i in range(fnum) for j in range(self._fsize)]

    def _other_ind(self, indices):
        """
        indices: a list of indices

        Returns the list of indices that excludes given indices.
        """
        return list(set(range(np.shape(self._state)[0])) - set(indices))

    def _fam_ind(self, card):
        """
        card: index of the card

        Returns the indices of all cards in the same family as card.
        """
        start = card - (card % self._fsize)
        return range(start, start + 4)

    def _hand_ind(self, player):
        """
        player: id of the player of interest

        Returns the indices of the cards that player is holding.
        """
        return [i for i, p in enumerate(self._owners) if p == player]

    def _sever_connections(self, p, posIndices):
        """
        p: id of player whose hand is concerned
        posIndices: indices of cards we want to keep (column indices)

        Finds the card in player's hand, where the posIndices sum to 1+ and
        the other indices have the lowest sum. Sets all other indices to 0,
        thereby severing their connections.
        """
        negIndices = self._other_ind(posIndices)
        negSum = np.sum(self._state[negIndices], axis=0)

        # if not in hand, set to inf
        notHand = self._other_ind(self._hand_ind(p))
        negSum[notHand] = self._state.size+1

        # if posIndices = 0, set to inf
        posSum = np.where(np.sum(self._state[posIndices], axis=1) == 0)
        negSum[posSum] = self._state.size+1

        best = np.argmin(negSum)
        self._state[[best], negIndices] = 0
        return best

    def _fix_rows(self):
        """
        Sets the columns of rows that sum to 1 to 0.
        """
        stop = False
        while not stop:
            stop = True
            rowIndices = np.where(np.sum(self._state, axis=1) == 1)[0]
            for rowIndex in rowIndices:
                colIndex = np.where(self._state[rowIndex] == 1)[0]
                other_row_ind = self._other_ind([rowIndex])
                if np.sum(self._state[:, colIndex], axis=0) > 1:
                    self._state[other_row_ind, colIndex] = 0
                    stop = False

    def _fix_columns(self):
        """
        Sets the rows of columns that sum to 1 to 0.
        """
        self._state = np.transpose(self._state)
        self._fix_rows()
        self._state = np.transpose(self._state)

    def _is_paradox(self):
        """
        Checks whether a paradox has occurred.
        """
        return (np.min(np.sum(self._state, axis=0)) <= 0 or
                np.min(np.sum(self._state, axis=1)) <= 0)

    def _is_win(self, player):
        """
        player: id of the player who took the last action

        Checks whether a win has occurred.
        TODO: can multiple people win simultaneously? Can player besides
        active player win?
        """
        for fam in range(self._fnum):
            # check if family is fully realized
            fam_ind = self._fam_ind(fam)
            fam_state = self._state[:, fam_ind]
            if np.array_equiv(np.sum(fam_state, axis=0),
                              np.ones(self._fsize)):

                # check if player holds all cards in family
                for p in range(self._fnum):
                    if np.sum(fam_state[self._hand_ind(p), :]) == self._fsize:
                        return (1, p)
        return (0, player)

    def _rebalance(self, player):
        """
        player: id of the player who took the last action

        Removes redundant connections and checks for paradoxes.
        """
        self._fix_rows()
        self._fix_columns()

        print(pd.DataFrame(self._state, index=self._owners)) # Todo remove

        if self._is_paradox():
            return (2, player)
        else:
            return self._is_win(player)

    def update_state(self, p1, p2, card, action):
        """
        p1: id of the player who asks
        p2: id of the player who responds
        card: index of the card
        action: either asking (q), responding yes (y), or no (n)

        Updates the state according to the action.
        """

        # ensure that p1 has at least one card from the family
        if action == 'q':
            self._sever_connections(p1, self._fam_ind(card))
            return self._rebalance(p1)

        # add the card to p2's hand and give it to p1
        elif action == 'y':
            index = self._sever_connections(p2, [card])
            self._owners[index] = p1
            return self._rebalance(p2)

        # remove the card from p2's hand
        elif action == 'n':
            self._state[self._hand_ind(p2), card] = 0
            return self._rebalance(p2)

        # invalid action token
        else:
            raise RuntimeError
