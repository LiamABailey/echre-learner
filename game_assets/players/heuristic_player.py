from copy import deepcopy
from typing import List, Tuple

from .player import Player
from ..card import Card
from ..euchre import SUITS, NINE, TEN, JACK, QUEEN, KING, ACE, LEFT_SUIT
from ..hand import Hand
from ..trick import Trick


class HeuristicPlayer(Player):
    """
    Euchre player that leverages heuristics for decision-making. Doesn't
    take advantage of 'memory' (known played cards) when playing a trick
    """

    def __init__(self, id: int, pickup_act = 2/3, trump_call_act = 0.55):
        """
        Parameters
        ----------
            id : int
                The player's ID

            pickup_thresh : float, default = 2/3
                Controls the aggressiveness with which the player decides
                to call 'pick up' during the face-up round of trump selection.
                Closer to 0 - less likely to call pick up, closer to 1 -more likely.
                Must be in range [0,1]

            trump_call_act : float, default = 0.55
                Controls the player's decision to pick a trump suit during the
                free selection round. 1 is most aggresive, 0 is least.
                Must be in range [0,1]

        """
        self.player_id = id
        self.seat = None
        self.cards_held = []
        if pickup_act > 1 or pickup_act < 0:
            raise ValueError(f"pickup_act must be in [0,1], received {pickup_act}")
        self.pickup_thresh = pickup_act
        if trump_call_act > 1 or trump_call_act < 0:
            raise ValueError(f"trump_call_act must be in [0,1], received {trump_call_act}")
        self.trump_call_thresh = trump_call_act

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
        weak_ix = self._weakest_card_ix(kitty_card.suit)
        weak_card = self.cards_held.pop(weak_ix)
        self.cards_held.append(kitty_card)

    def cards_in_suit(self, suit: int, is_trump: bool = False) -> List[int]:
        """
        Returns the indices of cards in hand in the suit

        Parameters
        ----------
            suit : int
                The integer of the suit, from euchre.SUITS
            is_trump : int
                If the suit under evaluation is trump
        """
        ix_in_suit = []
        for ix, card in enumerate(self.cards_held):
            # if the card is a member of the suit
            if (card.suit == suit) or\
                    (is_trump and card._is_left_bar(suit)):
                ix_in_suit.append(ix)
        return ix_in_suit

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
        played_card_ix = -1
        #if no cards have been played yet, play strongest card
        if len(active_trick.played_cards) == 0:
            selected_card_strength = -1
            for ix, card in enumerate(self.cards_held):
                strength = _eval_card_strength(card, active_hand.trump)
                if strength > selected_card_strength:
                    played_card_ix = ix
                    selected_card_strength = strength
        # else, if cards have been played, find a winning card that doesn't
        # renege
        else:
            # identify the current winning card
            best_ix = 0
            for candidate_ix, played_card in enumerate(active_trick.played_cards[1:]):
                if active_trick.played_cards[best_ix].card.lt_card(played_card.card, active_hand.trump, active_trick.leading_suit):
                    best_ix = candidate_ix + 1
            # is a team member winning ? if so, play worst card
            best_card = active_trick.played_cards[best_ix].card
            play_to_win = (active_trick.played_cards[best_ix].player_seat - self.seat) % 2 == 0
            # get all cards legal for play
            non_renege_ix = self.cards_in_suit(active_trick.leading_suit, active_trick.leading_suit == active_hand.trump)
            # if unable to renege (no cards forced/all eligible)
            if len(non_renege_ix) == 0:
                non_renege_ix = list(range(len(self.cards_held)))
            # play the best card in the scenrio:
            if play_to_win:
                lowest_winning_value = 2
                for ix, card in enumerate(self.cards_held):
                    if ix in non_renege_ix:
                        if best_card.lt_card(card, active_hand.trump, active_trick.leading_suit):
                            card_strength = _eval_card_strength(card, active_hand.trump)
                            if card_strength < lowest_winning_value:
                                played_card_ix = ix
                                lowest_winning_value = card_strength
            # if no  card has beeen picked: either there wasn't
            # a winning card to select above, or we don't want to win
            if played_card_ix == -1:
                played_card_ix = self._weakest_card_ix(active_hand.trump, non_renege_ix)

        return self.cards_held.pop(played_card_ix)

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
        pickup_signal = False
        if is_dealer:
            pickup_signal = self._select_kitty_pickup_dealer(kitty_card)
        else:
            # evaluate the strength of the hand, relative to the kitty card's suit
            hand_str = self._eval_hand_strength(kitty_card.suit)
            # evaluate the strength of the kitty card
            kitty_card_str = _eval_card_strength(kitty_card, kitty_card.suit)
            if dealer_is_team_member:
                # want kitty card to be strong, hand to be strong for suit
                eval_score = (hand_str ** (1/2)) * (kitty_card_str ** (1/2))
                if eval_score > self.pickup_thresh:
                    pickup_signal = True
            else:
                # want the kitty card to be weak relative to hand for pickup
                eval_score = (hand_str ** (1/2)) / (kitty_card_str ** (1/2))
                if 1 - self.pickup_thresh > eval_score :
                    pickup_signal = True

        return pickup_signal

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
        # if player is the dealer
        max_suit = -1
        max_score = -1
        for suit in SUITS:
            if suit != passed_card.suit:
                eval_score = self._eval_hand_strength(suit)
                if eval_score > max_score:
                    max_score = eval_score
                    max_suit = suit

        # if the dealer, forced to pick. If not, can pass (thresholded)
        if is_dealer or max_score > self.trump_call_thresh:
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

    def _weakest_card_ix(self, suit: int, elig: List[int] = []) -> int:
        """
        Evaluates the hand and identifies the weakest card relative
        to the provdied suit

        Parameters
        ----------
            suit : int, 0 <= v <= 3
                The integer representing the suit to evaluate

            elig : List[int], default = []
                The list of positions eligible for eval. If empty, evaluate all

        Returns
        -------
            int : The index of the card in self.cards_held
        """
        if len(elig) == []:
            elig = list(range(len(self.cards_held)))
        pos = -1
        strength = 2
        for ix, card in enumerate(self.cards_held):
            if ix in elig:
                if (card_score := _eval_card_strength(card, suit)) < strength:
                    pos = ix
                    strength = card_score
        return pos

    def _select_kitty_pickup_dealer(self, kitty_card):
        """
        Kitty pickup decision for the dealer

        Parameters
        ----------
            kitty_card : card.Card
                The face-up card in the kitty

        Returns
        -------
            bool : True if the card is to be picked up, false otherwise

        """
        # find the weakest card in the hand, relative to trump
        weak_ix = self._weakest_card_ix(kitty_card.suit)
        # evaluate current hand strength for all other suits
        strongest_suit = -1
        strongest_score = -1
        for suit in SUITS:
            if suit != kitty_card.suit:
                if (candidate_score := self._eval_hand_strength(suit)) > strongest_score:
                    strongest_suit = suit
                    strongest_score = candidate_score
        # pop the weakest card & evaluate
        weak_card = self.cards_held.pop(weak_ix)
        self.cards_held.append(kitty_card)
        new_hand_score = self._eval_hand_strength(kitty_card.suit)
        # post-eval, return the card to hand
        self.cards_held.pop()
        self.cards_held.append(weak_card)
        if new_hand_score > 0.6 and new_hand_score > strongest_score:
            return True
        return False


def _eval_card_strength(card: Card, suit: int) -> float:
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
        JACK: 12,
        "left": 11,
        ACE: 10,
        KING: 8,
        QUEEN: 7,
        TEN: 5,
        NINE: 3
    }
    nontrump_scores = {
        ACE: 7,
        KING: 5,
        QUEEN: 3,
        JACK: 2,
        TEN: 1,
        NINE: 0
    }
    if suit == -1:
        print("UH OH")
    if card.is_trump(suit):
        # check to see if the card is the left
        if card.face == JACK and card.suit != suit:
            score = trump_scores['left']
        else:
            score = trump_scores[card.face]
    else:
        score = nontrump_scores[card.face]

    return score / MAX_SCORE
