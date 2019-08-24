from .player_info import PlayerInfo


class MainScreen:
    def __init__(self, manager):
        self.manager = manager
        self.player_info = PlayerInfo(manager)

    def __call__(self, *args, **kwargs):
        self.manager.window.clear()
        self.manager.print_asset('game')
        self.setup_ui()

    def setup_ui(self):
        self.player_info()
