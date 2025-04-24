import tkinter as tk
import music

class GUI:
    def __init__(self):
        self.start_screen()
        self.observers = {}

    def start_screen(self):
        window = tk.Tk()
        window.title("Terra Incognita")
        window.geometry("1200x800")
        button = tk.Button(window, text="Change Music", command=lambda : music.change_music("music/riff.wav"))
        button.pack(padx=10, pady=10)
        window.mainloop()

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)