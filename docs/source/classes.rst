Code Behind Yu-Gi-Oh!
==================================

Let's explore the classes, methods, and functions that are responsible for Yu-Gi-Oh!'s functionality.

The Player Class
---------------------------------
This class handles all activity relating to the player. This includes drawing cards, summoning monsters, \
sending monsters to the graveyard, and other various getters/setters.

    .. autoclass:: src.player.Player
        :members:

The Card Class
---------------------------------
There are two types of card classes related to this version of Yu-Gi-Oh!. The first class is a parent class for a \
generic card. The second of the two is a more specific Monster Card.

The Generic Card Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: src.card.Card
        :members:

The Monster Card Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: src.card.Monster
        :members:

The Game Controller Class
---------------------------------
This class deals with controlling the actual functionality of the Yu-Gi-Oh! game. This controller is involved with \
determining the first player, changing turns, having monsters attack, determining a winner, etc.

    .. autoclass:: src.game.GameController
        :members:

The Yu-Gi-Oh! Session Class
---------------------------------
This class is in charge of creating, storing, presenting, and updating a Yu-Gi-Oh! game session.

    .. autoclass:: src.yugioh.Yugioh
        :members:
