import sys


class TitleScreen:
    def __init__(self, window, game):
        self.game = game
        self.window = window

    def __call__(self):
        self.window.clear()
        self.setup_ui()

    def setup_ui(self):
        self.window.button("> NEW  GAME", (30, 10), self.new_game, font=('DejaVu Sans Mono', 15, 'bold'))
        self.window.button("> LOAD GAME", (30, 12), self.load_game, font=('DejaVu Sans Mono', 15, 'bold'))
        self.window.button("> QUIT GAME", (30, 14), self.quit_game, font=('DejaVu Sans Mono', 15, 'bold'))

    def load_game(self, event):
        pass

    def new_game(self, event):
        pass

    def quit_game(self, event):
        """Saves and quits the game. Save is named 'autosave'"""
        self.game.save_system.save("autosave")
        self.window.clear()
        sys.exit(1)