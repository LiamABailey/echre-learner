# note - integer comparisons were about 10% faster on my device
CLUB = 0
DIAMOND = 1
HEART = 2
SPADE = 3
SUITS = [CLUB, DIAMOND, HEART, SPADE]
SUIT_DESCRIPTOR = {
    CLUB : "club",
    DIAMOND : "diamond",
    HEART : "heart",
    SPADE : "spade"
}
# The mapping of trump suit (K) to the suit of the left bar (V)
LEFT_SUIT = {
    CLUB : SPADE,
    DIAMOND : HEART,
    HEART : DIAMOND,
    SPADE : CLUB
}
NINE = 0
TEN = 1
JACK = 2
QUEEN = 3
KING = 4
ACE = 5
CARD_FACES = [NINE, TEN, JACK, KING, QUEEN, ACE]
FACE_DESCRIPTOR = {
    NINE : "nine",
    TEN : "ten",
    JACK : "jack",
    QUEEN : "queen",
    KING : "king",
    ACE : "ace"
}
NUM_PLAYERS = 4
NUM_TRICKS = 5
