import unittest

from game_assets import euchre, hand, trick, euchre

class TestAddTrick(unittest.TestCase):

    def setUp(self):
        self.hand = hand.Hand(0, euchre.DIAMOND)

        def test_add_trick_empty_hand(self):
            """
            Add a trick to an empty hand
            """
            self.hand.add_trick(trick.Trick())
            expected = hand.Hand()
            expected.tricks.append(trick.Trick())

            self.assertEqual(self.hand, expected)

        def test_add_trick_partial_hand(self):
            """
            Add a trick to a non-empty hand
            """
            self.hand.append(trick.Trick())
            self.hand.add_trick(trick.Trick())
            expected = hand.Hand()
            expected.tricks.extend([trick.Trick(), trick.Trick()])

            self.assertEqual(self.hand, expected)

        def test_add_trick_overfull_hand(self):
            """
            Add a trick to a hand at the hand size to encounter
            and exception
            """
            for _ in range(euchre.NUM_TRICKS):
                self.hand.append(trick.Trick())

            with self.assertRaises(ValueError):
                self.hand.add_trick(trick.Trick())


class TestCalcPoints(unittest.TestCase):

    def test_calc_points_zero_bidder(self):
        """
        Test _calc_points where 0 tricks won, did bid
        """
        self.assertEqual(hand.Hand._calc_points(0, True), 0)

    def test_calc_points_one_bidder(self):
        """
        Test _calc_points where 1 trick won, did bid
        """
        self.assertEqual(hand.Hand._calc_points(1, True), 0)

    def test_calc_points_two_bidder(self):
        """
        Test _calc_points where 2 tricks won, did bid
        """
        self.assertEqual(hand.Hand._calc_points(2, True), 0)

    def test_calc_points_three_bidder(self):
        """
        Test _calc_points where 3 tricks won, did bid
        """
        self.assertEqual(hand.Hand._calc_points(3, True), 1)

    def test_calc_points_four_bidder(self):
        """
        Test _calc_points where 4 tricks won, did bid
        """
        self.assertEqual(hand.Hand._calc_points(4, True), 1)

    def test_calc_points_five_bidder(self):
        """
        Test _calc_points where 5 tricks won, did bid
        """
        self.assertEqual(hand.Hand._calc_points(5, True), 2)

    def test_calc_points_zero_not_bidder(self):
        """
        Test _calc_points where 0 tricks won, didn't bid
        """
        self.assertEqual(hand.Hand._calc_points(0, False), 0)

    def test_calc_points_one_not_bidder(self):
        """
        Test _calc_points where 1 trick won, didn't bid
        """
        self.assertEqual(hand.Hand._calc_points(1, False), 0)

    def test_calc_points_two_not_bidder(self):
        """
        Test _calc_points where 2 tricks won, didn't bid
        """
        self.assertEqual(hand.Hand._calc_points(2, False), 0)

    def test_calc_points_three_not_bidder(self):
        """
        Test _calc_points where 3 tricks won, didn't bid
        """
        self.assertEqual(hand.Hand._calc_points(3, False), 2)

    def test_calc_points_four_not_bidder(self):
        """
        Test _calc_points where 4 tricks won, didn't bid
        """
        self.assertEqual(hand.Hand._calc_points(4, False), 2)

    def test_calc_points_five_not_bidder(self):
        """
        Test _calc_points where 5 tricks won, didn't bid
        """
        self.assertEqual(hand.Hand._calc_points(5, False), 2)


