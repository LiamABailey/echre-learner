from dataclasses import dataclass
from typing import Union

from euchre import CARD_FACES, SUIT_DESCRIPTOR, FACE_DESCRIPTOR, JACK

@dataclass
class Card:
    """
    Class for storing card information
    """
    suit: Union[str, int]
    face: Union[str, int]


    def __str__(self):
        return (f"{FACE_DESCRIPTOR[self.face].capitalize()} of "
                f"{SUIT_DESCRIPTOR[self.suit].capitalize()}s")


    def _is_left_bar(self, trump: Union[str, int]) -> bool:
        """
        Evaluate if the card is specifically the left bar of a given
        trump suit

        Parameters
        ----------
            trump : Union[str, int]
                The trump suit, from euchre.SUITS

        Returns
        -------
            bool : True if is left bar, false otherwise
        """
        if self.face == euchre.JACK and self.suit == LEFT_SUIT[trump]:
            return True

    def is_trump(self, trump: Union[str, int]) -> bool:
        """
        Evaluate if the card is in the trump suit

        Parameters
        ----------
            trump : Union[str, int]
                The trump suit, from euchre.SUITS

        Returns
        -------
            bool : True if member, false otherwise
        """
        if self.suit == trump or self._is_left_bar(trump):
            return True
        return False


    def lt_card(self, other: Card, trump: Union[str, int], lead: Union[str, int]) -> bool:
        """
        Check if this card is of lower value than another card, given
        the trump suit and leading suit

        Parameters
        ----------
            other : Card
                The card compared

            trump : Union[str, int]
                The trump suit, from euchre.SUITS

            trump : Union[str, int]
                The  suit that started the trick, from euchre.SUITS

        Returns
        -------
            bool : True if self < other, False otherwise
        """
        lt = True
        # this card is trump, other isn't
        if self.is_trump(trump) and not other.is_trump(trump):
            return False
        # this card isn't trump, other is
        elif not self.is_trump(trump) and other.is_trump(trump):
            return True
        #either both aren't, or are trump
        else:
            if self.is_trump(trump):
                # if either is a jack, special befahvoir
                if self.face == JACK and other.face != JACK:
                    return False
                elif self.face != JACK and other.face == JACK:
                    return True
                elif self.face == JACK and other.face == JACK:
                    if self._is_left_bar(trump):
                        return True
                    return False
                else:
                    CARD_FACES.index(self.face) < CARD_FACES.index(other.face)
            else:
                if self.is_trump(lead) and not other.is_trump(lead):
                    return False
                # this card isn't lead, other is
                elif not self.is_trump(lead) and other.is_trump(lead):
                    return True
                else:
                    # this is the rare case where neither card lead, or is
                    # in the trump suit. Neither of these cards can wind the
                    # trick, so we don't care about the evaluation.
                    CARD_FACES.index(self.face) < CARD_FACES.index(other.face)
