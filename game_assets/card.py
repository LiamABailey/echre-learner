from dataclasses import dataclass
from typing import Union

from euchre import SUIT_DESCRIPTOR, FACE_DESCRIPTOR

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
