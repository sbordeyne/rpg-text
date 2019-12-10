class TkIOWrapper:
    """
        A class that redirects the iostream to a tkinter window.

        :param window: a tkinter widget with a write method.
    """
    def __init__(self, window):
        self.window = window

    def write(self, text, *args, **kwargs):
        self.window.write(text)

    def flush(self, *args, **kwargs):
        pass
