import unittest

from game_assets import euchre, hand, trick

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
        self.hand = hand.Hand(0, euchre.DIAMOND)
