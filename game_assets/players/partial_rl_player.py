from numpy import array,zeros

from .heuristic_player import HeuristicPlayer
from ..models.trick_model import TrickModel
from ..card import Card
from ..hand import Hand
from ..trick import Trick
from ..euchre import CARD_FACES, SUITS, NUM_PLAYERS

class RLTrickPlayer(HeuristicPlayer):
    """
    Euchre player that leverages heuristics for the calling rounds, but
    can leverage *arbitrary models to perform trick playing.
    """

    def __init__(self, id: int, trick_play_model: TrickModel,
                pickup_act = 1/3, trump_call_act = 0.55,):
        """
        Parameters
        ----------
            id : int
                The player's ID

            trick_play_model : TrickModel
                An instance of a class conforming to `TrickModel` that supports
                card selection & learning over time

            pickup_thresh : float, default = 1/3
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
        self.learning = False
        if pickup_act > 1 or pickup_act < 0:
            raise ValueError(f"pickup_act must be in [0,1], received {pickup_act}")
        self.pickup_thresh = pickup_act
        if trump_call_act > 1 or trump_call_act < 0:
            raise ValueError(f"trump_call_act must be in [0,1], received {trump_call_act}")
        self.trump_call_thresh = trump_call_act
        self.trick_play_model = trick_play_model

    def enable_learning(self):
        """
        Toggles model training 'on'

        Parameters
        ----------
            None

        Returns
        -------
            None
        """
        self.learning = True

    def disable_learning(self):
        """
        Toggles model training 'off'

        Parameters
        ----------
            None

        Returns
        -------
            None
        """
        self.learning = False

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
            active_hand : hand.Hand
                The hand currently being played

            active_trick : trick.Trick
                The trick currently being played

            dealer_seat : int
                The seat of the dealer player, 0-3

            lead_seat : int
                The seat of the player who started the trick

        Returns
        -------
            card.Card : The card played by the player (popped from 'cards_held')

        """
        played_card_ix = self.trick_play_model.pred_card(self.cards_held, active_hand, active_trick)
        if self.training:
            # store the event to the memory buffer
            self.trick_play_model.add_to_buffer(self.cards_held, active_hand,
                                            active_trick, self.cards_held[played_card_ix])
            # perform a gradient fit step
            self.trick_play_model.step_fit()

        return self.cards_held.pop(played_card_ix)

    def _get_state_repr(self, active_hand: Hand, active_trick: Trick) -> array:
        """
        Given information about the cards held by the player, the active
        hand, and the active trick, return a representation of the state.

        The encoding scheme is as follows:

        positions 0-24:
            Trump: CARD_FACES order,J-left
            other suit 1,2,3: CARD_FACES
            1 if in player's hand, else 0
        positions 25,51,77,103,129
            The leading player of a trick. Clockwise from the agent:
                0,0.33,0.66,1
        positions 26-50, 52-76, 78-102, 104-128, 130-154
            The cards played, following the ordering scheme from positions 0-24
            Values are based on the played order
                (first played) 0.25, 0.5, 0.75, 1 (last played)

        Parameters
        ----------
            active_hand : hand.Hand
                The hand currently being played

            active_trick : trick.Trick
                The trick currently being played

        Return
        ------
            np.array : the 155 x 1 representation of the state
        """
        state = zeros((155,))
        # assign positions to cards in hand
        for in_hand in self.cards_held:
            state[_get_card_repr_ix(in_hand, active_hand.trump)] = 1
        # assign position to played cards
        for t_ix,played_trick in enumerate(active_hand):
            for played_card in played_trick:
                # calculate the value based on distance from player
                weight = ((played_card.player_seat - self.seat   -1)\
                        % NUM_PLAYERS) / (NUM_PLAYERS - 1)
                subgroup_pos = _get_card_repr_ix(played_card.card, active_hand.trump)
                # the index is offset by the hand, plus previously evaluated tricks
                state[(25 * (t_ix+1)) + subgroup_pos] = weight
        # assign positions to the active trick
        for played_card in active_trick:
            weight = ((played_card.player_seat - self.seat   -1)\
                    % NUM_PLAYERS) / (NUM_PLAYERS - 1)
            subgroup_pos = _get_card_repr_ix(played_card.card, active_hand.trump)
            # offset by the hand, previously evaluated tricks
            state[(25 * (t_ix + 2)) + subgroup_pos] = weight
        return state

    @staticmethod
    def _get_card_repr_ix(c: Card, trump_suit: int):
        """
        Returns the index of the card in the 0-24 space.

        For consistentcy, the non-trump suits are ordered based
        on the numerical order assigned in euchre.py.

        Parameters
        ----------
            c: card.Card
                The card under evaluation

            trump_suit : int
                The trump suit representation from `euchre`
        Returns
        -------
            int : 0-24
                The card index/position in the defined representation.
        """
        _trump_cards = 7
        _non_trump_cards = 6
        # note, SUITS[:trump_suit] + SUITS[trump_suit + 1:]
        # is more efficient, but requires SUITS = [0,1,2,3].
        non_trump_suits = SUITS[:]
        non_trump_suits.remove(trump_suit)
        if c.is_trump(trump_suit):
            if c.suit != trump_suit:
                # left bar
                return _trump_cards - 1
            else:
                return CARD_FACES.index(c.face)
        else:
            return _trump_cards\
                 + (non_trump_suits.index(c.suit) * _non_trump_cards)\
                 + CARD_FACES.index(c.face)
