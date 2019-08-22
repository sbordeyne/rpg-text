import tkinter as tk
import _io


class TkIOWrapper(_io.TextIOWrapper):
    pass


class Window(tk.Frame):
    def __init__(self, master=None, size=(1024, 768), loop=None):
        super().__init__()
        self.master = master

        self.canvas = tk.Canvas(self, width=size[0], height=size[1], bg='black')
        self.canvas.pack()
        self.items = []
        self.persistent_items = []
        self._loop_callable = loop
        self.loop()

    def print(self, text, position, persistent=False, **kwargs):
        item = self.canvas.create_text(position, text=text, fill='white', font=('DejaVu Sans Mono', ), anchor=tk.NW,
                                       **kwargs)
        if persistent:
            self.persistent_items.append(item)
        else:
            self.items.append(item)
        return item

    def button(self, text, position, callback):
        t_id = self.print(text, position, fillactive='yellow')
        self.canvas.tag_bind(t_id, '<Button-1>', callback)

    def clear(self):
        while self.items:
            i = self.items.pop()
            self.canvas.delete(i)

    def loop(self):
        if callable(self._loop_callable):
            self._loop_callable()

        self.after(50, self.loop)