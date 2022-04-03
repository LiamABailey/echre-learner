from dataclasses import dataclass
import unittest

from game_assets.players.partial_rl_player import RLTrickPlayer
from game_assets.card import Card
from game_assets import euchre
from game_assets.hand import Hand
from game_assets.trick import Trick


class TestGetCardReprIx(unittest.TestCase):
    """
    Unittests for the internal card indexing calculator.
    Due to the limited number of combinations, we test all.
    """

    def test_positions_trump_suit(self):
        """
        Tests where the card is in the trump suit
        """
        for trump in euchre.SUITS:
            for ix, face in enumerate(euchre.CARD_FACES):
                eval_card = Card(trump, face)
                with self.subTest(trump=euchre.SUIT_DESCRIPTOR[trump],
                                        face=euchre.FACE_DESCRIPTOR[face]):
                    self.assertEqual(\
                        RLTrickPlayer._get_card_repr_ix(eval_card, trump), ix)

    def test_positions_left_bar(self):
        """
        Tests of the left bar position
        """
        expected_position = 6
        for trump in euchre.SUITS:
            left_suit = euchre.LEFT_SUIT[trump]
            eval_card = Card(left_suit, euchre.JACK)
            with self.subTest(trump=euchre.SUIT_DESCRIPTOR[trump]):
                self.assertEqual(\
                    RLTrickPlayer._get_card_repr_ix(eval_card, trump),
                    expected_position)

    def test_positions_out_of_trump(self):
        """
        Tests for non-trump cards
        """
        for trump in euchre.SUITS:
            non_trumps = euchre.SUITS[:]
            non_trumps.remove(trump)
            for ntix, non_trump in enumerate(non_trumps):
                for fix, face in enumerate(euchre.CARD_FACES):
                    eval_card = Card(non_trump, face)
                    if eval_card.is_trump(trump):
                        # catch and ignore left bar
                        continue
                    with self.subTest(trump=euchre.SUIT_DESCRIPTOR[trump],
                                    non_trump=euchre.SUIT_DESCRIPTOR[non_trump],
                                    face=euchre.FACE_DESCRIPTOR[face]):
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
            ValidCase(0,1,0.25),
            ValidCase(0,3,0.75),
            ValidCase(2,0,0.5),
            ValidCase(1,3,0.5),
            ValidCase(3,0,0.25)
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
        oob_inputs = [-100, -1, euchre.NUM_PLAYERS, euchre.NUM_PLAYERS + 1, 100]
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

    def test_get_encoded_card_val_unset_seat(self):
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


class TestInitialPlayerEncoding(unittest.TestCase):

    def setUp(self):
        self.agent = RLTrickPlayer(0, None)

    def test_initial_player_encoding_valid(self):
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
            ValidCase(0,1,0),
            ValidCase(0,3,2/3),
            ValidCase(2,0,1/3),
            ValidCase(1,3,1/3),
            ValidCase(3,0,0)
        ]
        for i, vc in enumerate(valid_cases):
            with self.subTest(test = i):
                self.agent.assign_seat(vc.agent_seat)
                result_enc = self.agent._get_initial_player_encoding(vc.played_seat)
                self.assertAlmostEqual(result_enc, vc.expected_result, 5)

    def test_initial_player_encoding_oob(self):
        """
        Tests where the input is out of bounds
        """
        oob_inputs = [-100, -1, euchre.NUM_PLAYERS, euchre.NUM_PLAYERS + 1, 100]
        self.agent.assign_seat(0)
        for i, ps in enumerate(oob_inputs):
            with self.subTest(test = i):
                with self.assertRaises(ValueError) as te:
                    self.agent._get_initial_player_encoding(ps)
                self.assertTrue("Expected play_seat in [0,3], received " in str(te.exception))

    def test_initial_player_encoding_mistyped(self):
        """
        Tests where the input is an unsupported type
        """
        invalid_inputs = [True, False, 1.0, "1"]
        self.agent.assign_seat(0)
        for i, ps in enumerate(invalid_inputs):
            with self.subTest(test = i):
                with self.assertRaises(TypeError) as te:
                    self.agent._get_initial_player_encoding(ps)
                self.assertTrue("Expected type(play_seat) = int, received" in str(te.exception))

    def test_initial_player_encoding_unset_seat(self):
        """
        Test behavior where the agent's seat hasn't been assigned
        """
        play_seats = [0,1,2,3]
        for i, ps in enumerate(play_seats):
            with self.subTest(test = i):
                with self.assertRaises(TypeError) as te:
                    self.agent._get_initial_player_encoding(ps)
                self.assertTrue(("unsupported operand type(s) for "
                    "-: 'int' and 'NoneType'") in str(te.exception))


