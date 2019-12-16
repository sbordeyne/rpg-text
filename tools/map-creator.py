import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog as fd
import string
from collections import defaultdict, OrderedDict
import json
import os.path


HELP_TXT = """
Map Creator GUI - Tool made by Dogeek for https://github.com/Dogeek/rpg-text

Click on the map to select a cell. You can then edit the cell info
to your liking.

Click on the save button in the Form once you are done editing the cell info.

Form attributes :

Position - current cell position, read only
Location Name - a unique name for this location.
Description - a description of the location shown to the player once he enters.
NPCs - A space-separated list of character names present in this cell.
Icon - An icon to represent this location on the map, must be a single character
Submaps - A space-separated list of submaps to enter from this location.
Exits - Tick in which directions the player can go from this location.
Save - Saves the current cell info.

Menubar :
Save - Saves the map file.
Load - Loads a map file.
Help - Show this window.

(c) Dogeek - 2019
"""


def get_avg_charwidth(widget=None, text=None):
    if text is None:
        text = string.printable
    if widget is None:
        font = tkfont.Font(font='TkTextFont')
    else:
        font = tkfont.Font(font=widget['font'])
    return sum([font.measure(c) for c in text]) / len(text)


class HelpWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.text = tk.Text(self, width=80, height=40)
        self.vsb = tk.Scrollbar(self, command=self.text.yview)
        self.text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.vsb.pack(side=tk.RIGHT, expand=True, fill=tk.Y)
        self.text.insert(tk.END, HELP_TXT)
        self.text.config(state=tk.DISABLED, xscrollcommand=self.vsb.set)


class DataSerializer:
    def __init__(self, filename='map.json'):
        self.filename = filename
        self.data = defaultdict(dict)

    def save(self, filename=None):
        fname = filename or self.filename
        self.filename = fname
        with open(fname, 'w') as f:
            json.dump(self.data, f, indent=4)

    def load(self, filename=None):
        fname = filename or self.filename
        self.filename = fname
        with open(self.filename) as f:
            data = json.load(f)
        self.data.update(data)

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

    def on_click(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)

        x = int(x - x % 16)
        y = int(y - y % 16)
        self.selected_position = (x, y)
        self.master.form_frame.load(*self.map_position)
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
        for var in self.exits_var:
            var.set(1)

        self.exits_frame = tk.Frame(self)
        self.form_entries = OrderedDict()
        self.form_labels = OrderedDict()
        self.form_exits = OrderedDict()
        self.form_entries_names = ('Location Name', 'Description', 'NPCs', 'Icon', "Submaps")
        self.exits_names = ('N', 'S', 'E', 'W')
        self.position_variable = tk.StringVar()
        self.position_variable.set('(0, 0)')
        self.position_label_lbl = tk.Label(self, text='Position : ')
        self.position_label = tk.Label(self, textvariable=self.position_variable)
        for entry in self.form_entries_names:
            self.form_labels[entry] = tk.Label(self, text=entry + ' :')
            if not entry == 'Description':
                self.form_entries[entry] = tk.Entry(self, textvariable=self.variables[entry], width=20)
            else:
                self.form_entries[entry] = tk.Text(self, width=20)
        for i, ext in enumerate(self.exits_names):
            self.form_exits[ext + '_label'] = tk.Label(self.exits_frame, text=ext + " :")
            self.form_exits[ext + '_checkbox'] = tk.Checkbutton(self.exits_frame, variable=self.exits_var[i])
        self.exits_label = tk.Label(self, text='Exits :')
        self.save_button = tk.Button(self, text='Save', command=self.save_btn)
        self.setup_ui()

    def set_position_label(self, x, y):
        self.position_variable.set(f'({x}, {y})')
        self.update()
        self.update_idletasks()

    def setup_ui(self):
        self.position_label_lbl.grid(row=0, column=0, sticky='w')
        self.position_label.grid(row=0, column=1, sticky='w')
        for i, entry_lbl in enumerate(self.form_labels.values()):
            entry_lbl.grid(row=i + 1, column=0, sticky='w')
        for i, entry_entry in enumerate(self.form_entries.values()):
            entry_entry.grid(row=i + 1, column=1, sticky='we')
        for i, w in enumerate(self.form_exits.values()):
            w.grid(row=0, column=i + 1)
        x = len(self.form_labels.values()) + 1
        self.exits_label.grid(row=x, column=0, sticky='w')
        self.exits_frame.grid(row=x, column=1, sticky='w')
        self.save_button.grid(row=x + 1, column=0, sticky='w')

    def save_btn(self, *args):
        self.master.canvas.position_saved()
        name = DataSerializer.format_name(self.variables['Location Name'].get())
        self.master.data.data[name] = {}
        self.master.data.data[name]['description'] = self.form_entries["Description"].get('1.0', tk.END)
        self.master.data.data[name]['map_icon'] = self.variables["Icon"].get()
        self.master.data.data[name]['npc'] = self.variables["NPCs"].get().split(' ')
        self.master.data.data[name]['position'] = list(self.master.canvas.map_position)
        self.master.data.data[name]['submaps'] = self.variables["Submaps"].get().split(' ')
        self.master.data.data[name]['exits'] = [en for e, en in zip(self.exits_var, self.exits_names) if e.get() == 1]

    def load(self, x, y):
        name = ""
        for key, val in self.master.data.data.items():
            if val.get('position') == [x, y]:
                name = key
                break

        if self.master.data.data[name] != {}:
            self.form_entries['Description'].delete('1.0', tk.END)
            self.form_entries["Description"].insert(tk.END, self.master.data.data[name]['description'])
            self.variables["Icon"].set(self.master.data.data[name]['map_icon'])
            self.variables["Location Name"].set(name)
            self.variables["NPCs"].set(" ".join(self.master.data.data[name]['npc']))
            for e, en in zip(self.exits_var, self.exits_names):
                e.set(1 if en in self.master.data.data[name]['exits'] else 0)
        else:
            self.form_entries['Description'].delete('1.0', tk.END)
            self.variables["Icon"].set("")
            self.variables["Location Name"].set("")
            self.variables["NPCs"].set("")
            for e in self.exits_var:
                e.set(0)


