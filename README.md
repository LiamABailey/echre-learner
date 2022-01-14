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
- `card.py`: Defines 'cards', with support for comparison operations.
- `euchre.py`: Defines game constants
- `hand.py`: Defines a single round of play
- `player.py`: The abstract definition of 'player' agents. This mostly serves to define an interface, but some standard methods are defined
  - `random_player.py`: Defines an agent that makes decisions randomly, based on the available *legal* choices
  - `heuristic_player.py`: Specifies agents that make decisions based on pre-defined heuristics
  - a variety of __RL-Based Players__ are undergoing planning & research.
- `table.py`: Defines the `Table`, which manages game state & play.
- `trick.py`: The 'sub-round' of play

Generally, a `Table` is set up with four `Player`s. Each plays through the `Hand`s of
five `Trick`s, with each trick consisting of four `Card`s. 
