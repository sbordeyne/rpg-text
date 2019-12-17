import sys
from copy import copy

from .utils import sanitized_input, clear_screen
from .command_system import CommandSystem
from .character_system import CharacterSystem
from .treasure_system import TreasureSystem
from .combat_system import CombatSystem
from .game_timer import GameTimer
from .player import Player
from .map import Map
from .saveload import SaveSystem
from .utils import parse_dice_format
from .stats import Stats
from .shop_system import ShopSystem


class Game:
    def __init__(self):
        self.screen_width = 80
        self.map = Map(self)
        self.player = Player(self)
        self.timer = GameTimer(self)
        self.character_system = CharacterSystem(self)
        self.treasure_system = TreasureSystem(self)
        self.save_system = SaveSystem(self)
        self.combat_system = CombatSystem(self)
        self.shop_system = ShopSystem(self)
        self.command_system = CommandSystem(self)

    def next_turn(self):
        self.timer.tick()
        command = sanitized_input("> ", error_msg="Invalid Command!")
        while not self.command_system.parse(command):
            print("Invalid command. Type 'help' for help.")
            command = sanitized_input("> ", error_msg="Invalid Command!")

    def main_menu(self):
        print("Welcome to rpg-text!")
        print("> New Game")
        print("> Quick Start")
        print("> Load Game")
        print("> Quit")
        choice = sanitized_input("> ", error_msg="Invalid choice.").lower()
        if choice.startswith("n"):
            self.new_game()
        elif choice.startswith("q"):
            self.quick_start()
        elif choice.startswith("l"):
            self.load_game()
        elif choice.startswith("q"):
            self.quit()

    def new_game(self):
        clear_screen()
        print("Please enter your character's name.")
        p_name = sanitized_input("> ", error_msg="")
        print("Please enter your desired job (thief, wizard, fighter, cleric).")
        p_job = sanitized_input("> ", error_msg="Invalid job.", valid_input=("thief", "wizard", "fighter", "cleric"))
        self.player.name = p_name
        self.player.job = p_job
        satisfied_rolls = False
        saved_health = [2]
        saved_mana = [2]
        saved_stats = {k: 9 for k in Stats.stat_names}
        self.player.health_rolls.append(parse_dice_format(self.player.job.hp_die))
        self.player.mana_rolls.append(parse_dice_format(self.player.job.mp_die))
        self.player.stats.randomize()
        while not satisfied_rolls:
            print(f"HP : {self.player.health_rolls[0]} ; MP : {self.player.mana_rolls[0]} ; {str(self.player.stats)}")
            print(f"Sum : {sum(self.player.stats.as_dict.values())}")
            print("Are you satisfied with these stats?")
            print("Please enter 'yes', 'no', 'reroll', 'save', 'recall' or 'info'")
            p_cmd = sanitized_input('> ', error_msg="Invalid command.",
                                    valid_input=('yes', 'no', 'reroll', 'recall', 'save', 'info'))
            if p_cmd == 'yes':
                satisfied_rolls = True
            elif p_cmd in ('no', 'reroll'):
                self.player.health_rolls.append(parse_dice_format(self.player.job.hp_die))
                self.player.mana_rolls.append(parse_dice_format(self.player.job.mp_die))
                self.player.stats.randomize()
            elif p_cmd == 'save':
                saved_health = copy(self.player.health_rolls)
                saved_mana = copy(self.player.mana_rolls)
                saved_stats = self.player.stats.as_dict
                self.player.health_rolls.append(parse_dice_format(self.player.job.hp_die))
                self.player.mana_rolls.append(parse_dice_format(self.player.job.mp_die))
                self.player.stats.randomize()
            elif p_cmd == 'recall':
                self.player.health_rolls = copy(saved_health)
                self.player.mana_rolls = copy(saved_mana)
                self.player.stats.recall_stats(saved_stats)
            elif p_cmd == 'info':
                self.player.stats.info()
        self.player.health = self.player.max_health
        self.player.inventory.money.get_random_starting_money()

        # Clear the screen and start the game
        clear_screen()

    def quick_start(self):
        clear_screen()
        self.player.name = "Milton"
        self.player.job = "fighter"
        saved_health = [8]
        saved_mana = [1]
        saved_stats = {k: stat for k, stat in zip(Stats.stat_names, [16, 13, 13, 16, 13, 16])}
        self.player.inventory.money.get_random_starting_money()
        self.player.health_rolls = copy(saved_health)
        self.player.mana_rolls = copy(saved_mana)
        self.player.stats.recall_stats(saved_stats)
        self.player.health = self.player.max_health
        self.player.inventory.get_item("sword")
        self.player.inventory.equip_item("sword")
        self.player.experience = 8000
        self.player.try_level_up()
        self.player.try_level_up()
        clear_screen()

    def load_game(self):
        clear_screen()
        print("Enter a save name to load.")
        found_saves = SaveSystem.get_save_names()
        valid_inputs = copy(found_saves)
        valid_inputs.append("list")
        save_name = sanitized_input("> ", valid_input=valid_inputs, error_msg="Save file not found. Please try again.")
        if save_name.lower() == "list":
            print("Saves : " + ", ".join(found_saves))
        else:
            self.save_system.load(save_name)

    def enter(self, location):
        """Enter a location, or a shop. Specify the location to enter (shop, submap)"""
        if location == "shop":
            self.shop_system.enter()
        elif location in self.map.get_submaps():
            self.map = Map(self, location)
        else:
            self.command_system.help('enter')

    def exit(self):
        """Exits to the world map."""
        self.map = Map(self)

    def game_over(self):
        print("GAME OVER")  # TODO: Add option to load a saved game or exit.
        sys.exit(1)

    def quit(self):
        """Saves and quits the game. Save is named 'autosave'"""
        self.save_system.save("autosave")
        clear_screen()
        sys.exit(1)
