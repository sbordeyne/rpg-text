import sys
from copy import copy
from rpglib.utils import parse_dice_format
import os


class LoadGameScreen:
    def __init__(self, manager):
        self.manager = manager
        self.start_index = 0
        self.end_index = 24
        self.nb_saves = 0
        self.saves = [(sn, lambda evt: self.load_save(sn))
                      for sn in os.listdir('./saves') if sn.endswith('json')][self.start_index:self.end_index]
        self.saves.insert(0, ("NEW GAME", self.new_game))

    def __call__(self, *args, **kwargs):
        self.manager.window.clear()
        self.setup_ui()

    def setup_ui(self):
        self.manager.print_asset('load_game_frame')
        self.manager.window.print('LOAD GAME', (7, 1))
        self.manager.window.button('↑', (77, 2), self.move_up)
        self.manager.window.button('↓', (77, 27), self.move_down)
        self.update_ui()

    def move_up(self, event):
        if self.nb_saves > 24:
            self.start_index = max(self.start_index - 1, 0)
            self.end_index = min(self.end_index - 1, 24)
        self.update_ui()

    def move_down(self, event):
        if self.nb_saves > 24:
            self.start_index = min(self.start_index + 1, self.nb_saves)
            self.end_index = min(self.end_index + 1, self.nb_saves + 24)
        self.update_ui()

    def update_ui(self):
        self.nb_saves = len(self.saves)
        for i, save in enumerate(self.saves):
            save_name, save_callback = save
            self.manager.window.print(' ' * 72, (5, 3 + i))
            self.manager.window.button(save_name.upper(), (5, 3 + i), save_callback)

    def new_game(self, event):
        self.manager.title_screen.new_game_screen()

    def load_save(self, save_name):
        self.manager.game.save_system.load(save_name)
        self.manager.main_screen()


