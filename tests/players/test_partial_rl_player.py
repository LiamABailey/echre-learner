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

    def test_positions_out_of_trump(self):
        """
        Tests for non-trump cards
        """
        for trump in SUITS:
            non_trumps = SUITS[:]
            non_trumps.remove(trump)
            for ntix, non_trump in enumerate(non_trumps):
                for fix, face in enumerate(CARD_FACES):
                    eval_card = Card(non_trump, face)
                    if eval_card.is_trump(trump):
                        # catch and ignore left bar
                        continue
                    with self.subTest(trump=SUIT_DESCRIPTOR[trump],
                                    non_trump=SUIT_DESCRIPTOR[non_trump],
                                    face=FACE_DESCRIPTOR[face]):
                        expected_position = 7 + (ntix * 6) + fix
                        self.assertEqual(\
                            RLTrickPlayer._get_card_repr_ix(eval_card, trump),
                            expected_position)


class TestGetEncodedCardVal(unittest.TestCase):

    def setUp(self):
        self.agent = RLTrickPlayer(0, None)

    def test_get_encoded_card_val_valid(self):
        """
        Tests where the input is valid
        """
        raise NotImplementedError

    def test_get_encoded_card_val_oob(self):
        """
        Tests where the input is out of bounds
        """
        raise NotImplementedError

    def test_get_encoded_card_val_mistyped(self):
        """
        Tests where the input is an unsupported type
        """
        raise NotImplementedError

    def test_get_encoded_card_val_mistype_unset_seat(self):
        """
        Test behavior where the agent's seat hasn't been assigned
        """
        play_seats = [0,1,2,3]
        for i, ps in enumerate(play_seats):
            with self.subTest(test = i):
                with self.assertRaises(TypeError) as ae:
                    self.agent._get_encoded_card_val(ps)
                self.assertTrue("unsupported operand type(s) for -: 'int' and 'NoneType'")
