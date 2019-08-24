from .player_info import PlayerInfo


class MainScreen:
    def __init__(self, manager):
        self.manager = manager
        self.command = ""
        self.player_info = PlayerInfo(manager)

    def __call__(self, *args, **kwargs):
        self.manager.window.clear()
        self.manager.print_asset('game')
        self.manager.window.master.bind('<Key>', self.on_keypress)
        self.setup_ui()

    def setup_ui(self):
        self.player_info()
        self.manager.window.print(">", (5, 28))

    def on_keypress(self, event):
        print(self.command)
        if event.keysym in ('BackSpace', 'Delete'):
            self.command = self.command[:-1]
        elif event.keysym == 'Return':
            self.manager.window.did_action = True
            self.manager.window.print(' ' * 10, (7, 28))
            return
        self.command += event.char
        self.manager.window.print(' ' * 10, (7, 28))
        self.manager.window.print(self.command, (7, 28))
        if len(self.command) < 70:
            self.manager.window.print('_', (7 + len(self.command), 28))