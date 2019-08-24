from .player_info import PlayerInfo


class History:
    def __init__(self):
        self.history = []
        self.height = 4
        self._index = 0

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError
        return self.history[index]

    def __iter__(self):
        return iter(self.history[self.index - self.height:self.index])

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if isinstance(value, str):
            if value.lower() == 'end':
                self._index = len(self.history)
            elif value.lower() == 'home':
                self._index = self.height
            else:
                raise ValueError
        elif isinstance(value, int):
            self._index = min(max(value, 0), len(self.history))
        else:
            raise TypeError

    def add(self, text):
        self.history.append(text)
        self.index = len(self.history)

    def move(self, event):
        if event.keysym == 'Prior':
            self.index -= 1
        elif event.keysym == 'Next':
            self.index += 1
        else:
            self.index = event.keysym


class MainScreen:
    def __init__(self, manager):
        self.manager = manager
        self.command = ""
        self.player_info = PlayerInfo(manager)
        self.history = History()

    def __call__(self, *args, **kwargs):
        self.manager.window.clear()
        self.manager.print_asset('game')
        self.manager.window.master.bind('<Key>', self.on_keypress)
        self.setup_ui()

    def setup_ui(self):
        self.player_info()
        self.manager.window.print(">", (5, 28))

    def on_keypress(self, event):
        if event.keysym in ('BackSpace', 'Delete'):
            self.command = self.command[:-1]
        elif event.keysym == 'Return':
            self.manager.window.did_action = True
            self.manager.window.print(' ' * 70, (7, 28))
            return
        elif event.keysym in ('Prior', 'Next', 'Home', 'End'):
            self.history.move(event)
            self.update_ui()
            return
        else:
            self.command += event.char
        self.manager.window.print(' ' * 70, (7, 28))
        self.manager.window.print(self.command, (7, 28))
        if len(self.command) < 70:
            self.manager.window.print('_', (7 + len(self.command), 28))

    def write(self, text):
        if text:
            self.history.add(text)
            self.update_ui()

    def update_ui(self):
        for i, line in enumerate(self.history):
            self.manager.window.print(" " * 76, (3, 24 + i))
            self.manager.window.print(line, (3, 24 + i))
