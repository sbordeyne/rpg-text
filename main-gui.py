from tkgui.window_manager import WindowManager
import tkinter as tk
import sys


if __name__ == '__main__':
    root = tk.Tk()
    manager = WindowManager(root)
    sys.stdout = manager.io_wrapper
    root.mainloop()
