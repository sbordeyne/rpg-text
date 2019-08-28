import tkinter as tk
from collections import defaultdict, OrderedDict
import json


class DataSerializer:
    def __init__(self, filename='map.json'):
        self.filename = filename
        self.data = defaultdict(dict)

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    @staticmethod
    def format_name(name):
        return name.replace(" ", "_").replace("'", "").lower()


class MapView(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(0, 513, 16):
            self.create_line(0, i, 512, i, fill='grey')
            self.create_line(i, 0, i, 512, fill='grey')
        self.cursor = self.create_rectangle((0, 0, 16, 16))
        self.selected_position = (0, 0)
        self.bind('<Button-1>', self.on_click)
        pass

    def on_click(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)

        x = int(x - x % 16)
        y = int(y - y % 16)
        self.selected_position = (x, y)
        self.master.form_frame.set_position_label(*self.map_position)
        self.coords(self.cursor, x, y, x + 16, y + 16)

    @property
    def map_position(self):
        x, y = self.selected_position
        return x // 16, y // 16

    def position_saved(self):
        x, y = self.selected_position
        self.create_rectangle(x, y, x + 16, y + 16, stipple='gray50', fill='grey')


class FormView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variables = defaultdict(tk.StringVar)
        self.exits_var = [tk.IntVar() for i in range(4)]

        self.exits_frame = tk.Frame(self)
        self.form_entries = OrderedDict()
        self.form_labels = OrderedDict()
        self.form_exits = OrderedDict()
        self.form_entries_names = ('Location Name', 'Description', 'NPCs', 'Icon')
        self.exits_names = ('N', 'S', 'E', 'W')
        self.position_label_lbl = tk.Label(self, text='Position :')
        self.position_label = tk.Label(self, text='(0, 0)')
        for entry in self.form_entries_names:
            self.form_labels[entry] = tk.Label(self, text=entry + ' :')
            if not entry == 'Description':
                self.form_entries[entry] = tk.Entry(self, textvariable=self.variables[entry])
            else:
                self.form_entries[entry] = tk.Text(self)
        for i, ext in enumerate(self.exits_names):
            self.form_exits[ext + '_label'] = tk.Label(self.exits_frame, text=ext + " :")
            self.form_exits[ext + '_checkbox'] = tk.Checkbutton(self.exits_frame, variable=self.exits_var[i])
        self.exits_label = tk.Label(self, text='Exits :')
        self.save_button = tk.Button(self, text='Save', command=self.save_btn)
        self.setup_ui()

    def setup_ui(self):
        self.position_label_lbl.grid(row=0, column=0)
        self.position_label.grid(row=0, column=1)
        for i, entry_lbl in enumerate(self.form_labels.values()):
            entry_lbl.grid(row=i + 1, column=0)
        for i, entry_entry in enumerate(self.form_entries.values()):
            entry_entry.grid(row=i + 1, column=1, sticky='we')
        for i, ety in enumerate(self.form_exits.values()):
            ety.grid(row=0, column=i + 1)
        x = len(self.form_labels.values()) + 1
        self.exits_label.grid(row=x, column=0)
        self.exits_frame.grid(row=x, column=1)
        self.save_button.grid(row=x + 1, column=0)

    def save_btn(self, *args):
        self.master.canvas.position_saved()
        name = DataSerializer.format_name(self.variables['Location Name'].get())
        self.master.data.data[name] = {}
        self.master.data.data[name]['description'] = self.form_entries["Description"].get('1.0', tk.END)
        self.master.data.data[name]['map_icon'] = self.variables["Icon"].get()
        self.master.data.data[name]['npc'] = self.variables["NPCs"].get().split(' ')
        self.master.data.data[name]['position'] = list(self.master.canvas.map_position)
        self.master.data.data[name]['exits'] = [en for e, en in zip(self.exits_var, self.exits_names) if e.get() == 1]

    def set_position_label(self, x, y):
        self.position_label.config(text=f'({x}, {y})')


class MapCreatorGUI(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        kwargs['master'] = master
        super().__init__(*args, **kwargs)
        self.master = master

        self.form_frame = FormView(self)
        self.canvas = MapView(self, width=512, height=512, background='white')

        self.data = DataSerializer()

        self.setup_ui()
        self.loop()

    def setup_ui(self):
        self.canvas.pack(side=tk.LEFT)
        self.canvas.update()
        self.form_frame.pack(side='top')

        pass

    def loop(self):
        self.after(50, self.loop)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x512')
    root.resizable(False, False)
    root.title('RPG Text Map Creator')
    window = MapCreatorGUI(root)
    window.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
