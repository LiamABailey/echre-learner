import unittest

from game_assets import card, euchre

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


class TestLtCard(unittest.TestCase):

    def test_lt_card_base_true_case_trump(self):
        """
        basic case : same suit, is LT, trump suit
        """
        trump = euchre.SPADE
        lead = euchre.HEART
        card_1 = card.Card(trump, euchre.NINE)
        card_2 = card.Card(trump, euchre.TEN)
        self.assertTrue(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_base_false_case_trump(self):
        """
        basic case : same suit, is GE, trump suit
        """
        trump = euchre.SPADE
        lead = euchre.HEART
        card_1 = card.Card(trump, euchre.ACE)
        card_2 = card.Card(trump, euchre.KING)
        self.assertFalse(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_base_true_case_lead(self):
        """
        basic case : same suit, is LT, lead suit
        """
        trump = euchre.SPADE
        lead = euchre.HEART
        card_1 = card.Card(lead, euchre.JACK)
        card_2 = card.Card(lead, euchre.QUEEN)
        self.assertTrue(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_base_false_case_lead(self):
        """
        basic case : same suit, is GE, lead suit
        """
        trump = euchre.CLUB
        lead = euchre.DIAMOND
        card_1 = card.Card(lead, euchre.KING)
        card_2 = card.Card(lead, euchre.TEN)
        self.assertFalse(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_left_vs_right(self):
        """
        Confirm that left is less than right
        """
        trump = euchre.CLUB
        lead = euchre.SPADE
        card_1 = card.Card(lead, euchre.JACK)
        card_2 = card.Card(trump, euchre.JACK)
        self.assertTrue(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_right_vs_left(self):
        """
        Test that right is not less than left
        """
        trump = euchre.CLUB
        lead = euchre.SPADE
        card_1 = card.Card(trump, euchre.JACK)
        card_2 = card.Card(lead, euchre.JACK)
        self.assertFalse(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_is_trump(self):
        """
        Case where self is 9 of trump, beats out non-trump competitor
        """
        trump = euchre.DIAMOND
        lead = euchre.DIAMOND
        other = euchre.CLUB
        card_1 = card.Card(trump, euchre.NINE)
        card_2 = card.Card(other, euchre.ACE)
        self.assertFalse(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_is_not_trump(self):
        """
        Case where self loses to 9 of trump
        """
        trump = euchre.DIAMOND
        lead = euchre.DIAMOND
        other = euchre.CLUB
        card_1 = card.Card(other, euchre.NINE)
        card_2 = card.Card(trump, euchre.ACE)
        self.assertTrue(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_left_beats_suit_ace(self):
        """
        Case where the left beats the ace of its printed suit
        """
        trump = euchre.DIAMOND
        lead = euchre.DIAMOND
        card_1 = card.Card(euchre.LEFT_SUIT[trump], euchre.JACK)
        card_2 = card.Card(trump, euchre.ACE)
        self.assertFalse(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_right_beats_suit_ace(self):
        """
        Case where the right beats the ace of its printed suit
        """
        trump = euchre.DIAMOND
        lead = euchre.DIAMOND
        card_1 = card.Card(trump, euchre.JACK)
        card_2 = card.Card(trump, euchre.ACE)
        self.assertFalse(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_lead_beats_other(self):
        """
        Case where a match to leading suit results in GE.
        Neither card is trump.
        """
        trump = euchre.DIAMOND
        lead = euchre.SPADE
        card_1 = card.Card(lead, euchre.QUEEN)
        card_2 = card.Card(lead, euchre.NINE)
        self.assertFalse(card_1.lt_card(card_2, trump, lead))



    def test_lt_card_loses_to_lead(self):
        """
        Case where the other card matches leading suit, resulting in GE.
        Neither card is trump.
        """
        trump = euchre.DIAMOND
        lead = euchre.CLUB
        card_1 = card.Card(lead, euchre.TEN)
        card_2 = card.Card(lead, euchre.KING)
        self.assertTrue(card_1.lt_card(card_2, trump, lead))

    def test_lt_card_not_trump_not_lead_lt(self):
        """
        Case where cards are not in same suit, but neither are trump or
        the leading suit, and self is lt
        """
        trump = euchre.DIAMOND
        lead = euchre.CLUB
        other_1 = euchre.SPADE
        other_2 = euchre.HEART
        card_1 = card.Card(other_1, euchre.NINE)
        card_2 = card.Card(other_2, euchre.KING)
        self.assertTrue(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_not_trump_not_lead_ge(self):
        """
        Case where cards are not in same suit, but neither are trump or
        the leading suit, and self is ge
        """
        trump = euchre.DIAMOND
        lead = euchre.CLUB
        other_1 = euchre.SPADE
        other_2 = euchre.HEART
        card_1 = card.Card(other_1, euchre.ACE)
        card_2 = card.Card(other_2, euchre.QUEEN)
        self.assertFalse(card_1.lt_card(card_2, trump, lead))


    def test_lt_card_same(self):
        """
        Case where compared to same card - this isn't expected to occur,
        but we support it w/ undefined behavior.
        """
        trump = euchre.DIAMOND
        lead = euchre.CLUB
        card_1 = card.Card(trump, euchre.ACE)
        card_2 = card.Card(trump, euchre.ACE)
        self.assertIsInstance(card_1.lt_card(card_2, trump, lead), bool)
