import unittest
from game_assets.players.partial_rl_player import RLTrickPlayer
from game_assets.card import Card
from game_assets.euchre import (CARD_FACES, FACE_DESCRIPTOR, LEFT_SUIT,
                                JACK, SUITS, SUIT_DESCRIPTOR)

class TestGetCardReprIx(unittest.TestCase):
    """
    Unittests for the internal card indexing calculator.
    Due to the limited number of combinations, we test all.
    """

    def test_positions_trump_suit(self):
        """
        Tests where the card is in the trump suit
        """
        for trump in SUITS:
            for ix, face in enumerate(CARD_FACES):
                eval_card = Card(trump, face)
                with self.subTest(trump=SUIT_DESCRIPTOR[trump],
                                        face=FACE_DESCRIPTOR[face]):
                    self.assertEqual(\
                        RLTrickPlayer._get_card_repr_ix(eval_card, trump), ix)

    def test_positions_left_bar(self):
        """
        Tests of the left bar position
        """
        expected_position = 6
        for trump in SUITS:
            left_suit = LEFT_SUIT[trump]
            eval_card = Card(left_suit, JACK)
            with self.subTest(trump=SUIT_DESCRIPTOR[trump]):
                self.assertEqual(\
                    RLTrickPlayer._get_card_repr_ix(eval_card, trump),
                    expected_position)