class NewGameScreen:
    def __init__(self, manager):
        self.manager = manager
        self.job_name = None
        self.saved_health = [2]
        self.saved_mana = [2]
        self.saved_stats = {k: 9 for k in ('str', 'int', 'chr', 'con', 'wis', 'dex')}
        self.player_name = ""
        self.points_to_reassign = 0

    def __call__(self, *args, **kwargs):
        self.manager.window.clear()
        self.manager.window.master.bind('<Key>', self.on_keypress)
        self.setup_ui()

    def setup_ui(self):
        self.manager.print_asset('new_game_frame')
        self.manager.window.print('NEW GAME', (7, 1))
        self.manager.window.print('NAME : _', (7, 3))
        self.manager.window.print('JOB  :', (7, 5))
        self.manager.window.button('WARRIOR', (14, 5), self.select_job_warrior)
        self.manager.window.button('THIEF', (23, 5), self.select_job_thief)
        self.manager.window.button('WIZARD', (29, 5), self.select_job_wizard)
        self.manager.window.button('CLERIC', (36, 5), self.select_job_cleric)
        self.manager.window.print('STATS', (9, 8))

    def on_keypress(self, event):
        if self.job_name is None:
            if event.keysym in ('BackSpace', 'Delete'):
                self.player_name = self.player_name[:-1]
            elif len(self.player_name) < 8:
                self.player_name += event.char
            self.manager.window.print(' ' * 10, (14, 3))
            self.manager.window.print(self.player_name, (14, 3))
            if len(self.player_name) < 8:
                self.manager.window.print('_', (14 + len(self.player_name), 3))

    def select_job_warrior(self, event):
        self.job_name = 'warrior'
        self.clear_job_line()

    def select_job_thief(self, event):
        self.job_name = 'thief'
        self.clear_job_line()

    def select_job_wizard(self, event):
        self.job_name = 'wizard'
        self.clear_job_line()

    def select_job_cleric(self, event):
        self.job_name = 'cleric'
        self.clear_job_line()

    def clear_job_line(self):
        self.manager.game.player.name = self.player_name if self.player_name else "Milten"
        self.manager.game.player.job = self.job_name
        self.manager.window.print(' ' * 28, (14, 5))
        self.manager.window.print(' ' * 10, (14, 3))
        self.manager.window.print(self.job_name.upper(), (14, 5))
        self.manager.window.print(self.manager.game.player.name.capitalize(), (14, 3))
        self.manager.window.button(' REROLL ', (55, 10), self.roll_stats)
        self.manager.window.button('  SAVE  ', (55, 12), self.save_stats)
        self.manager.window.button(' RECALL ', (55, 14), self.recall_stats)
        self.manager.window.button('CONTINUE', (55, 16), self.start_game)

        stats = ('str', 'int', 'wis', 'dex', 'con', 'chr')
        self.manager.window.button('<', (18, 10 + 2 * 0), lambda evt: self.decrease_stat('str'))
        self.manager.window.button('>', (20, 10 + 2 * 0), lambda evt: self.increase_stat('str'))
        self.manager.window.button('<', (18, 10 + 2 * 1), lambda evt: self.decrease_stat('int'))
        self.manager.window.button('>', (20, 10 + 2 * 1), lambda evt: self.increase_stat('int'))
        self.manager.window.button('<', (18, 10 + 2 * 2), lambda evt: self.decrease_stat('wis'))
        self.manager.window.button('>', (20, 10 + 2 * 2), lambda evt: self.increase_stat('wis'))
        self.manager.window.button('<', (18, 10 + 2 * 3), lambda evt: self.decrease_stat('dex'))
        self.manager.window.button('>', (20, 10 + 2 * 3), lambda evt: self.increase_stat('dex'))
        self.manager.window.button('<', (18, 10 + 2 * 4), lambda evt: self.decrease_stat('con'))
        self.manager.window.button('>', (20, 10 + 2 * 4), lambda evt: self.increase_stat('con'))
        self.manager.window.button('<', (18, 10 + 2 * 5), lambda evt: self.decrease_stat('chr'))
        self.manager.window.button('>', (20, 10 + 2 * 5), lambda evt: self.increase_stat('chr'))

        self.roll_stats()

    def decrease_stat(self, stat_name):
        if self.manager.game.player.stats[stat_name] > 3:
            self.manager.game.player.stats[stat_name]._value -= 1
            self.points_to_reassign += 1
            self.update_ui()
        pass

    def increase_stat(self, stat_name):
        if self.points_to_reassign > 0 and self.manager.game.player.stats[stat_name] < 18:
            self.manager.game.player.stats[stat_name]._value += 1
            self.points_to_reassign -= 1
            self.update_ui()
        pass

    def roll_stats(self, *event):
        self.manager.game.player.stats.randomize()
        self.manager.game.player.health_rolls = []
        self.manager.game.player.health_rolls.append(parse_dice_format(self.manager.game.player.job.hp_die))
        self.manager.game.player.mana_rolls = []
        self.manager.game.player.mana_rolls.append(parse_dice_format(self.manager.game.player.job.mp_die))
        self.update_ui()

    def save_stats(self, *event):
        self.saved_health = copy(self.manager.game.player.health_rolls)
        self.saved_mana = copy(self.manager.game.player.mana_rolls)
        self.saved_stats = self.manager.game.player.stats.as_dict
        self.update_ui()

    def recall_stats(self, *event):
        self.manager.game.player.health_rolls = copy(self.saved_health)
        self.manager.game.player.mana_rolls = copy(self.saved_mana)
        self.manager.game.player.stats.recall_stats(self.saved_stats)
        self.update_ui()

    def start_game(self, *event):
        self.manager.game.player.health = self.manager.game.player.max_health
        self.manager.game.player.mana = self.manager.game.player.max_mana
        self.manager.game.player.inventory.money.get_random_starting_money()
        self.manager.main_screen()
        pass

    def update_ui(self):
        stats = ('str', 'int', 'wis', 'dex', 'con', 'chr')
        for i, stat_name in enumerate(stats):
            stat_value = self.manager.game.player.stats.as_dict[stat_name]
            self.manager.window.print(f'{stat_name.upper()}  :  {stat_value:2}', (6, 10 + 2 * i))

        self.manager.window.print("HEALTH :", (50, 3))
        self.manager.window.print("MANA   :", (50, 5))

        self.manager.window.print(f'{self.manager.game.player.max_health:2}', (60, 3))
        self.manager.window.print(f'{self.manager.game.player.max_mana:2}', (60, 5))

        self.manager.window.print(f'POINTS : {self.points_to_reassign:3}', (30, 23))
        self.manager.window.print(f'TOTAL  : '
                                  f'{sum(self.manager.game.player.stats.as_dict.values()) + self.points_to_reassign:3}',
                                  (30, 25))
        self.manager.window.print(f'SAVED  : {sum(self.saved_stats.values()):3}', (30, 27))


class TitleScreen:
    def __init__(self, manager):
        self.game = manager.game
        self.window = manager.window
        self.manager = manager
        self.new_game_screen = NewGameScreen(manager)
        self.load_game_screen = LoadGameScreen(manager)

    def __call__(self):
        self.window.clear()
        self.setup_ui()

    def setup_ui(self):
        self.window.button("> NEW  GAME", (30, 10), self.new_game_screen, font=('DejaVu Sans Mono', 15, 'bold'))
        self.window.button("> LOAD GAME", (30, 12), self.load_game_screen, font=('DejaVu Sans Mono', 15, 'bold'))
        self.window.button("> QUIT GAME", (30, 14), self.quit_game, font=('DejaVu Sans Mono', 15, 'bold'))

    def load_game(self, event):
        pass

    def quit_game(self, event):
        """Saves and quits the game. Save is named 'autosave'"""
        self.game.save_system.save("autosave")
        self.window.clear()
        sys.exit(1)