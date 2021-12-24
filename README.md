# euchre-learner
RL for (Most of) Euchre

RL Agent/Learner for Euchre, with the following simplifications:
- Does not perform trump suit selection (handled w/ a heuristic)
- "Going alone" is not implemented



Code layout:
  4 *players* (which perform decision-making randomly, by heuristic, or
    by learned policy) are seated at a *table*, which manages the initial
    dealing of cards, and scoring (both of tricks and hands)
