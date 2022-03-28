from itertools import product
from typing import Tuple
import unittest

from game_assets.players.random_player import Player
from game_assets.card import Card
from game_assets.euchre import NUM_PLAYERS, SUITS, CARD_FACES
from game_assets.hand import Hand
from game_assets.trick import Trick

import random

class ConcretePlayer(Player):
    """
    Because an ABC can't be directly instantiated, we implement
    a player conforming to the ABC to test the non-abstract methods.
    """
    def __init__(self, seat: int):
        pass

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
                self.player.seat = None

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


class receive_cards(unittest.TestCase):

    def setUp(self):
        self.player = ConcretePlayer(0)
        self.deck = [Card(suit, face) for suit, face in product(SUITS, CARD_FACES)]

    def test_receive_cards_valid(self):
        """
        Test that 5 cards accepted
        """
        hand_ixs = [
            [0,1,2,3,4],
            [2, 6, 10, 12, 16],
            [0, 5, 10, 15, 20],
            [19, 20, 21, 22, 23]
        ]
        for hand_ix_list in hand_ixs:
            hand = [self.deck[i] for i in hand_ix_list]
            with self.subTest():
                self.player.receive_cards(hand)
                self.assertCountEqual(self.player.cards_held, hand)
                self.player.cards_held = []

    def test_receive_cards_wrong_hand_size(self):
        """
        Test a series of bad hand sizes
        """
        hand_ixs = [
            [],
            [5],
            [5, 6, 7, 8],
            [10, 12, 14, 16, 18, 20]
        ]
        for hand_ix_list in hand_ixs:
            hand = [self.deck[i] for i in hand_ix_list]
            with self.subTest():
                with self.assertRaises(ValueError):
                    self.player.receive_cards(hand)

    def test_receive_cards_bad_types(self):
        """
        Validate type errors raised when passed non-Card typed objects
        """
        hands = [
            [1,2,3,4,5],
            ["ace of hearts", "ace of spades", "ace of diamonds", "jack of clubs", "queen of hearts"],
            [(0,2), (3,1), (2,4), (1,0), (0,5)],
            [Card(0,0), Card(0,0), Card(0,0), Card(0,0), 0],
            [1, Card(1,1), Card(1,1), Card(1,1), Card(1,1)]
        ]
        for hand in hands:
            with self.subTest():
                with self.assertRaises(TypeError):
                    self.player.receive_cards(hand)
