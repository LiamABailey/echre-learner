from typing import Union

from euchre import NUM_TRICKS
from trick import Trick

class Hand:

    def __init__(self, bidder: int, trump: Union[int,str]) -> None:
        """
        Hand constructor (encapsulating 5 tricks). Requires specification of
        the trump suit

        Parameters
        ----------
            bidder : int
                the seat index of the bidder (player who chose trump)

            trump : int or str
                One of the suits in euchre.SUITS



        Returns
        -------
            None
        """
        self.tricks = []
        self.trump = trump
        self.bidder = bidder
        # define winning defaults
        self.winning_team = None
        self.points = 0


    def add_trick(self, played_trick: Trick) -> None:
        """
        add a played and scored trick to the trick storer.

        Parameters
        ----------
            played_trick : Trick
                The trick to track

        Returns
        -------
            None

        """
            if len(self.tricks) > NUM_TRICKS:
                raise ValueError("Attempting to add unexpected trick!")
            self.tricks.append(played_trick)


    def score_hand(self) -> None:
        """
        Score a hand of (5) played tricks, and sets the winning team +
        score on the hand

        Parameters
        ----------
            None

        Returns
        -------
            None
        """
