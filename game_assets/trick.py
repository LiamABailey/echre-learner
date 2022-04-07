from collections import namedtuple
from dataclasses import dataclass

from .card import Card
from .euchre import NUM_PLAYERS


class UnscoredTrickException(Exception):
    pass


@dataclass
class PlayedCard:
    card: Card
    player_seat: int

class Trick:
    """
    Class associated with a single trick (where each player plays one card)
    """
    def __init__(self):
        """
        Instantiates an unplayed trick
        """
        self.leading_suit = None
        self.played_cards = []
        self.winning_player_seat = None

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
        # if the first card, set the leading suit
        if len(self.played_cards) == 0:
            self.leading_suit = card.suit
        self.played_cards.append(PlayedCard(card, player))

    def score_trick(self, trump: int) -> None:
        """
        Identify the winning player of a trick

        Parameters
        ----------
        trump : int
            Selected trump suit id. Must be in euchre.SUITS

        Returns
        -------
            None
        """
        if len(self.played_cards) != NUM_PLAYERS:
            raise ValueError(f"Expected {NUM_PLAYERS} played cards for trick scoring,"
                            f" saw {len(self.played_cards)}")
        # assume the starting player won, and then challenge this assumption
        leading_suit = self.played_cards[0].card.suit
        high = self.played_cards[0]
        # since played_cards tracks in order, we can review challengers in order
        for candidate in self.played_cards[1:]:
            if high.card.lt_card(candidate.card, trump, leading_suit):
                high = candidate
        self.winning_player_seat = high.player_seat

    def __repr__(self):
        return (f"Trick(lead_suit:{self.leading_suit}; "
                f"winning_player:{self.winning_player}; cards:{self.played_cards})")
