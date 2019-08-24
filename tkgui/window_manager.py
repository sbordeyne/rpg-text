from rpglib.game import Game
from .window import Window
from .title_screen import TitleScreen
from .main_screen import MainScreen
from .io_wrapper import TkIOWrapper
import io
import sys


# sys.stdout = TkIOWrapper


class WindowManager:
    def __init__(self, root):
        self.game = Game()
        self.root = root
        self.window = Window(root, loop=self.loop)
        self.window.pack()

        self.title_screen = TitleScreen(self)
        self.main_screen = MainScreen(self)
        self.title_screen()

    def loop(self, *args, **kwargs):
        if not self.game.command_system.parse(self.main_screen.command):
            print("Invalid Command. Type 'help' for help.")

    def print_asset(self, name='game', position=(0, 0)):
        with io.open(f"assets/screens/{name}", encoding='utf-8') as f:
            for i, line in enumerate(f):
                x = position[0]
                y = position[1] + i
                self.window.print(line, (x, y))