class TestGetStateRepr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Instantiate tricks, player-hands for use in testing
        """
        #  cards
        C_9 = Card(euchre.CLUB, euchre.NINE)
        D_10 = Card(euchre.DIAMOND, euchre.TEN)
        H_10 = Card(euchre.HEART, euchre.TEN)
        D_J = Card(euchre.DIAMOND, euchre.JACK)
        H_J = Card(euchre.HEART, euchre.JACK)
        S_J = Card(euchre.SPADE, euchre.JACK)
        C_Q = Card(euchre.CLUB, euchre.QUEEN)
        S_Q = Card(euchre.SPADE, euchre.QUEEN)
        D_K = Card(euchre.DIAMOND, euchre.KING)
        H_K = Card(euchre.HEART, euchre.KING)
        C_A = Card(euchre.CLUB, euchre.ACE)
        H_A = Card(euchre.HEART, euchre.ACE)

        # collections of cards for the player's hand
        cls.full_hand_1 = [C_9, D_10, H_J, D_K, H_K]
        cls.full_hand_2 = [D_J, H_J, D_10, S_Q, C_A]
        cls.p4_hand_1 = [H_10, S_J, C_Q, H_A]
        cls.p3_hand_1 = [D_J, C_Q, S_Q]
        cls.p2_hand_1 = [D_K, C_9]
        cls.p1_hand_1 = [H_10]
        cls.p1_hand_2 = [C_A]
        cls.p1_hand_3 = [S_J]
        # collections of completed tricks to
        # be loaded into the ongoing hand
        cls.complete_trick_1 = Trick()
        ct1_card_players = [(),(),(),()]
        for c in ct1_cards:
            cls.complete_trick_1.add_card(c[0],c[1])
        cls.complete_trick_2 = Trick()
        ct2_card_players = [(),(),(),()]
        for c in ct2_cards:
            cls.complete_trick_2.add_card(c[0],c[1])
        cls.completed_trick_3 = Trick()
        ct3_card_players = [(),(),(),()]
        for c in ct3_cards:
            cls.complete_trick_3.add_card(c[0],c[1])
        cls.completed_trick_4 = Trick()
        ct4_card_players = [(),(),(),()]
        for c in ct4_cards:
            cls.complete_trick_4.add_card(c[0],c[1])
        cls.completed_trick_5 = Trick()
        ct5_card_players = [(),(),(),()]
        for c in ct5_cards:
            cls.complete_trick_5.add_card(c[0],c[1])
        cls.completed_trick_6 = Trick()
        ct6_card_players = [(),(),(),()]
        for c in ct6_cards:
            cls.complete_trick_6.add_card(c[0],c[1])
        # collections of active tricks
        # no cards played
        cls.active_trick_c0_1 = Trick()
        # one card played
        cls.active_trick_c1_1 = Trick()
        cls.active_trick_c1_1.add_card()
        cls.active_trick_c1_2 = Trick()
        cls.active_trick_c1_2.add_card()
        cls.active_trick_c1_3 = Trick()
        cls.active_trick_c1_3.add_card()
        # two cards played
        cls.active_trick_c2_1 = Trick()
        cls.active_trick_c2_1.add_card()
        cls.active_trick_c2_1.add_card()
        cls.active_trick_c2_2 = Trick()
        cls.active_trick_c2_2.add_card()
        cls.active_trick_c2_2.add_card()
        # three_cards_played
        cls.active_trick_c3_1 = Trick()
        cls.active_trick_c3_1.add_card()
        cls.active_trick_c3_1.add_card()
        cls.active_trick_c3_1.add_card()
        cls.active_trick_c3_2 = Trick()
        cls.active_trick_c3_2.add_card()
        cls.active_trick_c3_2.add_card()
        cls.active_trick_c3_2.add_card()

    def setUp(self):
        """
        Instantiate new players for each test
        """
        self.agent = RLTrickPlayer(0, None)
