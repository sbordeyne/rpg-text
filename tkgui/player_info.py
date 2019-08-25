class PlayerInfo:
    def __init__(self, manager):
        self.window = manager.window
        self.game = manager.game
        self.manager = manager
        self._bottom_index = 0
        self._top_index = 0
        self.bottom_num_pages = 3
        self.top_num_pages = 2

    def __call__(self):
        self.setup_ui()
        self.refresh_page()

    @property
    def bottom_index(self):
        return self._bottom_index

    @bottom_index.setter
    def bottom_index(self, value):
        if value < 0:
            self._bottom_index = self.bottom_num_pages - 1
        elif value > self.bottom_num_pages - 1:
            self._bottom_index = 0
        else:
            self._bottom_index = value

    @property
    def top_index(self):
        return self._top_index

    @top_index.setter
    def top_index(self, value):
        if value < 0:
            self._top_index = self.top_num_pages - 1
        elif value > self.top_num_pages - 1:
            self._top_index = 0
        else:
            self._top_index = value

    def setup_ui(self):
        self.window.print(self.game.player.name, (50, 1))
        self.window.print(self.game.player.job.name.capitalize(), (49, 2))
        self.window.print(f"Level - {self.game.player.level}", (67, 2))
        self.window.print(f'XP {self.game.player.experience}/{self.game.player.xp_to_next_level}', (49, 3))
        self.window.print(f'Health {self.game.player.health}/{self.game.player.max_health}', (49, 4))
        self.window.print(f'Mana {self.game.player.mana}/{self.game.player.max_mana}', (49, 5))

    def setup_equipmnt(self):
        self.window.print(' EQUIPMNT ', (57, 7))
        i = 0
        for slot_name, slot_item in self.game.player.inventory.equipped.as_dict.items():
            if not isinstance(slot_item, list):
                self.window.print(f'{slot_name.upper()} : {slot_item.capitalize()}', (49, 8 + i))
            else:
                self.window.print(f'{slot_name.upper()} : '
                                  f'{", ".join([s.capitalize() for s in slot_item])}', (49, 8 + i))
            i += 1

    def setup_commands(self):
        self.window.print(' COMMANDS ', (57, 7))
        pass

    def clear_page(self):
        self.window.print(' ' * 10, (57, 14))
        self.window.print(' ' * 10, (57, 7))
        for i in range(8):
            self.window.print(' ' * 29, (48, 15 + i))
        for i in range(6):
            self.window.print(' ' * 29, (48, 8 + i))

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

    def on_bottom_page_left(self, event):
        self.bottom_index -= 1
        self.refresh_page()

    def on_bottom_page_right(self, event):
        self.bottom_index += 1
        self.refresh_page()

    def on_top_page_left(self, event):
        self.top_index -= 1
        self.refresh_page()

    def on_top_page_right(self, event):
        self.top_index += 1
        self.refresh_page()

    def refresh_page(self):
        self.clear_page()
        [self.setup_stats, self.setup_saving_throws, self.setup_money][self.bottom_index]()
        [self.setup_equipmnt, self.setup_commands][self.top_index]()
        self.window.button('<', (56, 14), self.on_bottom_page_left)
        self.window.button('<', (56, 7), self.on_top_page_left)
        self.window.button('>', (67, 14), self.on_bottom_page_right)
        self.window.button('>', (67, 7), self.on_top_page_right)
