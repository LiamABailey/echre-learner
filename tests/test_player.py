from typing import Tuple
import unittest

from game_assets.players.random_player import Player
from game_assets.card import Card
from game_assets.hand import Hand
from game_assets.trick import Trick

class ConcretePlayer(Player):
    """
    Because an ABC can't be directly implemented, we implement
    a player conforming to the ABC to test the non-abstract methods.
    """

    def exchange_with_kitty(self, kitty_card: Card) -> None:
        pass

    def play_card(self, active_hand: Hand, active_trick: Trick, dealer_seat: int, lead_seat: int) -> Card:
        pass

    def select_kitty_pickup(self, kitty_card: Card, is_dealer: bool, dealer_is_team_member: bool) -> bool:
        pass

    def select_trump(self, passed_card: Card, is_dealer: bool) -> Tuple[int, bool]:
        pass
