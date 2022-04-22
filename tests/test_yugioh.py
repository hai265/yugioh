# import unittest
#
# from src.card import create_deck_from_csv, create_deck_from_array
# from src.player import Player
# from src.yugioh import Yugioh, to_dict
#
#
# class TestYugiohCreate(unittest.TestCase):
#     def setUp(self):
#         self.yugioh_game = Yugioh()
#         self.preset_deck = create_deck_from_csv("sources/preset1")
#         self.preset_deck_string = []
#         for card in self.preset_deck:
#             self.preset_deck_string.append(card.name)
#
#     def test_create_game_add_two_player_name_to_game_preset_1(self):
#         return_data = self.yugioh_game.create_game(
#             {"player_name": "Yugi", "deck": self.preset_deck_string, "session_id": 1})
#         self.assertTrue(return_data["session_id"] == 1)
#         self.assertTrue(return_data["players"][0]["name"] == "Yugi")
#         true_deck = create_deck_from_array(["Hitotsu-Me Giant", "Dark Magician",
#                                             "Gaia The Fierce Knight", "Mammoth Graveyard",
#                                             "Silver Fang", "Curtain of the Dark One", "Tomozaurus",
#                                             "Feral Imp"])
#         self.assertEqual(return_data["players"][0]["deck"], to_dict(true_deck))
#         return_data = self.yugioh_game.create_game(
#             {"player_name": "Kaiba", "deck": self.preset_deck_string, "session_id": 1})
#         self.assertTrue(return_data["session_id"] == 1)
#         true_deck = create_deck_from_array(["Hitotsu-Me Giant", "Dark Magician",
#                                             "Gaia The Fierce Knight", "Mammoth Graveyard",
#                                             "Silver Fang", "Curtain of the Dark One", "Tomozaurus",
#                                             "Feral Imp"])
#         self.assertEqual(return_data["players"][1]["deck"], to_dict(true_deck))
#         self.assertTrue(return_data["current_player"]["name"] == "Yugi")
#         self.assertTrue(return_data["other_player"]["name"] == "Kaiba")
#
#     def test_create_game_create_two_game_sessions(self):
#         game1 = self.yugioh_game.create_game({"player_name": "Yugi", "deck": self.preset_deck_string, "session_id": 1})
#         game2 = self.yugioh_game.create_game({"player_name": "Yugi", "deck": self.preset_deck_string, "session_id": 2})
#         self.assertNotEqual(game1, game2)
#
#
# class TestYugiohRead(unittest.TestCase):
#     def setUp(self):
#         self.yugioh_game = Yugioh()
#         self.preset_deck = create_deck_from_csv("sources/preset1")
#         self.preset_deck_string = []
#         for card in self.preset_deck:
#             self.preset_deck_string.append(card.name)
#
#     def test_read_game_read_after_create(self):
#         game_status_dict = self.yugioh_game.read_game({"session_id": 1})
#         self.assertTrue(game_status_dict.keys() == self.yugioh_game.game.__dict__.keys())
#         self.assertTrue(["session_id"] != 0)
#
#
# class TestYugiohUpdate(unittest.TestCase):
#     def setUp(self):
#         self.yugioh_game = Yugioh()
#         self.preset_deck = create_deck_from_csv("sources/preset1")
#         self.preset_deck_string = []
#         for card in self.preset_deck:
#             self.preset_deck_string.append(card.name)
#         self.yugioh_game.create_game(
#             {"player_name": "Yugi", "deck": self.preset_deck_string, "session_id": 1})
#         self.yugioh_game.create_game(
#             {"player_name": "Kaiba", "deck": self.preset_deck_string, "session_id": 1})
#
#     def test_update_game_draw_card(self):
#         game_state = self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "draw_card"})
#         self.assertTrue(len(game_state["players"][0]["deck"] == 7))
#         self.assertTrue(len(game_state["players"][0]["hand"]) == 1)
#         game_state = self.yugioh_game.update_game({"session_id": 1, "player": 2, "move": "draw_card"})
#         self.assertTrue(len(game_state["players"][1]["deck"] == 7))
#         self.assertTrue(len(game_state["players"][1]["hand"]) == 1)
#
#     def test_update_game_summon_card_from_hand(self):
#         self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "draw_card", "args": [2]})
#         self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "summon_monster", "args": [0]})
#         game_state = self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "summon_monster", "args": [0]})
#         self.assertTrue(game_state["players"][0]["field"][0]["name"] == "Hitotsu-Me Giant")
#         self.assertTrue(game_state["players"][0]["field"][1]["name"] == "Dark Magician")
#         game_state = self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "draw_card"})
#         self.assertTrue(game_state["players"][1]["field"][0]["name"] == "Hitotsu-Me Giant")
#
#     def test_update_game_attack_monster_on_field(self):
#         # Summon dark magician on player 1's field, hitotsu me giant on player 2, and have dark magician attack giant
#         self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "draw_card", "args": [2]})
#         self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "summon_monster", "args": [1]})
#         self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "draw_card", "args": [1]})
#         self.yugioh_game.update_game({"session_id": 1, "player": 2, "move": "summon_monster", "args": [0]})
#         game_state = self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "attack_monster",
#                                                    "args": [0, 0]})
#         giant = create_deck_from_array(["Hitotsu-Me Giant"])[0]
#         magician = create_deck_from_array(["Dark Magician"])[0]
#         self.assertEqual(game_state["players"][1]["life_points"], Player.default_life_points -
#                          (magician.attack_points + giant.attack_points))
#         self.assertTrue(game_state["players"][1]["field"][0] == "None")
#
#     def test_update_game_attack_player_with_giant(self):
#         # Summon dark magician on player 1's field, hitotsu me giant on player 2, and have dark magician attack giant
#         self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "draw_card", "args": [0]})
#         self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "summon_monster", "args": [0]})
#         game_state = self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "attack_player",
#                                                    "args": [0]})
#         giant = create_deck_from_array(["Hitotsu-Me Giant"])[0]
#         self.assertEqual(game_state["players"][1]["life_points"], Player.default_life_points -
#                          giant.attack_points)
#
#     def test_update_game_change_turn(self):
#         # Summon dark magician on player 1's field, hitotsu me giant on player 2, and have dark magician attack giant
#         game_status = self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "change_turn"})
#         self.assertTrue(game_status["current_player"]["name"] == "Kaiba")
#         self.assertTrue(game_status["current_player"]["name"] == "Yugi")
#         game_status = self.yugioh_game.update_game({"session_id": 1, "player": 1, "move": "change_turn"})
#         self.assertTrue(game_status["current_player"]["name"] == "Yugi")
#         self.assertTrue(game_status["current_player"]["name"] == "Kaiba")
#
#
# class TestYugiohDelete(unittest.TestCase):
#     def setUp(self):
#         self.yugioh_game = Yugioh()
#         self.preset_deck = create_deck_from_csv("sources/preset1")
#         self.preset_deck_string = []
#         for card in self.preset_deck:
#             self.preset_deck_string.append(card.name)
#
#     def test_delete_yugioh_game(self):
#         status = self.yugioh_game.delete_game({"session_id": 1})
#         self.assertTrue("session_id" in status and status["session_id"] != 0)
