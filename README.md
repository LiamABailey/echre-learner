# euchre-learner
RL for (Most of) Euchre

## RL Agent/Learner for Euchre, with the following simplifications:
- Does not perform trump suit selection (handled w/ a heuristic)
- "Going alone" is not implemented
- Trump selection after passing on the revealed kitty card is "Stick the Dealer".
- Reneging is not part of the game - agents will avoid regeging. When cards are
selected for play *randomly* (e.g. for the random-action agent or during RL
exploration), only legal cards will be drawn from.

## Project layout:
- __Game Assets__
  - `card.py`: Defines 'cards', with support for comparison operations.
  - `euchre.py`: Defines game constants
  - `hand.py`: Defines a single round of play
  - `player\splayer.py`: The abstract definition of 'player' agents. This mostly serves to define an interface, but some standard methods are defined
    - `random_player.py`: Defines an agent that makes decisions randomly, based on the available *legal* choices
    - `heuristic_player.py`: Specifies agents that make decisions based on pre-defined heuristics
    - a variety of __RL-Based Players__ are undergoing planning & research.
  - `table.py`: Defines the `Table`, which manages game state & play.
  - `trick.py`: The 'sub-round' of play

Generally, a `Table` is set up with four `Player`s. Each plays through the `Hand`s of
five `Trick`s, with each trick consisting of four `Card`s.

## Additional Resources
- __analyses__
  - A series of jupyter notebooks dedicated to research topics of interest

## TODOS:
  - Review of Random Agent Performance
  - Verbosity flag to support insights into app behavior
  - Implementation of heuristic-based player
  - Implementation of RL-based player(s)

### A Note on Testing
Unit tests are written for various parts of the package as a way to validate behavior. Although some of the tests were valuable to affirm proper behavior (such as for `lt_card`), many of these methods served as learning exercises (getting comfortable with `SubTest` and researching testing under stochastic behavior) or simply practice. Although these test will be useful (to some degree) if I decide to re-work the internal game mechanisms, I make the following notes:
  a. I am unlikely to do this in the first place. As long as the implementation is not reasonably inefficient, and is accurate/correct, I will likely not perform a major overhaul.
  b. A meaningful amount of the tests are bound (to some degree or another) to implementation particulars, meaning that they would have to be rewritten along with the relevant code.
