from .utils import sanitized_input
from .command_system import CommandSystem
from .character_system import CharacterSystem
from .player import Player
from.map import Map


class Game:
    def __init__(self, p_name, p_job):
        self.map = Map(self)
        self.player = Player(self, p_name, p_job)
        self.n_turns = 0
        self.screen_width = 80
        self.character_system = CharacterSystem(self)
        self.command_system = CommandSystem(self)

    def next_turn(self):
        self.n_turns += 1
        command = sanitized_input("> ", error_msg="Invalid Command!")
        while not self.command_system.parse(command):
            print("Invalid command. Type 'help' for help.")
            command = sanitized_input("> ", error_msg="Invalid Command!")
