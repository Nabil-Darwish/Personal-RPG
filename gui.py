import tkinter as tk
from rpg_enum import GUINotification

class ObserverNotFoundError(Exception):
    pass

class GUI:
    def __init__(self):
        self.observers = {}
        self.title = ""

    def start_screen(self):
        self.notify_observers(GUINotification.MUSIC_PLAY)
        window = tk.Tk()
        window.title(self.title)
        window.geometry("800x600")
        button = tk.Button(window, text="Change Music", command=lambda : self.notify_observers(GUINotification.MUSIC_CHANGE, "music/riff.wav"))
        button.pack(padx=10, pady=10)
        window.mainloop()

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