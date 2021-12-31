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
        self.test_trick_1 = trick.Trick()
        test_trick_1_cards = [
            card.Card(euchre.CLUB, euchre.ACE),
            card.Card(euchre.DIAMOND, euchre.TEN),
            card.Card(euchre.CLUB, euchre.QUEEN),
            card.Card(euchre.CLUB, euchre.KING)
        ]
        test_trick_1_order = [2,3,0,1]
        self.test_trick_1_diamond_expected_win_seat = 3
        self.test_trick_1_club_expected_win_seat = 2
        self.test_trick_1_heart_expected_win_seat = 2
        for c, s in zip(test_trick_1_cards, test_trick_1_order):
            self.test_trick_1.add_card(c, s)

        self.test_trick_2 = trick.Trick()
        test_trick_2_cards = [
            card.Card(euchre.CLUB, euchre.QUEEN),
            card.Card(euchre.SPADE, euchre.JACK),
            card.Card(euchre.CLUB, euchre.JACK),
            card.Card(euchre.HEART, euchre.NINE)
        ]
        test_trick_2_order = [3,0,1,2]
        self.test_trick_2_spade_expected_win_seat = 0
        self.test_trick_2_club_expected_win_seat = 1
        self.test_trick_2_heart_expected_win_seat = 2
        self.test_trick_2_diamond_expected_win_seat = 3
        for c, s in zip(test_trick_2_cards, test_trick_2_order):
            self.test_trick_2.add_card(c, s)

        self.test_trick_3 = trick.Trick()
        test_trick_3_cards = [
            card.Card(euchre.DIAMOND, euchre.TEN),
            card.Card(euchre.SPADE, euchre.KING),
            card.Card(euchre.CLUB, euchre.JACK),
            card.Card(euchre.SPADE, euchre.ACE)
        ]
        test_trick_3_order = [0,1,2,3]
        self.test_trick_3_spade_expected_win_seat = 2
        self.test_trick_3_club_expected_win_seat = 2
        self.test_trick_3_heart_expected_win_seat = 0
        self.test_trick_3_diamond_expected_win_seat = 0
        for c, s in zip(test_trick_3_cards, test_trick_3_order):
            self.test_trick_3.add_card(c, s)


    def test_score_trick_not_fully_played(self):
        """
        Assert error raised when not scoring a fully-played trick
        """
        trump_suit = euchre.DIAMOND
        with self.assertRaises(ValueError):
            self.empty_trick.score_trick(trump_suit)

    def test_score_trick_test_trick_1_diamond(self):
        """
        Test of scoring for simple case - trump beats non-trump
        """
        self.test_trick_1.score_trick(euchre.DIAMOND)
        self.assertEqual(self.test_trick_1.winning_player, self.test_trick_1_diamond_expected_win_seat)

    def test_score_trick_test_trick_1_club(self):
        """
        Test of scoring - lead wins by size w/in trump
        """
        self.test_trick_1.score_trick(euchre.CLUB)
        self.assertEqual(self.test_trick_1.winning_player, self.test_trick_1_club_expected_win_seat)

    def test_score_trick_test_trick_1_heart(self):
        """
        No trump cards played, high card wins
        """
        self.test_trick_1.score_trick(euchre.HEART)
        self.assertEqual(self.test_trick_1.winning_player, self.test_trick_1_heart_expected_win_seat)

    def test_score_trick_test_trick_2_club(self):
        """
        Test of scoring for right beats left, when left played first
        """
        self.test_trick_2.score_trick(euchre.CLUB)
        self.assertEqual(self.test_trick_2.winning_player, self.test_trick_2_club_expected_win_seat)

    def test_score_trick_test_trick_2_spade(self):
        """
        Test of scoring for right beats left, when right played first
        """
        self.test_trick_2.score_trick(euchre.SPADE)
        self.assertEqual(self.test_trick_2.winning_player, self.test_trick_2_spade_expected_win_seat)

    def test_score_trick_test_trick_2_heart(self):
        """
        Test of scoring for low red card beating black cards
        """
        self.test_trick_2.score_trick(euchre.HEART)
        self.assertEqual(self.test_trick_2.winning_player, self.test_trick_2_heart_expected_win_seat)

    def test_score_trick_test_trick_2_diamond(self):
        """
        Test of scoring: no trump played, lead wins
        """
        self.test_trick_2.score_trick(euchre.DIAMOND)
        self.assertEqual(self.test_trick_2.winning_player, self.test_trick_2_diamond_expected_win_seat)

    def test_score_trick_test_trick_3_heart(self):
        """
        Test of scoring for lead wins when no trump played, despite being the lowest face value
        """
        self.test_trick_3.score_trick(euchre.HEART)
        self.assertEqual(self.test_trick_3.winning_player, self.test_trick_3_heart_expected_win_seat)

    def test_score_trick_test_trick_3_spade(self):
        """
        Test of scoring for left beating ace/king
        """
        self.test_trick_3.score_trick(euchre.SPADE)
        self.assertEqual(self.test_trick_3.winning_player, self.test_trick_3_spade_expected_win_seat)
