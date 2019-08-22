import tkinter as tk


class Window(tk.Frame):
    def __init__(self, master=None, size=(1024, 768)):
        super().__init__()
        self.master = master

        self.canvas = tk.Canvas(self, width=size[0], height=size[1], bg='black')
        self.canvas.pack()
        self.items = []

    def print(self, text, position, **kwargs):
        item = self.canvas.create_text(position, text=text, fill='white', **kwargs)
        self.items.append(item)
        return item

    def button(self, text, position, callback):
        t_id = self.print(text, position, fillactive='yellow')
        self.canvas.tag_bind(t_id, '<Button-1>', callback)

    def clear(self):
        while self.items:
            i = self.items.pop()
            self.canvas.delete(i)


if __name__ == '__main__':
    root = tk.Tk()
    window = Window(root)
    window.pack()
    root.mainloop()
