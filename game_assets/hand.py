from typing import Union

class Hand:

    def __init__(self, trump: Union[int,str]) -> None:
        """
        Hand constructor (encapsulating 5 tricks). Requires specification of
        the trump suit

        Parameters
        ----------
            trump : int or str
                One of the suits in euchre.SUITS

        Returns
        -------
            None
        """
        self.tricks = []
        self.trump = trump
