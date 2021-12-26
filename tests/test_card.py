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
        c_9 = card.Card(euchre.CLUB, euchre.NINE)
        self.assertFalse(c_9._is_left_bar(trump))


    def test_is_left_bar_right(self):
        """
        Test a basic case where the card is the right bar
        """
        trump = euchre.SPADE
        r_j = card.Card(euchre.SPADE, euchre.JACK)
        self.assertFalse(r_j._is_left_bar(trump))


    def test_is_left_bar_offsuit_jack(self):
        """
        Test a basic case where the card is a jack, but neither the
        left or right
        """
        trump = euchre.DIAMOND
        c_9 = card.Card(euchre.CLUB, euchre.JACK)
        self.assertFalse(c_9._is_left_bar(trump))
