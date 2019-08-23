import tkinter as tk


class Window(tk.Frame):
    def __init__(self, master=None, width=80, aspect_ratio=4/3, loop=None):
        super().__init__()
        self.master = master

        self.master.resizable(False, False)

        self.width = width
        self.height = int(round(width / aspect_ratio, 0))
        w = width * 10
        h = self.height * 10

        self.canvas = tk.Canvas(self, width=w, height=h, bg='black')
        self.canvas.pack()
        self.items = []

        for x in range(self.width + 1):
            items = []
            for y in range(self.height):
                items.append(self.canvas.create_text((x * 10, y * 20), text=" ", fill="white",
                                                     font=('DejaVu Sans Mono', ), anchor=tk.NW))
            self.items.append(items)

        self._loop_callable = loop
        self.did_action = False
        self.loop()

    def print(self, text, position, **kwargs):
        x_start, y_start = position
        for i, character in enumerate(text):
            x = min(x_start + i, self.width)
            y = min(y_start, self.height)
            iid = self.items[x][y]
            self.canvas.itemconfigure(iid, text=character, **kwargs)

    def button(self, text, position, callback):
        def highlight(evt):
            self.canvas.itemconfigure(tag_name, fill='yellow')

        def de_highlight(evt):
            self.canvas.itemconfigure(tag_name, fill='white')

        tag_name = f'button-{position[0]}{position[1]}'
        self.print(text, position, tags=tag_name)
        self.canvas.tag_bind(tag_name, '<Button-1>', callback)
        self.canvas.tag_bind(tag_name, '<Enter>', highlight)
        self.canvas.tag_bind(tag_name, '<Leave>', de_highlight)

    def clear(self):
        self.items = []

        for x in range(self.width + 1):
            items = []
            for y in range(self.height):
                items.append(self.canvas.create_text((x * 10, y * 20), text=" ", fill="white",
                                                     font=('DejaVu Sans Mono', ), anchor=tk.NW))
            self.items.append(items)

    def loop(self):
        if callable(self._loop_callable) and self.did_action:
            self._loop_callable()
            self.did_action = False

        self.after(50, self.loop)