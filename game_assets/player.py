from abc import ABC
from typing import List

from .card import Card


class Player(ABC):
    """
    The basic player definition
    """

    def __init__(self, id: int):
        """
        Parameters
        ----------
            id : int
                The player's ID
        """
        self.player_id = id
        self.cards_held = []


    def receive_cards(self, cards: List[Card]):
        """
        receive a 'hand' of five cards

        Paramters
        ---------
            cards: the 5 cards for the player for the hand

        Returns
        -------
            None
        """
        if len(cards) !=5
            raise ValueError("Must receive five cards")
        self.cards_held = cards
