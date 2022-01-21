from typing import Tuple
import unittest

from game_assets.players.random_player import Player
from game_assets.card import Card
from game_assets.euchre import NUM_PLAYERS
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


class TestAssignSeat(unittest.TestCase):

    def setUp(self):
        self.player = ConcretePlayer(0)

    def test_assign_seat_valid(self):
        """
        Test that the 4 accepted seats are allowed
        """
        for seat_ix in range(0,NUM_PLAYERS):
            with self.subTest():
                self.player.assign_seat(seat_ix)
                self.assertEqual(self.player.seat, seat_ix)

    def test_assign_seat_invalid_ix(self):
        """
        Validate that OOB seats are not accepted
        """
        for seat_ix in [-1, NUM_PLAYERS]:
            with self.subTest():
                with self.assertRaises(ValueError):
                    self.player.assign_seat(seat_ix)

    def test_assign_seat_bad_type(self):
        """
        Confirm type errors raised when non-int used
        """
        for seat_ix in [1.0, '0', True]:
            with self.subTest():
                with self.assertRaises(TypeError):
                    self.player.assign_seat(seat_ix)
