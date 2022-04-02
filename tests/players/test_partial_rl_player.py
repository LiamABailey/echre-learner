from dataclasses import dataclass
import unittest

from game_assets.players.partial_rl_player import RLTrickPlayer
from game_assets.card import Card
from game_assets.euchre import (CARD_FACES, FACE_DESCRIPTOR, LEFT_SUIT,
                                JACK, SUITS, SUIT_DESCRIPTOR, NUM_PLAYERS)


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
        @dataclass
        class ValidCase:
            agent_seat: int
            played_seat: int
            expected_result: float

        valid_cases = [
            ValidCase(0,0,1.),
            ValidCase(0,1,0.),
            ValidCase(0,3,2/3),
            ValidCase(2,0,1/3),
            ValidCase(1,3,1/3),
            ValidCase(3,0,0.)
        ]
        for i, vc in enumerate(valid_cases):
            with self.subTest(test = i):
                self.agent.assign_seat(vc.agent_seat)
                result_enc = self.agent._get_encoded_card_val(vc.played_seat)
                self.assertAlmostEqual(result_enc, vc.expected_result, 5)

    def test_get_encoded_card_val_oob(self):
        """
        Tests where the input is out of bounds
        """
        oob_inputs = [-100, -1, NUM_PLAYERS, NUM_PLAYERS + 1, 100]
        self.agent.assign_seat(0)
        for i, ps in enumerate(oob_inputs):
            with self.subTest(test = i):
                with self.assertRaises(ValueError) as te:
                    self.agent._get_encoded_card_val(ps)
                self.assertTrue("Expected play_seat in [0,3], received " in str(te.exception))

    def test_get_encoded_card_val_mistyped(self):
        """
        Tests where the input is an unsupported type
        """
        invalid_inputs = [True, False, 1.0, "1"]
        self.agent.assign_seat(0)
        for i, ps in enumerate(invalid_inputs):
            with self.subTest(test = i):
                with self.assertRaises(TypeError) as te:
                    self.agent._get_encoded_card_val(ps)
                self.assertTrue("Expected type(play_seat) = int, received" in str(te.exception))

    def test_get_encoded_card_val_mistype_unset_seat(self):
        """
        Test behavior where the agent's seat hasn't been assigned
        """
        play_seats = [0,1,2,3]
        for i, ps in enumerate(play_seats):
            with self.subTest(test = i):
                with self.assertRaises(TypeError) as te:
                    self.agent._get_encoded_card_val(ps)
                self.assertTrue(("unsupported operand type(s) for "
                    "-: 'int' and 'NoneType'") in str(te.exception))
