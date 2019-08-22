import tkinter as tk
from tkgui.window import Window
import io
from rpglib.game import Game


game = Game()


def loop():
    global game
    while True:
        game.next_turn()


root = tk.Tk()
window = Window(root)  # , loop=loop)
window.pack()

with io.open("assets/screens/game", encoding='utf-8') as f:
    for i, line in enumerate(f):
        window.print(line, (0, i * 20), persistent=True)

root.mainloop()