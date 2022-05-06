from numpy import array,floor,zeros

from .heuristic_player import HeuristicPlayer
from ..models.trick_model import TrickModel
from ..card import Card
from ..hand import Hand
from ..trick import Trick
from .. import euchre

class RLTrickPlayer(HeuristicPlayer):
    """
    Euchre player that leverages heuristics for the calling rounds, but
    can leverage *arbitrary models to perform trick playing.
    """

    def __init__(self, id: int, trick_play_model: TrickModel,
                pickup_act = 1/3, trump_call_act = 0.55):
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
        self._last_reward = None

    @property
    def last_reward(self):
        return self._last_reward

    @attribute.setter
    def last_reward(self, trick_won: bool, hand_won: bool = None,
                        hand_points: int = 0) -> None:
        """
        Constructs and sets the reward associated with the last action -
        reward is weighted by if the trick was won (by the team), if the hand
        was won (by the team, if on a terminating round), and the points
        awarded to the team that won the hand (if on a terminating round)

        Parameters
        ----------
            trick_won: bool
                True if the player's team won the last trick, else False
            hand_won: bool = None
                True if player's team won the hand, else False. None if
                    not immediately after a hand-terminating trick
            hand_points: bool = None
                Number of points awarded to the team that won the hand. Zero
                    if not immediately after a hand-terminating trick

        Returns
        -------
            None

        Side Effects
        ------------


        """
        # winning a trick is +/- .1 points
        r_trick = ((2 ** (trick_won + 1)) -3)/10
        r_hand = 0
        if hand_team_won is not None:
            r_hand = (2 ** (hand_won +1) -3) * hand_points
        self._last_reward = r_trick + r_hand



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
            Trump: euchre.CARD_FACES order,J-left
            other suit 1,2,3: euchre.CARD_FACES
            1 if in player's hand, else 0
        positions 25,51,77,103,129
            The leading player of a trick. Clockwise from the agent:
                0,0.33,0.66,1
        positions 26-50, 52-76, 78-102, 104-128,
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
            state[self._get_card_repr_ix(in_hand, active_hand.trump)] = 1
        # assign position to played cards
        t_ix = 0
        for t_ix,played_trick in enumerate(active_hand.tricks):
            # get the encoding for the starting player
            state[(26 * (t_ix + 1)) -1] =\
                self._get_initial_player_encoding(played_trick.played_cards[0].player_seat)
            for played_card in played_trick.played_cards:
                # calculate the value based on distance from player
                weight = self._get_encoded_card_val(played_card.player_seat)
                subgroup_pos = self._get_card_repr_ix(played_card.card, active_hand.trump)
                # the index is offset by the hand, plus previously evaluated tricks
                state[(26 * (t_ix+1)) + subgroup_pos] = weight
        # if we entered the above loop, increment active trick range ix by 1
        t_ix += bool(active_hand.tricks)
        # assign positions to the ongoing trick
        # if no tricks have been played and if no cards have been played:
        if not (t_ix or active_trick.played_cards):
                state[25] = self._get_initial_player_encoding(self.seat)
        else:
            state[(26 * (t_ix + 1)) -1] =\
              self._get_initial_player_encoding(active_trick.played_cards[0].player_seat)
        for played_card in active_trick.played_cards:
            weight = self._get_encoded_card_val(played_card.player_seat)
            subgroup_pos = self._get_card_repr_ix(played_card.card, active_hand.trump)
            # offset by the hand, previously evaluated tricks
            state[(26 * (t_ix + 1)) + subgroup_pos] = weight
        return state

    def _get_encoded_card_val(self, play_seat: int) -> float:
        """
        Given the seat of the played card, return the
        0.25, 0.5, 0.75, 1  encoded/'weighted' value of the card

        Parameters
        ----------
            play_seat : int
                The seat index of the player that played the card

        Returns
        -------
            float : one of 0.25, 0.5, 0.75, 1
        """
        if not isinstance(play_seat, int) or isinstance(play_seat, bool):
            raise TypeError(f"Expected type(play_seat) = int, received {type(play_seat)}")
        if not (0 <= play_seat < euchre.NUM_PLAYERS):
            raise ValueError(f"Expected play_seat in [0,3], received {play_seat}")
        return (((play_seat - self.seat -1)% euchre.NUM_PLAYERS) + 1) * .25

    def _get_initial_player_encoding(self, play_seat: int) -> float:
        """
        Given the seat of the first player, return the
        0 (left), 1/3, 2/3, 1(self)  encoding of the position

        Parameters
        ----------
            play_seat : int
                The seat index of the player that went first

        Returns
        -------
            float : one of 0, 1/3, 2/3, 1, representing the position encoding
        """
        if not isinstance(play_seat, int) or isinstance(play_seat, bool):
            raise TypeError(f"Expected type(play_seat) = int, received {type(play_seat)}")
        if not (0 <= play_seat < euchre.NUM_PLAYERS):
            raise ValueError(f"Expected play_seat in [0,3], received {play_seat}")
        return (((play_seat - self.seat -1)% euchre.NUM_PLAYERS)) / (euchre.NUM_PLAYERS -1)

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
        if c.is_trump(trump_suit):
            if c.suit != trump_suit:
                # left bar
                return _trump_cards - 1
            else:
                return euchre.CARD_FACES.index(c.face)
        else:
            # note, euchre.SUITS[:trump_suit] + euchre.SUITS[trump_suit + 1:]
            # is more efficient, but requires euchre.SUITS = [0,1,2,3].
            non_trump_suits = euchre.SUITS[:]
            non_trump_suits.remove(trump_suit)
            return _trump_cards\
                 + (non_trump_suits.index(c.suit) * _non_trump_cards)\
                 + euchre.CARD_FACES.index(c.face)

    @staticmethod
    def _invert_card_repr_ix(ix: int, trump_suit: int):
        """
        Given the index of the card in the 0-24 space, and
        the trump suit, returns the associated Card

        Expected index is from the _get_card_repr_ix method

        Parameters
        ----------
            ix: int; 0 <= ix <= 24
                The index representation of the card.

            trump_suit: int
                The trump suit representation from 'euchre'

        Returns
            card.Card : The card represented by the index
        """
        if not isinstance(ix, int) or isinstance(ix,bool):
            raise TypeError(f"ix must be int, received {type(ix)}")
        if ix < 0 or ix > 24:
            raise ValueError(f"ix must be between 0 and 24, received {ix}")
        if ix < 6:
            return Card(trump_suit, euchre.CARD_FACES.index(ix))
        elif ix == 6:
            # left bar
            return Card(euchre.LEFT_SUIT[trump_suit], euchre.JACK)
        else:
            non_trump_suits = euchre.SUITS[:]
            non_trump_suits.remove(trump_suit)
            # the cards at index 7-24 are the remaining suits,
            # each with six possible cards. Because of this, we can
            # unpack the suit and face as follows:
            return Card(floor((ix-7)/6), (ix-7)%6)
