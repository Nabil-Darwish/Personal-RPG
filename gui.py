import tkinter as tk
from rpg_enum import GUINotification

class ObserverNotFoundError(Exception):
    pass

class GUI:
    def __init__(self):
        self.observers = {}
        self.title = ""
        self.window_manager = WindowManager()

    def start_screen(self):
        self.notify_observers(GUINotification.MUSIC_PLAY)
        self.window_manager.start_window()
        button = tk.Button(self.window_manager.window, text="Change Music", command=lambda : self.notify_observers(GUINotification.MUSIC_CHANGE, "music/riff.wav"))
        button.pack(padx=10, pady=10)
        change_title_button = tk.Button(self.window_manager.window, text="Change Title", command=lambda : self.window_manager.update_window(self.title))
        change_title_button.pack(padx=10, pady=10)
        self.window_manager.window.mainloop()

    def add_observer(self, notification_type, observer):
        if notification_type not in self.observers:
            self.observers[notification_type] = []
        self.observers[notification_type].append(observer)

    def remove_observer(self, notification_type, observer):
        if observer in self.observers[notification_type]:
            self.observers[notification_type].remove(observer)
        else:
            raise ObserverNotFoundError("Observer not found in notification type given!")

    def notify_observers(self, notification_type, *args, **kwargs):
        if notification_type in self.observers:
            for observer in self.observers[notification_type]:
                observer(*args, **kwargs)

    def change_title(self, title):
        self.title = title

class WindowManager:
    def __init__(self):
        self.window = None

    def start_window(self):
        self.window = tk.Tk()
        self.window.title("RPG")
        self.window.geometry("800x600")

    def update_window(self, new_title):
        self.window.title(new_title)