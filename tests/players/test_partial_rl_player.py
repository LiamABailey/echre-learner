from dataclasses import dataclass
import os
import unittest


from numpy import loadtxt, ndarray, zeros
from numpy.testing import assert_allclose

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

    @staticmethod
    def load_state_csv(fname: str) -> ndarray:
        """
        Loads a 1d state representation from a provided csv

        Parameters
        ----------
            fname : str
                The name of the file to load

        Returns
        -------
            ndarray: the 1d array representing the state
        """
        fpath = os.path.join("tests","assets","players","partial_rl_player_states",fname)
        return loadtxt(fpath, delimiter = ',')

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
        ct1_card_players = [(C_9,2),(D_10,3),(H_J,0),(H_K,1)]
        for c in ct1_card_players:
            cls.complete_trick_1.add_card(c[0],c[1])
        cls.complete_trick_2 = Trick()
        ct2_card_players = [(H_A,0),(C_Q,1),(D_10,2),(H_J,3)]
        for c in ct2_card_players:
            cls.complete_trick_2.add_card(c[0],c[1])
        cls.complete_trick_3 = Trick()
        ct3_card_players = [(S_J,1),(C_Q,2),(S_Q,3),(C_9,0)]
        for c in ct3_card_players:
            cls.complete_trick_3.add_card(c[0],c[1])
        cls.complete_trick_4 = Trick()
        ct4_card_players = [(C_A,3),(D_K,0),(C_Q,1),(S_Q,2)]
        for c in ct4_card_players:
            cls.complete_trick_4.add_card(c[0],c[1])
        cls.complete_trick_5 = Trick()
        ct5_card_players = [(H_J,1),(S_J,2),(D_J,3),(S_Q,0)]
        for c in ct5_card_players:
            cls.complete_trick_5.add_card(c[0],c[1])
        cls.complete_trick_6 = Trick()
        ct6_card_players = [(H_10,2),(D_10,3),(D_K,0),(C_A,1)]
        for c in ct6_card_players:
            cls.complete_trick_6.add_card(c[0],c[1])
        # collections of active tricks
        # no cards played
        cls.active_trick_c0_1 = Trick()
        # one card played
        cls.active_trick_c1_1 = Trick()
        cls.active_trick_c1_1.add_card(S_J,1)
        cls.active_trick_c1_2 = Trick()
        cls.active_trick_c1_2.add_card(H_A,2)
        cls.active_trick_c1_3 = Trick()
        cls.active_trick_c1_3.add_card(H_J,3)
        # two cards played
        cls.active_trick_c2_1 = Trick()
        cls.active_trick_c2_1.add_card(D_10,0)
        cls.active_trick_c2_1.add_card(D_J,1)
        cls.active_trick_c2_2 = Trick()
        cls.active_trick_c2_2.add_card(H_K,2)
        cls.active_trick_c2_2.add_card(H_A,3)
        # three_cards_played
        cls.active_trick_c3_1 = Trick()
        cls.active_trick_c3_1.add_card(D_10,3)
        cls.active_trick_c3_1.add_card(D_J,0)
        cls.active_trick_c3_1.add_card(C_Q,1)
        cls.active_trick_c3_2 = Trick()
        cls.active_trick_c3_2.add_card(S_Q,1)
        cls.active_trick_c3_2.add_card(C_A,2)
        cls.active_trick_c3_2.add_card(H_K,3)

    def test_get_state_repr_trick1_lead(self):
        """
        Tests where the agent has a full hand, and no cards
        have been played yet (agent starts)
        """
        lead_cases = [
            {
                'agent_hand': self.full_hand_1,
                'agent_seat': 0,
                'trump_suit': euchre.SPADE,
                'expected_encoding': self.load_state_csv("trick1_lead_case0.csv")
            },
            {
                'agent_hand': self.full_hand_1,
                'agent_seat': 1,
                'trump_suit': euchre.DIAMOND,
                'expected_encoding': self.load_state_csv("trick1_lead_case1.csv")
            },
            {
                'agent_hand': self.full_hand_2,
                'agent_seat': 2,
                'trump_suit': euchre.HEART,
                'expected_encoding': self.load_state_csv("trick1_lead_case2.csv")
            },
            {
                'agent_hand': self.full_hand_2,
                'agent_seat': 3,
                'trump_suit': euchre.CLUB,
                'expected_encoding': self.load_state_csv("trick1_lead_case3.csv")
            },
        ]
        active_trick = Trick()
        for i, lc in enumerate(lead_cases):
            trial_agent = RLTrickPlayer(0, None)
            trial_agent.assign_seat(lc['agent_seat'])
            trial_agent.receive_cards(lc['agent_hand'])
            # construct the hand
            active_hand = Hand(0, lc['trump_suit'], None, None)
            with self.subTest(test = i):
                # construct state
                result_state = trial_agent._get_state_repr(active_hand, active_trick)
                assert_allclose(result_state, lc['expected_encoding'], atol=0.01)

    def test_get_state_repr_trick1_nonlead(self):
        """
        Tests where the agent has a full hand, and the first trick is
        ongoing (agent did not start)
        """
        nonlead_cases = [
            {
                'agent_hand': self.full_hand_1,
                'agent_seat': 0,
                'trump_suit': euchre.CLUB,
                'active_trick': self.active_trick_c1_1,
                'expected_encoding': self.load_state_csv("trick1_nonlead_case0.csv")
            },
            {
                'agent_hand': self.full_hand_1,
                'agent_seat': 1,
                'trump_suit': euchre.DIAMOND,
                'active_trick': self.active_trick_c1_3,
                'expected_encoding': self.load_state_csv("trick1_nonlead_case1.csv")
            },
            {
                'agent_hand': self.full_hand_2,
                'agent_seat': 2,
                'trump_suit': euchre.HEART,
                'active_trick': self.active_trick_c2_1,
                'expected_encoding': self.load_state_csv("trick1_nonlead_case2.csv")
            },
            {
                'agent_hand': self.full_hand_2,
                'agent_seat': 3,
                'trump_suit': euchre.SPADE,
                'active_trick': self.active_trick_c3_1,
                'expected_encoding': self.load_state_csv("trick1_nonlead_case3.csv")
            },
        ]
        for i, lc in enumerate(nonlead_cases):
            trial_agent = RLTrickPlayer(0, None)
            trial_agent.assign_seat(lc['agent_seat'])
            trial_agent.receive_cards(lc['agent_hand'])
            # construct the hand
            active_hand = Hand(0, lc['trump_suit'], None, None)
            with self.subTest(test = i):
                # construct state
                result_state = trial_agent._get_state_repr(active_hand, lc['active_trick'])
                assert_allclose(result_state, lc['expected_encoding'], atol=0.01)

    def test_get_state_repr_multi_trick(self):
        """
        validate performance of state encoding as the game is underway
        """
        underway_cases = [
            {
                'agent_hand': self.p4_hand_1,
                'agent_seat': 2,
                'trump_suit': euchre.HEART,
                'active_trick': self.active_trick_c1_3,
                'played_tricks': [self.complete_trick_1],
                'expected_encoding': self.load_state_csv("underway_case1.csv")
            },
            {
                'agent_hand': self.p3_hand_1,
                'agent_seat': 1,
                'trump_suit': euchre.CLUB,
                'active_trick': self.active_trick_c2_2,
                'played_tricks': [self.complete_trick_2, self.complete_trick_3],
                'expected_encoding': self.load_state_csv("underway_case2.csv")
            },
            {
                'agent_hand': self.p2_hand_1,
                'agent_seat': 0,
                'trump_suit': euchre.SPADE,
                'active_trick': self.active_trick_c3_1,
                'played_tricks': [self.complete_trick_4, self.complete_trick_5, self.complete_trick_6],
                'expected_encoding': self.load_state_csv("underway_case3.csv")
            }
        ]
        for i, uc in enumerate(underway_cases):
            trial_agent = RLTrickPlayer(0, None)
            trial_agent.assign_seat(uc['agent_seat'])
            trial_agent.cards_held = uc['agent_hand']
            # construct the hand
            active_hand = Hand(0, uc['trump_suit'], None, None)
            for t in uc['played_tricks']:
                active_hand.add_trick(t)
            with self.subTest(test = i):
                # construct state
                result_state = trial_agent._get_state_repr(active_hand, uc['active_trick'])
                assert_allclose(result_state, uc['expected_encoding'], atol=0.01)

    def test_get_state_repr_last_trick(self):
        """
        state encoding where the last trick is being played (only one card
        remains in the agent's hand)
        """
        underway_cases = [
            {
                'agent_hand': self.p1_hand_1,
                'agent_seat': 3,
                'trump_suit': euchre.HEART,
                'active_trick': self.active_trick_c1_1,
                'played_tricks': [self.complete_trick_1, self.complete_trick_2,
                                self.complete_trick_3, self.complete_trick_4],
                'expected_encoding': self.load_state_csv("last_trick_case0.csv")
            },
            {
                'agent_hand': self.p1_hand_2,
                'agent_seat': 1,
                'trump_suit': euchre.SPADE,
                'active_trick': self.active_trick_c2_1,
                'played_tricks': [self.complete_trick_6, self.complete_trick_5,
                                self.complete_trick_3, self.complete_trick_1],
                'expected_encoding': self.load_state_csv("last_trick_case1.csv")
            },
            {
                'agent_hand': self.p1_hand_3,
                'agent_seat': 0,
                'trump_suit': euchre.CLUB,
                'active_trick': self.active_trick_c3_2,
                'played_tricks': [self.complete_trick_2, self.complete_trick_4,
                                self.complete_trick_6, self.complete_trick_5],
                'expected_encoding': self.load_state_csv("last_trick_case2.csv")
            }
        ]
        for i, uc in enumerate(underway_cases):
            trial_agent = RLTrickPlayer(0, None)
            trial_agent.assign_seat(uc['agent_seat'])
            trial_agent.cards_held = uc['agent_hand']
            # construct the hand
            active_hand = Hand(0, uc['trump_suit'], None, None)
            for t in uc['played_tricks']:
                active_hand.add_trick(t)
            with self.subTest(test = i):
                # construct state
                result_state = trial_agent._get_state_repr(active_hand, uc['active_trick'])
                assert_allclose(result_state, uc['expected_encoding'], atol=0.01)

    def test_get_state_repr_all_complete(self):
        """
        Tests where all players have played five cards (no cards in hand
        for the agent)
        """
        complete_cases = [
            {
                'agent_seat': 0,
                'trump_suit': euchre.DIAMOND,
                'active_trick': self.complete_trick_1,
                'played_tricks': [self.complete_trick_5, self.complete_trick_4,
                                self.complete_trick_3, self.complete_trick_2],
                'expected_encoding': self.load_state_csv("complete_case0.csv")
            },
            {
                'agent_seat': 2,
                'trump_suit': euchre.SPADE,
                'active_trick': self.complete_trick_2,
                'played_tricks': [self.complete_trick_4, self.complete_trick_6,
                                self.complete_trick_1, self.complete_trick_3],
                'expected_encoding': self.load_state_csv("complete_case01.csv")
            },
            {
                'agent_seat': 1,
                'trump_suit': euchre.CLUB,
                'active_trick': self.complete_trick_6,
                'played_tricks': [self.complete_trick_1, self.complete_trick_3,
                                self.complete_trick_2, self.complete_trick_5],
                'expected_encoding': self.load_state_csv("complete_case2.csv")
            }
        ]
        for i, cc in enumerate(complete_cases):
            trial_agent = RLTrickPlayer(0, None)
            trial_agent.assign_seat(cc['agent_seat'])
            trial_agent.cards_held = []
            active_hand = Hand(0, cc['trump_suit'], None, None)
            for t in cc['played_tricks']:
                active_hand.add_trick(t)
            with self.subTest(test = i):
                raise NotImplementedError
                result_state = trial_agent._get_state_repr(active_hand, cc['active_trick'])
                assert_allclose(result_state, cc['expected_encoding'], atol=0.01)

    def test_get_state_repr_empty(self):
        """
        Base case with empty hand, active trick, and agent has no cards
        """
        trial_agent = RLTrickPlayer(0, None)
        trial_agent.assign_seat(0)
        active_hand = Hand(0, euchre.SPADE, None, None)
        active_trick = Trick()

        expected_state = zeros(155)
        # if no cards have been played, the agent assumes it must be going first
        expected_state[25] = 1

        result_state = trial_agent._get_state_repr(active_hand, active_trick)
        assert_allclose(result_state, expected_state)
