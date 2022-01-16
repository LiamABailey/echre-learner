from .card import Card
from .euchre import NUM_TRICKS, NUM_TRICKS_TO_WIN_HAND, TEAM_ZERO, TEAM_ZERO_ID, TEAM_ONE_ID, TEAMS
from .trick import Trick, UnscoredTrickException

class Hand:

    def __init__(self, bidder: int, trump: int,
                kitty_face_up: Card, kitty_picked_up : bool) -> None:
        """
        Hand constructor (encapsulating 5 tricks). Requires specification of
        the trump suit

        Parameters
        ----------
            bidder : int
                the seat index of the bidder (player who chose trump)

            trump : int
                One of the suits in euchre.SUITS

            kitty_face_up :
                The face-up card evaluated in the first round of bidding

            kitty_picked_up :
                If the face-up card was picked up or passed on


        Returns
        -------
            None
        """
        self.tricks = []
        self.trump = trump
        self.bidder = bidder
        self.kitty_face_up = kitty_face_up
        self.kitty_picked_up = kitty_picked_up
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
        num_wins = 0
        if len(self.tricks) != NUM_TRICKS:
            raise ValueError(f"Expected {NUM_TRICKS} tricks, saw {len(self.tricks)}")
        for trick in self.tricks:
            if trick.winning_player is None:
                raise UnscoredTrickException
            if trick.winning_player in TEAM_ZERO:
                num_wins += 1
        if num_wins >= NUM_TRICKS_TO_WIN_HAND:
            self.winning_team = TEAM_ZERO_ID
        else:
            self.winning_team = TEAM_ONE_ID
            # invert - the previous tallying was performed with respect to
            # team zero winning
            num_wins = NUM_TRICKS - num_wins
        self.points = self._calc_points(num_wins, self.bidder in TEAMS[self.winning_team])

    @staticmethod
    def _calc_points(num_tricks_won: int, is_bidder: bool) -> int:
        """
        Calculate the number of points won by the team

        # bidder:
            < 2: 0 points
            3-4: 1 point
            5: 2 points
        # not bidder:
            < 2: 0 points
            > 2: 2 points

        Parameters
        ----------
            num_tricks_won : int
                The number of tricks in the hand won

            is_bidder : bool
                If the team contained the bidder
        """
        n_points = 0
        if num_tricks_won >= 3:
            if num_tricks_won == 5 or not is_bidder:
                n_points = 2
            else:
                n_points = 1

        return n_points


    def __repr__(self):
        return (f"Hand(trump:{self.trump}; bidder:{self.bidder}; winning_team:"
                f"{self.winning_team}; points:{self.points}; "
                f"tricks:{self.tricks})")

    def __eq__(self, other):
        """
        Equality method
        """
        if not isinstance(other, Hand):
           raise TypeError("Expected instance of hand.Hand")
        tricks_eq = False
        if len(self.tricks) == len(other.tricks):
            tricks_eq = True
            for trick_s, trick_o in zip(self.tricks, other.tricks):
                if trick_s != trick_o:
                    tricks_eq = False

        return (self.trump == other.trump) and (self.bidder == other.bidder) and\
            (self.winning_team == other.winning_team) and\
            (self.points == other.points) and tricks_eq
