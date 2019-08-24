class PlayerInfo:
    def __init__(self, manager):
        self.window = manager.window
        self.game = manager.game
        self.manager = manager
        self._index = 0
        self.num_pages = 3

    def __call__(self):
        self.setup_ui()
        self.refresh_page()

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if value < 0:
            self._index = self.num_pages - 1
        elif value > self.num_pages - 1:
            self._index = 0
        else:
            self._index = value

    def setup_ui(self):
        self.window.print(self.game.player.name, (50, 1))
        self.window.print(self.game.player.job.name.capitalize(), (49, 2))
        self.window.print(f"Level - {self.game.player.level}", (67, 2))
        self.window.print(f'XP {self.game.player.experience}/{self.game.player.xp_to_next_level}', (49, 3))
        self.window.print(f'Health {self.game.player.health}/{self.game.player.max_health}', (49, 4))
        self.window.print(f'Mana {self.game.player.mana}/{self.game.player.max_mana}', (49, 5))

    def clear_page(self):
        self.window.print(' ' * 10, (57, 14))
        for i in range(8):
            self.window.print(' ' * 29, (48, 15 + i))

    def setup_stats(self):
        self.window.print('STATS', (59, 14))
        i = 0
        for key, value in self.game.player.stats.as_dict.items():
            self.window.print(f'{key.upper()}   -  {value}', (49, 15 + i))
            i += 1

    def setup_saving_throws(self):
        self.window.print('SAV.THROWS', (57, 14))
        i = 0
        for key, value in self.game.player.job.saving_throws.as_dict.items():
            self.window.print(f'{key.upper()}   -  {value}', (49, 15 + i))
            i += 1

    def setup_money(self):
        self.window.print('  MONEY   ', (57, 14))
        i = 0
        for key, value in self.game.player.inventory.money.coins.items():
            self.window.print(f'{key.upper()} :  {value}', (49, 15 + i))
            i += 1
        self.window.print(f'GEMS   :  {self.game.player.inventory.money.gems_value}   GC', (49, 15 + i))
        self.window.print(f'JEWELS :  {self.game.player.inventory.money.jewels_value}   GC', (49, 16 + i))
        self.window.print(f'TOTAL  :  {self.game.player.inventory.money.value:02} GC', (49, 17 + i))

    def on_page_left(self, event):
        self.index -= 1
        self.refresh_page()

    def on_page_right(self, event):
        self.index += 1
        self.refresh_page()

    def refresh_page(self):
        self.clear_page()
        [self.setup_stats, self.setup_saving_throws, self.setup_money][self.index]()
        self.window.button('<', (56, 14), self.on_page_left)
        self.window.button('>', (67, 14), self.on_page_right)
