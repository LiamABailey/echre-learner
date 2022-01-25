import unittest


from game_assets.players.random_player import RandomPlayer
from game_assets.table import Table
from game_assets.euchre import TEAM_ZERO_ID, TEAM_ONE_ID

class TestGetScores(unittest.TestCase):
    """
    Tests for get_scores method
    """

    def setUp(self):
        p1, p2, p3, p4 = [RandomPlayer(i) for i in range(4)]
        self.base_table = Table(p1, p2, p3, p4)

    def test_get_scores_zero_zero(self):
        """
        Basic test: confirms initalization at zero
        """
        expected = [0, 0]
        actual_scores = self.base_table.get_scores()
        self.assertEqual(expected, actual_scores)


    def test_get_scores_variable(self):
        """
        Test values across a collection of non-zero scores to check
        proper assignemnt
        """
        # scores in the order of team-zero, team-1
        score_pairs = [
            [0, 2],
            [3, 0],
            [4, 6]
        ]
        for score_pair in score_pairs:
            with self.subTest():
                self.base_table.scores[TEAM_ZERO_ID] = score_pair[0]
                self.base_table.scores[TEAM_ONE_ID] = score_pair[1]
                actual_scores = self.base_table.get_scores()
                self.assertEqual(score_pair, actual_scores)

"""
Additional unit tests not provided - behavior will be indirectly validated
by review. The author is aware that the above tests are not of particuarly
high value given the relatively static nature of this project.

See README.
"""
