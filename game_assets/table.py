from typing import Tuple

from scorer import Scorer
from player import Player
from euchre import NUM_PLAYERS, NUM_TRICKS

class Table:
    """
    The game table, consisting of the scorer, and the four players.
    """
    def __init__(self,
                scorer: Scorer,
                p1: Player,
                p2: Player,
                p3: Player,
                p4: Player):
        """
        Set up the table with the scorer and
        four players. Players [1,3] and [2,4] are on teams

        Parameters
        ----------

        Returns
        -------
            None

        """
        self.scorer = scorer
        self.players = [p1, p2, p3, p4]
        self.dealer = 0
        self.team1_score = 0
        self.team2_score = 0


    def get_scores(self) -> Tuple[int,int]:
        """
        Return the current scores

        Parameters
        ----------
            None

        Returns:
            int : the current score for the first team (players 1 and 3)
            int : the current score for the second team (players 2 and 4)
        """
        return self.team1_score, self.team2_score


    def play_hand(self):
        """
        Play a hand (5 tricks) of euchre.

        Parameters
        ----------
            None

        Returns
        -------
            None
        """
        pass
        # deal
        # choose trump
        for _ in range(NUM_TRICKS):
            self._play_trick()


    def _deal(self):
        """
        Deal a hand of cards
        """
        pass


    def _play_trick(self):
        """
        Have the 4 players play a single trick.
        """
        pass


    def _next_dealer(self):
        """
        Pass the deal to the next dealer (positional)
        """
        self.dealer = (self.dealer + 1) % NUM_PLAYERS
