import unittest
from src.CLIInterface import create_card
from src.CLIInterface import create_deck_from_preset
from src.player import Player


class TestPlayer(unittest.TestCase):

    def test_draw_card(self):
        # Create a player
        player = Player(5000, "Yugi")

        # Create a deck for the player
        deck = create_deck_from_preset("sources/preset1")
        player.deck = deck

        # Hand should be empty
        self.assertTrue(len(player.hand) == 0)

        # Draw card and make sure it was added to hand
        card = deck[0]
        player.draw_card()
        self.assertTrue(len(player.hand) == 1)
        self.assertTrue(player.hand[0].name == card.name)
        self.assertTrue(player.hand[0].description == card.description)
        self.assertTrue(player.hand[0].card_type == card.card_type)

        # Draw another card and make sure it was added to hand
        card = deck[0]
        player.draw_card()
        self.assertTrue(len(player.hand) == 2)
        self.assertTrue(player.hand[1].name == card.name)
        self.assertTrue(player.hand[1].description == card.description)
        self.assertTrue(player.hand[1].card_type == card.card_type)

        # Draw a third card and make sure it was added to hand
        card = deck[0]
        player.draw_card()
        self.assertTrue(len(player.hand) == 3)
        self.assertTrue(player.hand[2].name == card.name)
        self.assertTrue(player.hand[2].description == card.description)
        self.assertTrue(player.hand[2].card_type == card.card_type)

    def test_get_hand_size(self):
        # Create a player
        player = Player(5000, "Yugi")

        # Create a reusable card
        card = create_card("Tomozaurus")

        # Hand should be empty
        self.assertTrue(player.get_hand_size() == 0)

        # Draw cards and make sure it was added to hand
        player.hand.append(card)
        self.assertTrue(player.get_hand_size() == 1)

        player.hand.append(card)
        self.assertTrue(player.get_hand_size() == 2)

        player.hand.append(card)
        self.assertTrue(player.get_hand_size() == 3)

    def test_get_deck_size(self):
        # Create a player
        player = Player(5000, "Yugi")

        # Create a deck for the player
        deck = create_deck_from_preset("sources/preset1")
        player.deck = deck

        # Deck should have 8
        self.assertTrue(player.get_deck_size() == 8)

        # Draw a cards and make sure deck is updated
        player.deck.pop(0)
        self.assertTrue(player.get_deck_size() == 7)

        player.deck.pop(0)
        self.assertTrue(player.get_deck_size() == 6)

        player.deck.pop(0)
        self.assertTrue(player.get_deck_size() == 5)

    def test_send_card_to_graveyard(self):
        # Create a player
        player = Player(5000, "Yugi")

        # Create a reusable card
        card = create_card("Tomozaurus")

        # Graveyard should be empty
        self.assertTrue(player.get_graveyard_size() == 0)

        # Place cards in graveyard
        player.graveyard.append(card)
        self.assertTrue(player.get_graveyard_size() == 1)

        player.graveyard.append(card)
        self.assertTrue(player.get_graveyard_size() == 2)

    def test_summon_monster(self):
        # Create a player
        player = Player(5000, "Yugi")

        # Create a deck for the player
        deck = create_deck_from_preset("sources/preset1")
        player.deck = deck

        # Draw three cards for the player
        player.draw_card()
        player.draw_card()
        player.draw_card()

        # Summon all three monsters to board
        card = player.hand[0]
        player.summon_monster(0, 0)
        self.assertTrue(len(player.hand) == 2)
        self.assertTrue(player.field[0].name == card.name)
        self.assertTrue(player.field[0].description == card.description)
        self.assertTrue(player.field[0].card_type == card.card_type)

        # Summon all three monsters to board
        card = player.hand[1]
        player.summon_monster(1, 1)
        self.assertTrue(len(player.hand) == 1)
        self.assertTrue(player.field[1].name == card.name)
        self.assertTrue(player.field[1].description == card.description)
        self.assertTrue(player.field[1].card_type == card.card_type)

        # Summon all three monsters to board
        card = player.hand[0]
        player.summon_monster(0, 2)
        self.assertTrue(len(player.hand) == 0)
        self.assertTrue(player.field[2].name == card.name)
        self.assertTrue(player.field[2].description == card.description)
        self.assertTrue(player.field[2].card_type == card.card_type)

    def test_tribute_summon(self):
        # This will be implemented later
        pass

    def send_card_to_graveyard(self):
        # Create a player
        player = Player(5000, "Yugi")

        # Create a deck for the player
        deck = create_deck_from_preset("sources/preset1")
        player.deck = deck

        # Draw five cards for the player
        player.draw_card()
        player.draw_card()
        player.draw_card()
        player.draw_card()
        player.draw_card()

        # Summon three monsters to board
        player.summon_monster(0, 0)
        player.summon_monster(0, 1)
        player.summon_monster(0, 2)

        # Send monster from only field to graveyard
        card = player.field[0]
        player.send_card_to_graveyard(0, -1)
        self.assertTrue(len(player.graveyard) == 1)
        self.assertTrue(player.graveyard[0].name == card.name)
        self.assertTrue(player.graveyard[0].description == card.description)
        self.assertTrue(player.graveyard[0].card_type == card.card_type)
        self.assertTrue(len(player.hand) == 2)
        self.asserTrue(player.field[0] is None)

        # Send monster from only hand to graveyard
        card = player.hand[0]
        player.send_card_to_graveyard(-1, 0)
        self.assertTrue(len(player.graveyard) == 2)
        self.assertTrue(player.graveyard[1].name == card.name)
        self.assertTrue(player.graveyard[1].description == card.description)
        self.assertTrue(player.graveyard[1].card_type == card.card_type)
        self.assertTrue(len(player.hand) == 1)

        # Send monster from both hand and graveyard
        card1 = player.hand[0]
        card2 = player.field[1]
        player.send_card_to_graveyard(1, 0)
        self.assertTrue(len(player.graveyard) == 4)
        self.assertTrue(player.graveyard[2].name == card1.name)
        self.assertTrue(player.graveyard[2].description == card1.description)
        self.assertTrue(player.graveyard[2].card_type == card1.card_type)
        self.assertTrue(player.graveyard[3].name == card2.name)
        self.assertTrue(player.graveyard[3].description == card2.description)
        self.assertTrue(player.graveyard[3].card_type == card2.card_type)
        self.assertTrue(len(player.hand) == 0)

    def test_decrease_life_points(self):
        # Create a player
        player = Player(5000, "Yugi")

        self.assertTrue(player.lifePoints == 5000)
        player.decrease_life_points(1000)
        self.assertTrue(player.lifePoints == 4000)

