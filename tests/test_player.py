import unittest
from src.card import create_card, create_deck_from_preset
from src.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        # Create a self.player
        self.player = Player(5000, "Yugi")
        # Create a deck for the self.player
        self.deck = create_deck_from_preset("sources/preset1")
        self.player.deck = self.deck

    def test_draw_card(self):
        # Hand should be empty
        self.assertTrue(len(self.player.hand) == 0)

        # Draw card and make sure it was added to hand
        card = self.deck[0]
        self.player.draw_card(1)
        self.assertTrue(len(self.player.hand) == 1)
        self.assertEqual(card, self.player.hand[0])

        # Draw another card and make sure it was added to hand
        card = self.deck[0]
        self.player.draw_card(1)
        self.assertTrue(len(self.player.hand) == 2)
        self.assertEqual(card, self.player.hand[1])

        # Draw a third card and make sure it was added to hand
        card = self.deck[0]
        self.player.draw_card(1)
        self.assertTrue(len(self.player.hand) == 3)
        self.assertEqual(card, self.player.hand[2])

    def test_get_hand_size(self):
        # Create a self.player
        self.player = Player(5000, "Yugi")

        # Create a reusable card
        card = create_card("Tomozaurus")

        # Hand should be empty
        self.assertTrue(self.player.get_hand_size() == 0)

        # Draw cards and make sure it was added to hand
        self.player.hand.append(card)
        self.assertTrue(self.player.get_hand_size() == 1)

        self.player.hand.append(card)
        self.assertTrue(self.player.get_hand_size() == 2)

        self.player.hand.append(card)
        self.assertTrue(self.player.get_hand_size() == 3)

    def test_get_deck_size(self):
        # Deck should have 8
        self.assertTrue(self.player.get_deck_size() == 8)

        # Draw a cards and make sure deck is updated
        self.player.deck.pop(0)
        self.assertTrue(self.player.get_deck_size() == 7)

        self.player.deck.pop(0)
        self.assertTrue(self.player.get_deck_size() == 6)

        self.player.deck.pop(0)
        self.assertTrue(self.player.get_deck_size() == 5)

    def test_send_card_to_graveyard(self):
        # Create a self.player
        self.player = Player(5000, "Yugi")

        # Create a reusable card
        card = create_card("Tomozaurus")

        # Graveyard should be empty
        self.assertTrue(self.player.get_graveyard_size() == 0)

        # Place cards in graveyard
        self.player.graveyard.append(card)
        self.assertTrue(self.player.get_graveyard_size() == 1)

        self.player.graveyard.append(card)
        self.assertTrue(self.player.get_graveyard_size() == 2)

    def test_summon_monster(self):
        # Draw three cards for the player
        self.player.draw_card(3)

        # Summon all three monsters to board
        card = self.player.hand[0]
        self.player.normal_summon(0, 0, 'atk')
        self.assertTrue(len(self.player.hand) == 2)
        self.assertEqual(card, self.player.monster_field[0])

        # Summon all three monsters to board
        card = self.player.hand[0]
        self.player.normal_summon(0, 1, 'atk')
        self.assertTrue(len(self.player.hand) == 1)
        self.assertEqual(card, self.player.monster_field[1])

        # Summon all three monsters to board
        card = self.player.hand[0]
        self.player.normal_summon(0, 2, 'atk')
        self.assertTrue(len(self.player.hand) == 0)
        self.assertEqual(card, self.player.monster_field[2])

    def test_successful_level7_tribute_summon(self):
        # create copies of monsters involved in the summoning process
        tribute1 = create_card("Hitotsu-Me Giant")
        tribute2 = create_card("Mammoth Graveyard")
        dark_magician = create_card("Dark Magician")

        self.player.hand = [tribute1, tribute2, dark_magician]

        # summon two level 4 or lower monsters
        self.player.normal_summon(0, 0, 'atk')
        self.player.normal_summon(0, 1, 'atk')

        # try to summon one level 7 or higher monster by tributing the two monsters that were just summoned
        self.player.tribute_summon(0, 0, 1, 'atk')

        # check monster field
        expected_monster_field = [dark_magician, None, None, None, None]
        self.assertEqual(expected_monster_field, self.player.monster_field)

        # check graveyard
        expected_graveyard = [tribute1, tribute2]
        self.assertEqual(expected_graveyard, self.player.graveyard)

        # check hand
        self.assertEqual([], self.player.hand)

    def test_failed_level7_tribute_summon(self):
        # create copies of monsters involved in the summoning process
        tribute1 = create_card("Hitotsu-Me Giant")
        dark_magician = create_card("Dark Magician")

        self.player.hand = [tribute1, dark_magician]

        # summon one level 4 lower monster
        self.player.normal_summon(0, 0, 'atk')
        # try to summon one level 7 or higher monster by tributing the monster that were just summoned
        self.player.tribute_summon(0, 0, -1, 'atk')

        # check monster field
        expected_monster_field = [tribute1, None, None, None, None]
        self.assertEqual(expected_monster_field, self.player.monster_field)

        # check graveyard
        self.assertEqual([], self.player.graveyard)
        # check hand
        self.assertEqual([dark_magician], self.player.hand)

    def test_failed_level7_tribute_summon_using_same_tribute(self):
        # create copies of monsters involved in the summoning process
        tribute1 = create_card("Hitotsu-Me Giant")
        dark_magician = create_card("Dark Magician")

        self.player.hand = [tribute1, dark_magician]

        # summon one level 4 lower monster
        self.player.normal_summon(0, 0, 'atk')
        # try to summon one level 7 or higher monster by tributing the summoned monster twice
        self.player.tribute_summon(0, 0, 0, 'atk')

        # check monster field
        expected_monster_field = [tribute1, None, None, None, None]
        self.assertEqual(expected_monster_field, self.player.monster_field)

        # check graveyard
        self.assertEqual([], self.player.graveyard)
        # check hand
        self.assertEqual([dark_magician], self.player.hand)

    def test_summon_monsters_defense_position(self):
        card1 = create_card("Hitotsu-Me Giant")
        card2 = create_card("Tomozaurus")
        dark_magician = create_card("Dark Magician")

        self.player.hand = [card1, card2, dark_magician]
        # summon level 4 or lower monsters
        self.player.normal_summon(0, 0, 'def')
        self.player.normal_summon(0, 1, 'def')
        # try to summon one level 7 or higher monster by tributing the summoned monster twice
        self.player.tribute_summon(0, 0, 1, 'def')

        self.assertEqual('def', self.player.monster_field[0].position)

    def test_change_monsters_positions(self):
        card1 = create_card("Hitotsu-Me Giant")
        card2 = create_card("Tomozaurus")

        self.player.hand = [card1, card2]

        # summon level 4 or lower monsters
        self.player.normal_summon(0, 0, 'atk')
        self.player.normal_summon(0, 1, 'def')

        # change monster positions
        self.player.change_monster_position(0)
        self.player.change_monster_position(1)

        self.assertEqual('def', self.player.monster_field[0].position)
        self.assertEqual('atk', self.player.monster_field[1].position)

    def test_send_card_to_graveyard_from_field_and_hand(self):
        # Draw five cards for the player
        self.player.draw_card(5)

        # Summon three monsters to board
        for i in range(3):
            self.player.normal_summon(0, i, 'atk')

        # Send monster from only field to graveyard
        card = self.player.monster_field[0]
        self.player.send_card_to_graveyard(0, -1)

        self.assertTrue(len(self.player.graveyard) == 1)
        self.assertEqual(card, self.player.graveyard[0])
        self.assertTrue(len(self.player.hand) == 2)
        self.assertTrue(self.player.monster_field[0] is None)

        # Send monster from only hand to graveyard
        card = self.player.hand[0]
        self.player.send_card_to_graveyard(-1, 0)
        self.assertTrue(len(self.player.graveyard) == 2)

        self.assertEqual(card, self.player.graveyard[1])
        self.assertTrue(len(self.player.hand) == 1)

        # Send monster from both hand and graveyard
        field_card = self.player.monster_field[1]
        hand_card = self.player.hand[0]
        self.player.send_card_to_graveyard(1, 0)
        self.assertTrue(len(self.player.graveyard) == 4)
        self.assertEqual(field_card, self.player.graveyard[2])
        self.assertEqual(hand_card, self.player.graveyard[3])
        self.assertTrue(len(self.player.hand) == 0)

    def test_decrease_life_points(self):
        self.assertTrue(self.player.life_points == 5000)
        self.player.decrease_life_points(1000)
        self.assertTrue(self.player.life_points == 4000)
