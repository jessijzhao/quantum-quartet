"""
Author: jessijzhao
Date: June 1, 2022

Custom types and data classes for Quantenquartett.
"""


class Actions:
    QUESTION: str = "q"
    POSITIVE: str = "y"
    NEGATIVE: str = "n"


class ActionType:
    VALID: int = 0
    WIN: int = 1
    LOSS: int = -1
