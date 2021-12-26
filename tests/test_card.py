import unittest

from game_assets import euchre
from game_assets import card

class TestIsLeftBar(unittest.TestCase):

    def test_is_left_bar_true(self):
        """
        Test where card is left bar
        """
        trump = euchre.HEART
        l_j = card.Card(euchre.LEFT_SUIT[trump], euchre.JACK)
        self.assertTrue(l_j._is_left_bar(trump))


    def test_is_left_bar_false(self):
        """
        Test a basic case where the card is not the left bar
        """
        trump = euchre.DIAMOND
        other_suit = euchre.CLUB
        c_9 = card.Card(other_suit, euchre.NINE)
        self.assertFalse(c_9._is_left_bar(trump))


    def test_is_left_bar_right(self):
        """
        Test a basic case where the card is the right bar
        """
        trump = euchre.SPADE
        r_j = card.Card(trump, euchre.JACK)
        self.assertFalse(r_j._is_left_bar(trump))


    def test_is_left_bar_offsuit_jack(self):
        """
        Test a basic case where the card is a jack, but neither the
        left or right
        """
        trump = euchre.DIAMOND
        other_suit = euchre.CLUB
        c_9 = card.Card(other_suit, euchre.JACK)
        self.assertFalse(c_9._is_left_bar(trump))


class TestIsTrump(unittest.TestCase):

    def test_is_trump_true(self):
        """
        Test where card is in the trump suit
        """
        trump = euchre.HEART
        h_10 = card.Card(trump, euchre.TEN)
        self.assertTrue(h_10.is_trump(trump))


    def test_is_trump_false(self):
        """
        Test where card is not in the trump suit
        """
        trump = euchre.HEART
        other_suit = euchre.CLUB
        c_a = card.Card(other_suit, euchre.ACE)
        self.assertFalse(c_a.is_trump(trump))


    def test_is_trump_left_bar(self):
        """
        Confirm that the left bar is identified as trump
        """
        trump = euchre.SPADE
        l_j = card.Card(euchre.LEFT_SUIT[trump], euchre.JACK)
        self.assertTrue(l_j.is_trump(trump))


    def test_is_trump_right_bar(self):
        """
        Confirm that the right bar is identified as trump
        """
        trump = euchre.SPADE
        r_j = card.Card(trump, euchre.JACK)
        self.assertTrue(r_j.is_trump(trump))
