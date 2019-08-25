import _io


class TkIOWrapper:  # (_io.TextIOWrapper):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window

    def write(self, text, *args, **kwargs):
        self.window.write(text)
    pass

    def flush(self, *args, **kwargs):
        pass
