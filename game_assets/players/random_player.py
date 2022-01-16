from numpy.random import choice, randint, random
from .player import Player
from .euchre import SUITS

class RandomPlayer(Player):
    """
    Euchre player that chooses cards randomly
    """

    def exchange_with_kitty(self, kitty_card: Card) -> None:
        """
        Method controlling dealer's adding of kitty_card to the hand,
        and discarding of a card. RandomPlayer picks at random.

        Parameters
        ----------
            kitty_card : card.Card
                The face-up card in the kitty added to hand

        Returns
        -------
            None
        """
        card_ix = np.random.randint(low = 0, high = len(self.cards_held))
        removed_card = self.cards_held.pop(card_ix)
        self.cards_held.append(kitty_card)
        return removed_card

    def play_card(self, active_hand: Hand, active_trick: Trick, dealer_seat: int, lead_seat: int) -> Card:
        """
        Randomly selects a valid card to play, and plays it.

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
        # if the player has a card of the eligible suit, we limit
        # to cards of that suit
        eligible_ix = range(len(self.cards_held))
        if active_trick.leading_suit in [c.suit for c in self.cards_held]:
            eligible_ix = [i for i,c in enumerate(self.cards_held) if c.suit == active_trick.leading_suit]
        play_ix = choice(eligible_ix)
        return self.cards_held.pop(play_ix)

    def select_kitty_pickup(self, kitty_card : Card, is_dealer: bool,
                            dealer_is_team_member: bool) -> bool:
        """
        25% of the time, requests that the kitty is picked up. Othewise, passes.

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
        # 25% chance of calling pick up
        if random() < 0.25:
            return True
        return False

    def select_trump(self, passed_suit: string, is_dealer: bool) -> Tuple[int, bool]:
        """
        If the player is the dealer (or otherwise on a 25% chance), picks
        a trump suit at random. Otherwise, passes the selection

        Parameters
        ----------
            passed_suit : string
                The suit-string passed in the kitty round (turned down)

            is_dealer : bool
                If the player is in the dealer's seat (is stuck)

        Returns
        -------
            int : The selected suit, if any (from euchre.SUITS)
            bool : True if suit selected, false otherwise.
        """
        # if stuck, or 25% chance otherwise
        if is_dealer or random() < 0.25:
            return choice(SUITS), True
        else:
            return None, False
