from abc import ABC
from typing import List, Tuple

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

    @abstractmethod
    def select_kitty_pickup(self, is_dealer: bool, dealer_is_team_member: bool) -> bool:
        """
        Evaluates the face-up card in the kitty, and
        provides a decision as to if the dealer should pick up the card

        Parameters
        ----------
            is_dealer : bool
                If the player is in the dealer's seat

            is_team_member : bool
                If the dealer is the player's team member

        Returns
        -------
            bool : True if the card is to be picked up, false otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def select_trump(self, passed_suit: string, is_dealer: bool) -> Tuple[str, bool]:
        """
        The player evaluates the hand for the best suit to play. If
        not the dealer, may pass. Will not select the suit that was
        passed during the face-up kitty round.

        Parameters
        ----------
            passed_suit : string
                The suit-string passed in the kitty round (turned down)

            is_dealer : bool
                If the player is in the dealer's seat (is stuck)

        Returns
        -------
            str : The selected suit, if any
            bool : True if suit selected, false otherwise.
        """
        raise NotImplementedError
