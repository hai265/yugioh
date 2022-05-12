[![coverage report](https://cmsc435.garrettvanhoy.com/hai265/yugioh/badges/master/coverage.svg)](https://cmsc435.garrettvanhoy.com/hai265/yugioh/commits/gitlab_badge)
# Yu-Gi-Oh!

## Overview
This team project is for CMSC435: Software Development at the University of Maryland. This project strives to recreate the popular Yu-Gi-Oh! card game, derived from the highly popular Japanese animated series Yu-Gi-Oh!. The Yu-Gi-Oh! card game has evolved significantly since the release of the TV's shows various spin offs. For the sake of this project, we will be creating a simplified version of the original Yu-Gi-Oh! card game. For more information on this project, please visit the following link for documentation:

[Yu-Gi-Oh! Documentation](https://devakmurali.github.io/yugiohwebsite/index.html)

## How To Run the Software

This scrum focused on implementing the individual components of the Yu-Gi-Oh! card game. As it stands right now, there is no method (terminal/UI) to allow the user to send inputs into the game. These components are planned to be implemented in later sprints. For now, the individual components have been developed, along with unit testing to test the functionality of each.

To run the server , run `docker build --tag yugioh-server -f Dockerfile.server .`, and then after building the image, run 
`docker run -p 5555:5555 -it yugioh-server`  
To run the client , run `docker build --tag yugioh-client -f Dockerfile.client .`, and then after building the image, run 
`docker run -it yugioh-client`  
To run the tests, run:  
`
pip install virtualenv`  
`virtualenv venv`  
`source venv/bin/activate`  
`pip install pytest-cov`  
`pytest --cov=src tests/`

## Sprint 04/03 - 04/10

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

## Sprint 04/10 - 04/24

**Hai Nguyen**| Effort - 100%

<ins>Work completed</ins>
- Wrote `client.py` and `server.py` 
- Wrote tests for CRUD version of yugioh

**Devak Murali**| Effort - 100%

<ins>Work completed</ins>
- Created documentation for game using Sphinx in PyCharm and pushed to directory
- Hosted HTML documentation on GitHub pages
- Began initial development for UI using Flask


**Pratulya Santharam**| Effort - 100%

<ins>Work completed</ins>
- Created database tables for users and cards
- Implemented functions for user registration/login
- Implemented function for reading cards in `cards.csv` into the database
- Wrote tests for above functions on nominal inputs

**Aravind Ganeshan**| Effort - 100%

<ins>Work completed</ins>
- Refactored game logic components.
- Implemented tribute summoning functionality.
- Implemented monster position switching and direct attacking.
- Created test suites for the above components.
- Contributed to development of Yugioh interface.

**Mo Goldberger**| Effort - 0%

## Sprint 3
**Hai Nguyen**| Effort - 100%

<ins>Work completed</ins>
- Rewrote server using websockets
- Used inquirer to get user input during a game
- Built a command line interface to support the various yugioh actions
- Built a logger to log game actions
- Built a game menu so users can access the various parts of the program


**Pratulya Santharam**| Effort - 100%

<ins>Work completed</ins>
- Fixed login/registration prompt, included whitelist
- Reworked database tables to include user decks and spell cards
- Created AWS RDS instance 
- Updated win/loss functionality to change user's stats
- Added funcitonality for exporting decks
- Added more database functions for reading cards, saving decks, and reading saved decks
- Wrote tests for above functions

**Devak Murali**| Effort - 100%

<ins>Work completed</ins>
- Attempted to create a UI to host the CLI, but was unable to integrate with docker and websockets. 
- Also tried to create a UI for starting menu, but ran into the same problems as above
- Created additional preset decks and added more cards to the available cards for the game
- Created and tested a deck building interface that can be called from the game_menu CLI
- Updated Sphinx documentation to include how to run the sofwtware and included all the new classes and methods written for the game.
- Did some bug fixes and added additional functions to card.py

