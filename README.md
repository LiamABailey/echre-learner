# euchre-learner
RL for (Most of) Euchre

####RL Agent/Learner for Euchre, with the following simplifications:
- Does not perform trump suit selection (handled w/ a heuristic)
- "Going alone" is not implemented
- Trump selection after passing on the revealed kitty card is "Stick the Dealer".
- Reneging is not part of the game - agents will avoid regeging. When cards are
selected for play *randomly* (e.g. for the random-action agent or during RL
exploration), only legal cards will be drawn from.



####Code layout:
  4 *players* (which perform decision-making randomly, by heuristic, or
    by learned policy) are seated at a *table*, which manages the initial
    dealing of cards, and scoring (via the creation and management of
    *trick*s and *hand*s)
