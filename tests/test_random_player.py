from itertools import product
from random import shuffle
from scipy.stats import chisquare
import unittest


from game_assets.card import Card
from game_assets.euchre import SUITS, CARD_FACES
from game_assets.players.random_player import RandomPlayer


class TestExchangeWithKitty(unittest.TestCase):
    """
    Unittests for validating the exchange_with_kitty
    method of random player. Due to the relatively
    low complexity of the behavior, we randomly sample
    a large number of draws, and then validate
    that the distribution of returned cards is sufficiently
    uniform.
    """

    def setUp(self):
        """

        """
        self.random_player = RandomPlayer(0)
        self.n_tests = 100000
        self.alpha = 0.05
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
            card_id:0 for card_id in  product(SUITS, CARD_FACES)
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
        self.assertGreater(chisquare(list(returned_cards.values())).pvalue, self.alpha)