class TestScoreHand(unittest.TestCase):

    def setUp(self):
        """
        Construct tricks for adding to hands
        """
        t0_win_trick = trick.Trick()
        t0_win_trick.winning_player = euchre.TEAM_ZERO[0]
        t1_win_trick = trick.Trick()
        t1_win_trick.winning_player = euchre.TEAM_ONE[0]

        self.t0_win3_tricks = [
            t0_win_trick,
            t0_win_trick,
            t1_win_trick,
            t0_win_trick,
            t1_win_trick
        ]
        self.t0_win_4_tricks = [t0_win_trick] * 3 + [t1_win_trick, t0_win_trick]
        self.t0_win_5_tricks = [t0_win_trick] * 5
        self.t1_win3_tricks = [
            t0_win_trick,
            t1_win_trick,
            t1_win_trick,
            t0_win_trick,
            t1_win_trick
        ]
        self.t1_win_5_tricks = [t1_win_trick] * 5
        self.four_tricks = [t0_win_trick] * 4

        unscored_trick = trick.Trick()
        self.last_trick_unscored = [t1_win_trick] * 4 + [unscored_trick]

    def test_score_hand_team_zero_three_bidder(self):
        """
        Test score hand when team zero wins w/ 3 tricks, is bidder
        """
        t0_win_3 = hand.Hand(0, euchre.DIAMOND)
        t0_win_3.tricks = self.t0_win3_tricks
        expected = hand.Hand(0, euchre.DIAMOND)
        expected.tricks = self.t0_win3_tricks
        expected.winning_team = euchre.TEAM_ZERO_ID
        expected.points = 1

        t0_win_3.score_hand()
        self.assertEqual(t0_win_3, expected)


    def test_score_hand_team_zero_four_bidder(self):
        """
        Test score hand when team zero wins w/ 4 tricks, is bidder
        """
        t0_win_4 = hand.Hand(0, euchre.HEART)
        t0_win_4.tricks = self.t0_win_4_tricks
        expected = hand.Hand(0, euchre.HEART)
        expected.tricks = self.t0_win_4_tricks
        expected.winning_team = euchre.TEAM_ZERO_ID
        expected.points = 1

        t0_win_4.score_hand()
        self.assertEqual(t0_win_4, expected)

    def test_score_hand_team_zero_three_not_bidder(self):
        """
        Test score hand when team zero wins w/ 3 tricks, not bidder
        """
        t0_win_3_nb = hand.Hand(1, euchre.CLUB)
        t0_win_3_nb.tricks = self.t0_win3_tricks
        expected = hand.Hand(1, euchre.CLUB)
        expected.tricks = self.t0_win3_tricks
        expected.winning_team = euchre.TEAM_ZERO_ID
        expected.points = 2

        t0_win_3_nb.score_hand()
        self.assertEqual(t0_win_3_nb, expected)

    def test_score_hand_team_one_three(self):
        """
        Test score hand when team one wins w/ 3 tricks
        """
        t1_win_3 = hand.Hand(1, euchre.SPADE)
        t1_win_3.tricks = self.t1_win3_tricks
        expected = hand.Hand(1, euchre.SPADE)
        expected.tricks = self.t1_win3_tricks
        expected.winning_team = euchre.TEAM_ONE_ID
        expected.points = 1

        t1_win_3.score_hand()
        self.assertEqual(t1_win_3, expected)

    def test_score_hand_team_zero_five_bidder(self):
        """
        Test score hand when team zero wins w/ 5 tricks, is bidder
        """
        t0_win_5 = hand.Hand(2, euchre.CLUB)
        t0_win_5.tricks = self.t0_win_5_tricks
        expected = hand.Hand(2, euchre.CLUB)
        expected.tricks = self.t0_win_5_tricks
        expected.winning_team = euchre.TEAM_ZERO_ID
        expected.points = 2

        t0_win_5.score_hand()
        self.assertEqual(t0_win_5, expected)

    def test_score_hand_team_zero_five_not_bidder(self):
        """
        Test score hand when team zero wins w/ 5 tricks, isn't bidder
        """
        t0_win_5_nb = hand.Hand(3, euchre.CLUB)
        t0_win_5_nb.tricks = self.t0_win_5_tricks
        expected = hand.Hand(3, euchre.CLUB)
        expected.tricks = self.t0_win_5_tricks
        expected.winning_team = euchre.TEAM_ZERO_ID
        expected.points = 2

        t0_win_5_nb.score_hand()
        self.assertEqual(t0_win_5_nb, expected)


    def test_score_hand_team_one_five(self):
        """
        Test score hand when team one wins w/ 5 tricks
        """
        t1_win_5 = hand.Hand(3, euchre.DIAMOND)
        t1_win_5.tricks = self.t1_win_5_tricks
        expected = hand.Hand(3, euchre.DIAMOND)
        expected.tricks = self.t1_win_5_tricks
        expected.winning_team = euchre.TEAM_ONE_ID
        expected.points = 2

    def test_score_hand_premature(self):
        """
        Validate exception behavior when attempting to score a hand
        where one of
        """
        short_hand = hand.Hand(0, euchre.CLUB)
        short_hand.tricks = self.four_tricks

        with self.assertRaises(ValueError):
            short_hand.score_hand()

    def test_score_hand_unscored_trick(self):
        """
        Validate exception behavior when attempting to score
        a hand where one of the tricks is unscored
        """
        unscored_trick_hand = hand.Hand(1, euchre.HEART)
        unscored_trick_hand.tricks = self.last_trick_unscored

        with self.assertRaises(trick.UnscoredTrickException):
            unscored_trick_hand.score_hand()
