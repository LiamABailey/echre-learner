from abc import ABC, abstractmethod
from typing import List

from ..card import Card
from ..hand import Hand
from ..trick import Trick

class TrickModel(ABC):
    """
    Basic definition of a model supporting trick playing
    """

    @abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def save(self, file_path: str):
        """
        Given the target file path, save the model into a file

        Parameters
        ----------
            file_path : str
                The saved model destination

        Returns
        -------
            None
        """
        raise NotImplementedError

    @abstractmethod
    def load(self, file_path: str):
        """
        Given the source file path, load the model from a file

        Parameters
        ----------
            file_path : str
                The saved model destination

        Returns
        -------
            None
        """
        raise NotImplementedError

    @abstractmethod
    def pred_card(self, player_hand: List[Card], active_hand: Hand,
                active_trick: Trick) -> int:
            """
            Selects the card to play from the players hand

            Given the known information about the game:
                - played tricks
                - the trick currently being played
                - the kitty card (and if it was passed)
                - the face-up card in the dealer's hand
                - the dealer's seat
                - the seat of the player who starts the trick
                - the player's current hand
             selects a card to play, removing it from the player's hand and
             returning it

            Parameters
            ----------
                player_hand : List[Card]
                    The cards currently held by the player

                active_hand : Hand.hand
                    The hand currently being played

                active_trick : Trick.trick
                    The trick currently being played

                dealer_seat : int
                    The seat of the dealer player, 0-3

                lead_seat : int
                    The seat of the player who started the trick

            Returns
            -------
                int : the in-hand index of the card to be played
            """
            raise NotImplementedError

    def fit(self, **kwargs) -> None:
        """
        Perform a single fit step
        """
        raise NotImplementedError
