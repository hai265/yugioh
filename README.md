# Yu-Gi-Oh!

## Overview
This team project looks to implement a simplified version of the Yu-Gi-Oh! card game. The following are the rules of our simplified version of Yu-Gi-Oh!

Rules:
- Players play against each other with a deck of Monster Cards
- Players start the game with a set number of cards in their hand
- At the beginning of their turn, players can draw a card from the top of their deck
- Players can place monster cards in attack position or defense position
- At the end of their turn, players can choose to attack other players monsters

    <ins>When attacking:</ins>
    - Only monsters in the attack position can attack
    - When attacking an opponent's monster that is also in attack position, the weaker monster gets sent to the graveyard and the difference in attack strength is subtracted from the life points of the owner of the weaker monster
    - When attacking an opponent's monster that is in defense position, the defensive monster is destroyed *only* if the attacking monster has more attack points than the defending monster's defense points
    - If attacking a defensive monster with defense points greater than the attacking monster's attack points, the owner of the attacking monster loses life points equivalent to the difference in attack and defense points.

- After this, the player ends their turn and allows other players to go
- The game ends when one player's life points reaches zero or the player runs out of cards in their deck

## How To Run the Software

This scrum focused on implementing the individual components of the Yu-Gi-Oh! card game. As it stands right now, there is no method (terminal/UI) to allow the user to send inputs into the game. These components are planned to be implemented in later sprints. For now, the individual components have been developed, along with unit testing to test the functionality of each.

### `card.py`

This class defined the structure and initialization of Yu-Gi-Oh! cards. It also allow has functions to allow the user to display the information of the card. The unit testing for this is located in `test_card.py`.

### `player.py`

This class handles all activity relating to the player. This includes drawing cards, summoning monsters, sending monsters to the graveyard, and other various getters/setters. The unit testing for this is located in `test_player.py`.

### `game.py`
This class deals with controlling the actual functionality of the Yu-Gi-Oh! game. This controller is involved with determining the first player, changing turns, having monsters attack, determining a winner, etc. The testing for this class is in `test_game_controller.py`.

### `CLIInterface.py`

This file contains quite a few classes. The first of these classes is a class that aids in the creation of cards. This file also contains a class to create an entire deck made from a preset file.

Finally, this file contains an interface for displaying the current player's hand, setting the current player, and starting a game. This function allows the player to interact with the terminal to play the game. As it stands right now however, this interface is not complete as displaying player hands and setting current players is planned to be implemented in the future scrums.

The testing for this file is located in `test_cli.py`.


## Scrum 04/03 - 04/10

**Hai Nguyen**| Effort - 100%

<ins>Work completed</ins>
- Begun inital user stories and issues for Jeff, Tim, and Sarah
- Implemented `CLIInterface.py` and `test_cli.py`
- Managed merge requests and merge conflits on GitHub

**Pratulya Santharam**| Effort - 100%

<ins>Work completed</ins>
- Completed user stories and issues for Jeff
- Implemented `cards.py` and `test_card.py`

**Devak Murali**| Effort - 100%

<ins>Work completed</ins>
- Completed user stories and issues for Tim
- Implemented `player.py` and `test_player.py`
- Completed README.md documentation for current sprint

**Aravind Ganesan**| Effort - 100%

<ins>Work completed</ins>
- Completed user stories and issues for Sarah
- Implemented `game.py` and `test_game_controller.py`

**Mo Goldberger**| Effort - 0%
