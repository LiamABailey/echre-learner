from itertools import product
from random import shuffle
from typing import Dict, Tuple

from .card import Card
from .player import Player
from .euchre import NUM_PLAYERS, NUM_TRICKS, SUITS, CARD_FACES

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
        self.deck = [Card(suit, face) for suit, face in product(SUITS, CARD_FACES)]


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
        # deal out cards
        kitty_face_up = self._deal()
        # choose trump
        for _ in range(NUM_TRICKS):
            self._play_trick()


    def _deal(self) -> Card:
        """
        Deal a hand of cards

        Parameters
        ----------
            None

        Returns
        -------
            Card : the face-up card in the kitty

        """
        # shuffle the deck
        shuffle(self.deck)
        # hand out cards
        for p_ix, player in enumerate(self.players):
            start_ix = p_ix * NUM_TRICKS
            player.receive_cards(self.deck[start_ix:start_ix + NUM_TRICKS])
        # return the kitty, which is the 21st card in the deck
        return self.deck[NUM_PLAYERS * NUM_TRICKS]

    def _pick_trump(self, kitty_card) -> Dict:
        """
        Have the four players perform trump selection

        Paramters
        ~~~~~~~~~
            kitty_card : Card
                The face-up card in the kitty
        Returns
        ~~~~~~~
            Dictonary of results (k,v):
                "trump" : str
                    The selected trump suit
                "selector" : int
                    The player ID of the player that selected trump
        """
        # because dealer is tracked positionally to the player list, we can
        # leverage that position to rotate the player order as needed
        player_order = self.players[self.dealer:] + self.players[:self.dealer]
        # TODO : design selection on first pass
        # TODO : design selection on second pass
        # TODO : define pick-up for dealer

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
