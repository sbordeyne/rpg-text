from rpglib.utils import parse_dice_format
from tkgui.window_manager import WindowManager
import tkinter as tk


def new_game(game):
    p_name = "Dogeek"
    p_job = "warrior"
    game.player.name = p_name
    game.player.job = p_job
    game.player.health_rolls.append(parse_dice_format(game.player.job.hp_die))
    game.player.mana_rolls.append(parse_dice_format(game.player.job.mp_die))
    game.player.stats.randomize()
    game.player.health = game.player.max_health
    game.player.inventory.money.get_random_starting_money()


if __name__ == '__main__':
    root = tk.Tk()
    manager = WindowManager(root)
    root.mainloop()
