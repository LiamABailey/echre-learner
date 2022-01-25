"""
Testing stochastic behavior is tricky, as it's hard to guarantee behavior. Different
methods have their drawbacks:
- Mocking radomness functions: Can break under code changes
- Statistical testing of output distributions: Noisy - expect false positives at a rate of alpha
- Boundary setting: Essentially a weaker version of statistical testing, with the potential for fewer FP

For now, I'm using the first and third methods above, but other options will be researched. Tests
of these simple methods serve *primarily* as testing practice, although some pieces of
behavior checking are valuable (e.g. 'doesn't return suit of kitty', `properly discards card`)
"""

from itertools import product
from random import shuffle, choice
from typing import List
import unittest
from unittest.mock import patch

from game_assets.card import Card
from game_assets.euchre import SUITS, CARD_FACES
from game_assets.players.random_player import RandomPlayer


class ProportionAssert:
    def assertCollectionProportionGreater(self, values: List[float], required_prop: float):
        """
        Assert that all values in values are greater than required_prop,
        and that they sum to one

        Parameters
        ----------
            values : List[float]
                The values under test

            required_prop : float
                The minimum value accepted.
        """
        for v in values:
            if v <= required_prop:
                raise AssertionError(f"{v} is less than {required_prop}")
        self.assertAlmostEqual(sum(values), 1, places = 5)


class TestExchangeWithKitty(unittest.TestCase, ProportionAssert):
    """
    Unittests for validating the exchange_with_kitty
    method of random player. Due to the relatively
    low complexity of the behavior, we randomly sample
    a large number of draws, and then validate
    that the distribution of returned cards is sufficiently uniform
    (here, defined as all cards being returned greater than 3% of the time)
    """

    def setUp(self):
        """
        Prepare assets for test
        """
        self.random_player = RandomPlayer(0)
        self.n_tests = 100000
        self.card_prop_threshold = 0.03
        self.deck = [Card(suit, face) for suit, face in product(SUITS, CARD_FACES)]
        shuffle(self.deck)

    def test_exchange_with_kitty(self):
        """
        Repeated testing of exchange_with_kitty
        to observe removed_card + proper hand after removal.

        Over a sufficiently large sample, we expect the distribution
        of returned cards to be uniform.

        Performing many trials supports the validation of two reqiurements:
            a. Returned cards are truly randomly distributed (uniform)
            b. The process operates correctly, regardless of cards in hand or kitty.
        """
        # construct card tracker
        returned_cards = {
            card_id:0 for card_id in product(SUITS, CARD_FACES)
        }
        for _ in range(self.n_tests):
            self.random_player.receive_cards(self.deck[:5])
            kitty_card = self.deck[5]
            returned_card = self.random_player.exchange_with_kitty(kitty_card)
            # assert appropriate behavior
            self.assertNotEqual(kitty_card, returned_card)
            self.assertEqual(len(self.random_player.cards_held), 5)
            self.assertCountEqual(self.random_player.cards_held + [returned_card], self.deck[:6])
            self.assertTrue(kitty_card in self.random_player.cards_held)
            # track the returned card
            returned_cards[(returned_card.suit, returned_card.face)] += 1
            # shuffle the deck
            shuffle(self.deck)
        #
        self.assertCollectionProportionGreater([v/self.n_tests for v in returned_cards.values()],
                                        self.card_prop_threshold)


