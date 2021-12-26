from collections import namedtuple
from typing import Union

from card import Card
from euchre import NUM_PLAYERS

class Trick:
    """
    Class associated with a single trick (where each player plays one card)
    """
    PlayedCard = namedtuple('PlayedCard',['player','card'])
    def __init__():
        """

        """
        self.played_cards = []
        self.winning_player = None


    def add_card(self, card: Card, player: int) -> None:
        """
        Track a played card

        Parameters
        ----------
            card : Card
                The played card

            player : int
                The seat index of the agent that played the card.

        Returns
        -------
            None

        """
        if len(self.played_cards) > NUM_PLAYERS:
            raise ValueError("Attempting to add an extra card")
        if player < 0 or NUM_PLAYERS <= player:
            raise ValueError(f"Player seat {player} not supported")
        self.played_cards.append(PlayedCard(player, card))


    def score_trick(self, trump: Union[str, int]) -> None:
        """
        Identify the winning player of a trick

        Parameters
        ----------
        trump : Union[str, int]
            Selected trump suit. Must be in euchre.SUITS

        Returns
        -------
            None
        """
        # assume the starting player won, and then challenge this assumption
        leading_suit = self.played_cards[0].card.suit
        high = self.played_cards[0].card
        for p in range(1, NUM_PLAYERS):
            candidate = self.played_cards[p]
            if high.card.lt_card(candidate.card, trump, leading_suit):
                high = candidate
        self.winning_player = high.player
