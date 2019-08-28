import tkinter as tk
from collections import defaultdict, OrderedDict
import json


class MapCreatorGUI(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        kwargs['master'] = master
        super().__init__(*args, **kwargs)
        self.master = master
        self.variables = defaultdict(tk.StringVar)
        self.exits_var = [tk.IntVar() for i in range(4)]

        self.canvas = tk.Canvas(self, width=512, height=768)
        self.form_frame = tk.Frame(self)
        self.exits_frame = tk.Frame(self.form_frame)
        self.form_entries = OrderedDict()
        self.form_labels = OrderedDict()
        self.form_exits = OrderedDict()
        self.form_entries_names = ('Location Name', 'Description', 'NPCs', 'Icon')
        self.exits_names = ('N', 'S', 'E', 'W')
        for entry in self.form_entries_names:
            self.form_labels[entry] = tk.Label(self.form_frame, text=entry + ' :')
            self.form_entries[entry] = tk.Entry(self.form_frame, textvariable=self.variables[entry])
        for i, ext in enumerate(self.exits_names):
            self.form_exits[ext + '_label'] = tk.Label(self.exits_frame, text=ext + " :")
            self.form_exits[ext + '_checkbox'] = tk.Checkbutton(self.exits_frame, variable=self.exits_var[i])
        self.exits_label = tk.Label(self.form_frame, text='Exits :')
        self.setup_ui()
        self.loop()

    def setup_ui(self):
        self.canvas.grid(row=0, column=0)
        self.form_frame.grid(row=0, column=1, sticky='we')
        for i, entry_lbl in enumerate(self.form_labels.values()):
            entry_lbl.grid(row=i, column=0)
        for i, entry_entry in enumerate(self.form_entries.values()):
            entry_entry.grid(row=i, column=1, sticky='we')
        for i, ety in enumerate(self.form_exits.values()):
            ety.grid(row=0, column=i)
        x = len(self.form_labels.values())
        self.exits_label.grid(row=x, column=0)
        self.exits_frame.grid(row=x, column=1)
        pass

    def loop(self):
        self.after(50, self.loop)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1024x768')
    root.resizable(False, False)
    root.title('RPG Text Map Creator')
    window = MapCreatorGUI(root)
    window.grid(row=0, column=0, sticky='nswe')
    root.mainloop()