class TestSelectKittyPickup(unittest.TestCase):
    """
    Tests that kitty pick up, performed via reference to random.random(), is
    bounded within an acceptable range. (This could be done via inspection,
    but is included as a thought exercise, as for more complex behavior inspection
    may not suffice)
    """

    def assertCardPickProp(self):
        for k in self.seen_kitty_cards:
            prop_pickup = self.pickup_kitty_cards[k]/self.seen_kitty_cards[k]
            self.assertGreater(prop_pickup, self.pickup_kitty_prop_min)
            self.assertLess(prop_pickup, self.pickup_kitty_prop_min)

    def setUp(self):
        """
        Set up the player
        """
        self.random_player = RandomPlayer(0)
        self.low_thresh = 0.1
        self.high_thresh = 0.9
        self.deck = [Card(suit, face) for suit, face in product(SUITS, CARD_FACES)]
        self.random_patch_loc = "game_assets.players.random_player.random"
        shuffle(self.deck)

    def test_select_kitty_pickup_dealer_nopick(self):
        """
        Validate that a pickup signal of 'false' is returned at a high threshold
        when player is dealer
        """
        kitty_card = self.deck[5]
        with patch(self.random_patch_loc, return_value = self.high_thresh):
            pick_up_signal = self.random_player.select_kitty_pickup(kitty_card,
                                                                    True,
                                                                    True)
        self.assertFalse(pick_up_signal)

    def test_select_kitty_pickup_partdealer_pick(self):
        """
        Validate that a pickup signal of 'true' is returned at a low threshold
        when player is dealer
        """

        kitty_card = self.deck[5]
        with patch(self.random_patch_loc, return_value = self.low_thresh):
            pick_up_signal = self.random_player.select_kitty_pickup(kitty_card,
                                                                    True,
                                                                    True)
        self.assertTrue(pick_up_signal)


    def test_select_kitty_pickup_partner_dealer_nopick(self):
        """
        Validate that a pickup signal of 'false' is returned at a high threshold
        when partner is dealer
        """

        kitty_card = self.deck[5]
        with patch(self.random_patch_loc, return_value = self.high_thresh):
            pick_up_signal = self.random_player.select_kitty_pickup(kitty_card,
                                                                    False,
                                                                    True)
        self.assertFalse(pick_up_signal)

    def test_select_kitty_pickup_partner_dealer_pick(self):
        """
        Validate that a pickup signal of 'true' is returned at a low threshold
        when partner is dealer
        """

        kitty_card = self.deck[5]
        with patch(self.random_patch_loc, return_value = self.low_thresh):
            pick_up_signal = self.random_player.select_kitty_pickup(kitty_card,
                                                                    False,
                                                                    True)
        self.assertTrue(pick_up_signal)

    def test_select_kitty_pickup_opponent_dealer_nopick(self):
        """
        Validate that a pickup signal of 'false' is returned at a high threshold
        when a player on the opposing team is the dealer
        """

        kitty_card = self.deck[5]
        with patch(self.random_patch_loc, return_value = self.high_thresh):
            pick_up_signal = self.random_player.select_kitty_pickup(kitty_card,
                                                                    False,
                                                                    False)
        self.assertFalse(pick_up_signal)

    def test_select_kitty_pickup_opponent_dealer_pick(self):
        """
        Validate that a pickup signal of 'true' is returned at a low threshold
        when a player on the opposing team is the dealer
        """

        kitty_card = self.deck[5]
        with patch(self.random_patch_loc, return_value = self.low_thresh):
            pick_up_signal = self.random_player.select_kitty_pickup(kitty_card,
                                                                    False,
                                                                    False)
        self.assertTrue(pick_up_signal)

class TestSelectTrump(unittest.TestCase, ProportionAssert):
    """
    The random agent will select a trump 25% of the time (100% of the time if
    stuck), and then selects that trump at random.
    """

    def setUp(self):
        """
        Set up the player
        """
        self.random_player = RandomPlayer(0)
        self.n_tests = 100000
        self.selected_trump = {
            i:0 for i in SUITS
        }
        self.suit_prop_threshold = 0.22

    def test_select_trump_dealer(self):
        """
        Test select trump when the player is the dealer (stuck)
        """
        # perform n tests
        for _ in range(self.n_tests):
            passed_card = Card(choice(SUITS), choice(CARD_FACES))
            suit, picked = self.random_player.select_trump(passed_card, True)
            self.assertTrue(picked)
            # enforce that the passed suit wasn't selected
            self.assertNotEqual(suit, passed_card.suit)
            self.selected_trump[suit] += 1
        # look for random distribution of suit regardless of card passed
        self.assertCollectionProportionGreater([v/self.n_tests for v in self.selected_trump.values()],
                                        self.suit_prop_threshold)


    def test_select_trump_not_dealer(self):
        """
        Test trump selection when not dealer. Does not enforce a fixed
        selection rate of trump, but does validate at least a 10% pass rate
        """
        n_passed = 0
        for _ in range(self.n_tests):
            passed_card = Card(choice(SUITS), choice(CARD_FACES))
            suit, picked = self.random_player.select_trump(passed_card, False)
            if picked:
                self.assertNotEqual(suit, passed_card.suit)
                self.selected_trump[suit] += 1
            else:
                n_passed += 1

        self.assertGreater(n_passed/self.n_tests, 0.1)
        self.assertCollectionProportionGreater([v/(self.n_tests - n_passed) for v in self.selected_trump.values()],
                                        self.suit_prop_threshold)
