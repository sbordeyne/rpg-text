from rpglib.game import Game
from .window import Window
from .title_screen import TitleScreen
import tkinter as tk
import io


class WindowManager:
    def __init__(self, root):
        self.game = Game()
        self.root = root
        self.window = Window(root, loop=self.loop)
        self.window.pack()

        self.title_screen = TitleScreen(self.window, self.game)
        self.title_screen()

    def loop(self, *args, **kwargs):
        self.game.next_turn()

    def print_game_window(self):
        with io.open("assets/screens/game", encoding='utf-8') as f:
            for i, line in enumerate(f):
                self.window.print(line, (0, i))