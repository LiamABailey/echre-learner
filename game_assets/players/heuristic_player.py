from typing import Tuple

from .player import Player
from .card import Card


class HeuristicPlayer(Player):
    """
    Euchre player that leverages heuristics for decision-making.
    """

    def exchange_with_kitty(self, kitty_card: Card) -> None:
        """
        Method controlling dealer's adding of kitty_card to the hand,
        and discarding of a card

        Parameters
        ----------
            kitty_card : card.Card
                The face-up card in the kitty added to hand

        Returns
        -------
            None
        """
        raise NotImplementedError

    def play_card(self, active_hand: Hand, active_trick: Trick, dealer_seat: int, lead_seat: int) -> Card:
        """
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
            Card.card : The card played by the player (popped from 'cards_held')

        """
        raise NotImplementedError

    def select_kitty_pickup(self, kitty_card : Card, is_dealer: bool,
                            dealer_is_team_member: bool) -> bool:
        """
        Evaluates the face-up card in the kitty, and
        provides a decision as to if the dealer should pick up the card

        Parameters
        ----------
            kitty_card : card.Card
                The face-up card in the kitty

            is_dealer : bool
                If the player is in the dealer's seat

            is_team_member : bool
                If the dealer is the player's team member

        Returns
        -------
            bool : True if the card is to be picked up, false otherwise
        """
        # evaluate the stregnth of the card relative to the cards in hand.
        raise NotImplementedError

    def select_trump(self, passed_card: Card, is_dealer: bool) -> Tuple[int, bool]:
        """
        The player evaluates the hand for the best suit to play. If
        not the dealer, may pass. Will not select the suit that was
        passed during the face-up kitty round.

        Parameters
        ----------
            passed_card : card
                The card passed in the kitty round (turned down)

            is_dealer : bool
                If the player is in the dealer's seat (is stuck)

        Returns
        -------
            int : The selected suit, if any (from euchre.SUITS). -1 if no suit selected
            bool : True if suit selected, false otherwise.
        """
        DECISION_THRESH = 0.55
        # if player is the dealer
        max_suit = -1
        max_score = -1
        for suit in euchre.SUITS if suit != passed_card.suit:
            eval_score = self._eval_hand_strength(suit)
            if eval_score > max_score:
                max_score = eval_score
                max_suit = eval_suit

        # if the dealer, forced to pick. If not, can pass (thresholded)
        if is_dealer or max_score > DECISION_THRESH:
            return max_suit, True
        else:
            return -1, False


    def _eval_hand_strength(self, suit: int) -> float:
        """
        Evaluates the strength of a hand (five cards) relative to a suit:
        Each card is scored as follows
            when on-suit:
                Jack(R): 1
                Jack(L): 11/12
                Ace: 5/6
                King: 3/4
                Queen: 7/12
                Ten: 5/12
                Nine: 1/4

            when off-suit:
                Ace: 7/12
                King: 5/12
                Queem: 1/4
                Jack: 1/6
                Ten: 1/12
                Nine: 0

        This gives a minimum score of 1/6 (three offsuit nines + two offsuit tens),
        and a maxmimum score of 49/12 (On-suit R, L, Ace, King, and either Queen or off-suit Ace).
        Scores are normalized between 0 and 1 with respect to these boundaries.

        Parameters
        ----------
            suit : int, 0 <= v <= 3
                The integer representing the suit to evaluate

        Returns
        -------
            float : The score/value of the hand, [0,1]
        """
        MIN_SCORE = 1/6
        MAX_SCORE = 49/12


        score = 0
        for card in self.cards_held:
            score += _eval_card_strength(card, suit)
        return (score - MIN_SCORE)/(MAX_SCORE - MIN_SCORE)

def _eval_card_strength(card: Card, suit) -> float:
    """
    Evaluates the strength of a card, given the suit

    Each card is scored as follows
        when on-suit:
            Jack(R): 12
            Jack(L): 11
            Ace: 10
            King: 8
            Queen: 7
            Ten: 5
            Nine: 3

        when off-suit:
            Ace: 7
            King: 5
            Queem: 3
            Jack: 2
            Ten: 1
            Nine: 0

    Scores are returned over the [0,1] range (linear standardization)

    Parameters
    ----------
        card : card.Card
            The card under evaluation
        suit : int, 0 <= v <= 3
            The integer representing the suit to evaluate

    Returns
    -------
        float : The score/value of the card, [0,1]
    """
    MAX_SCORE = 12
    trump_scores = {
        euchre.JACK: 12,
        "left": 11,
        euchre.ACE: 10,
        euchre.KING: 8,
        euchre.QUEEN: 7,
        euchre.TEN: 5,
        euchre.NINE: 3
    }
    nontrump_scores = {
        euchre.ACE: 7,
        euchre.KING: 5,
        euchre.QUEEN: 3,
        euchre.JACK: 2,
        euchre.TEN: 1,
        euchre.NINE: 0
    }
    if card.is_trump(suit):
        # check to see if the card is the left
        if card.face == euchre.JACK and card.suit != suit:
            score = trump_scores['left']
        else:
            score = trump_scores[card.face]
    else:
        score = nontrump_scores[card.face]

    return score / MAX_SCORE
