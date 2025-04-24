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
        self.query_player_name()
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
        else:
            raise ObserverNotFoundError("Observer not found in notification type given!")

    def change_title(self, title):
        self.title = title

    def query_player_name(self):
        name_var = tk.StringVar()
        name_label = tk.Label(self.window_manager.window, text="What's your name?")
        name_entry = tk.Entry(self.window_manager.window, textvariable=name_var)
        name_submit = tk.Button(self.window_manager.window, text="Submit", command=lambda : self.notify_observers(GUINotification.PLAYER_NAME_SUBMITTED, name_var.get()))
        name_label.pack(padx=10, pady=10)
        name_entry.pack(padx=10, pady=10)
        name_submit.pack(padx=10, pady=10)

class WindowManager:
    def __init__(self):
        self.window = None

    def start_window(self):
        self.window = tk.Tk()
        self.window.title("RPG")
        self.window.geometry("800x600")

    def update_window(self, new_title):
        self.window.title(new_title)