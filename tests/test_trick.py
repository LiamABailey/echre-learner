import unittest

from game_assets import card, euchre, trick

class TestAddCard(unittest.TestCase):

    def setUp(self):
        self.trick = trick.Trick()

    def test_add_card_to_empty(self):
        """
        Add a card to an empty trick, check for correct leading suit &
        card in trick
        """
        first_card_suit = euchre.HEART
        first_card_seat = 2
        first_card = card.Card(first_card_suit, euchre.TEN)
        expected_cards = [trick.PlayedCard(first_card, first_card_seat)]
        self.trick.add_card(first_card, first_card_seat)

        self.assertEqual(self.trick.leading_suit, first_card_suit)
        self.assertEqual(self.trick.played_cards, expected_cards)

    def test_add_card_to_single(self):
        """
        Add a card to a trick containing one card
        """
        lead_suit = euchre.DIAMOND
        lead_card = card.Card(lead_suit, euchre.ACE)
        lead_seat = 0
        self.trick.leading_suit = lead_suit
        self.trick.played_cards = [trick.PlayedCard(lead_card, lead_seat)]

        second_card = card.Card(euchre.SPADE, euchre.NINE)
        second_seat = 1
        self.trick.add_card(second_card, second_seat)

        expected_cards = [trick.PlayedCard(lead_card, lead_seat),
                        trick.PlayedCard(second_card, second_seat)]
        self.assertEqual(self.trick.leading_suit, lead_suit)
        self.assertEqual(self.trick.played_cards, expected_cards)

    def test_add_card_to_fill(self):
        """
        Add a fourth card to a trick, filling it
        """
        lead_suit = euchre.DIAMOND
        first_3_cards = [
            card.Card(lead_suit, euchre.JACK),
            card.Card(euchre.SPADE, euchre.TEN),
            card.Card(lead_suit, euchre.ACE)
        ]
        first_3_seats = [2,3,0]
        self.trick.leading_suit = lead_suit
        self.trick.played_cards = [trick.PlayedCard(c, s) for c, s in zip(first_3_cards, first_3_seats)]

        last_card = card.Card(lead_suit, euchre.QUEEN)
        last_seat = 1
        self.trick.add_card(last_card, last_seat)

        expected_cards = first_3_cards  + [last_card]
        expected_seats = first_3_seats + [last_seat]
        expected_played_cards = [trick.PlayedCard(card, seat) for card, seat in zip(expected_cards, expected_seats)]
        self.assertEqual(self.trick.leading_suit, lead_suit)
        self.assertEqual(self.trick.played_cards, expected_played_cards)

    def test_add_card_low_seat(self):
        """
        Attempt to add a card w/ an lower-than-acceptable seat
        """
        low_seat = -1
        with self.assertRaises(ValueError):
            self.trick.add_card(card.Card(euchre.CLUB, euchre.KING), low_seat)

    def test_add_card_high_seat(self):
        """
        Attempt to add a card w/ an higher-than-acceptable seat
        """
        low_seat = euchre.NUM_PLAYERS + 1
        with self.assertRaises(ValueError):
            self.trick.add_card(card.Card(euchre.CLUB, euchre.KING), low_seat)


class TestScoreTrick(unittest.TestCase):

    def setUp(self):
        self.empty_trick = trick.Trick()
        self.trump_wins_trick = trick.Trick()
        trump_wins_cards = [
            card.Card(euchre.CLUB, euchre.ACE),
            card.Card(euchre.DIAMOND, euchre.TEN),
            card.Card(euchre.CLUB, euchre.QUEEN),
            card.Card(euchre.CLUB, euchre.KING)
        ]
        trump_wins_seat_order = [2,3,0,1]
        self.trump_wins_diamond_expected_seat = 3
        self.trump_wins_club_expected_seat = 2
        self.trump_wins_heart_expected_seat = 2
        for c, s in zip(trump_wins_cards, trump_wins_seat_order):
            self.trump_wins_trick.add_card(c, s)

    def test_score_trick_not_fully_played(self):
        """
        Assert error raised when not scoring a fully-played trick
        """
        trump_suit = euchre.DIAMOND
        with self.assertRaises(ValueError):
            self.empty_trick.score_trick(trump_suit)


    def test_score_trick_trump_wins(self):
        """
        Test of scoring for simple case - trump beats non-trump
        """
        self.trump_wins_trick.score_trick(euchre.DIAMOND)
        self.assertEqual(self.trump_wins_trick.winning_player, self.trump_wins_diamond_expected_seat)