class MapCreatorGUI(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        kwargs['master'] = master
        super().__init__(*args, **kwargs)
        self.master = master
        self.help_window = None

        self.menubar = tk.Menu(self.master)
        self.menubar.add_command(label="Save", command=self._on_data_save)
        self.menubar.add_command(label="Load", command=self._on_data_load)
        self.menubar.add_command(label="Help", command=self._on_help)
        self.master.config(menu=self.menubar)

        self.form_frame = FormView(self)
        self.canvas = MapView(self, width=512, height=512, background='white')

        self.data = DataSerializer()

        master.bind('<Control-s>', self.data.save)
        master.bind('<Configure>', self.on_configure)
        self.setup_ui()
        self.loop()

    def setup_ui(self):
        self.canvas.pack(side=tk.LEFT)
        self.canvas.update()
        self.form_frame.pack(side=tk.LEFT)

    def on_configure(self, event):
        canvw = 512  # self.canvas['width']
        longest_label_name = sorted(self.form_frame.form_entries_names, key=len)[-1]
        margin_width = get_avg_charwidth(self.form_frame.form_labels[longest_label_name],
                                         longest_label_name) * len(longest_label_name)
        new_width = abs(int(self.winfo_width()) - int(canvw) - margin_width)
        cw = 8.8  # get_avg_charwidth()
        new_width_in_characters = int(new_width // cw)
        for entry in self.form_frame.form_entries_names:
            self.form_frame.form_entries[entry].config(width=new_width_in_characters)

    def _on_data_load(self, *args):
        fname = fd.askopenfilename()
        if not os.path.exists(fname):
            return
        self.data.load(fname)
        for v in [_ for _ in self.data.data.values() if _]:
            x, y = v['position']
            x *= 16
            y *= 16
            self.canvas.create_rectangle(x, y, x + 16, y + 16, stipple='gray50', fill='grey')

    def _on_data_save(self, *args):
        fname = fd.asksaveasfilename()
        self.data.save(fname)

    def _on_help(self, *args):
        def _on_help_close():
            self.help_window.destroy()
            self.help_window = None

        if self.help_window is None:
            self.help_window = tk.Toplevel(self)
            self.help_window.title("Help")
            self.help_window.resizable(False, False)
            gui = HelpWindow(self.help_window)
            gui.pack(expand=True, fill=tk.BOTH)
            self.help_window.protocol('WM_DELETE_WINDOW', _on_help_close)

    def loop(self):
        self.after(50, self.loop)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x525')
    root.minsize(800, 525)
    root.resizable(True, False)
    root.title('RPG Text Map Creator')
    window = MapCreatorGUI(root)
    window.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
