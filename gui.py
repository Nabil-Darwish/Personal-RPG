import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from rpg_enum import GUINotification
from util import Subject


class GUI(Subject):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.window_manager = WindowManager()

    def start_screen(self):
        self.notify_observers(GUINotification.MUSIC_PLAY)
        self.window_manager.start_window()
        self.starting_widgets()
        self.window_manager.window.mainloop()

    def update_title(self, title):
        self.title = title


    def query_player_name(self):
        self.window_manager.clear_frame()
        name_var = tk.StringVar()
        name_label = tk.Label(self.window_manager.window, text="What's your name?")
        name_entry = tk.Entry(self.window_manager.window, textvariable=name_var)
        name_submit = tk.Button(self.window_manager.window, text="Submit", command=lambda : self.notify_observers(GUINotification.PLAYER_NAME_SUBMITTED, name_var.get()))
        name_label.pack(padx=10, pady=10)
        name_entry.pack(padx=10, pady=10)
        name_submit.pack(padx=10, pady=10)

    def starting_widgets(self):
        self.window_manager.update_window(self.title)

        game_title_label = tk.Label(self.window_manager.window, text=self.title.upper(), font=("Castellar", 30))
        game_title_label.pack(padx=10, pady=10)

        start_button = tk.Button(self.window_manager.window, text="Start", height = 5, width = 30, command=self.query_player_name)
        start_button.pack(padx=10, pady=10)

    def preview_fonts(self):
        test_label = tk.Label(self.window_manager.window, text="TERRA\nINCOGNITA", font=("Courier", 30))
        test_label.pack(padx=10, pady=10)

        font_choice = tk.StringVar()

        combobox = ttk.Combobox(self.window_manager.window, values=sorted(tkFont.families()), textvariable=font_choice)
        combobox.pack(padx=10, pady=10)
        combobox.current()

        button_accept = tk.Button(self.window_manager.window, text="Accept", command=lambda : self.change_label_font(test_label, font_choice.get()))
        button_accept.pack(padx=10, pady=10)

    def initial_stats_screen(self, both_parties):
        self.window_manager.clear_frame()

        player_text = tk.Text(self.window_manager.window)
        player_text.grid(row=0, column=0)
        player_text.insert(tk.END, both_parties[0])
        player_text.tag_add("green", "1.0", "1.end")
        player_text.tag_config("green", foreground="green")

        enemy_text = tk.Text(self.window_manager.window)
        enemy_text.grid(row=0, column=2)
        enemy_text.insert(tk.END, both_parties[1])
        enemy_text.tag_add("red", "1.0", "1.end")
        enemy_text.tag_config("red", foreground="red")

        turn_1_button = tk.Button(self.window_manager.window, text="Go to turn 1", command=lambda: self.notify_observers(GUINotification.REQUEST_CURRENT_UNIT_TABLE))
        turn_1_button.grid(row=1, column=1)

    def combat_grid_screen(self, both_parties_tables):
        self.window_manager.clear_frame()

        player_table = tk.Text(self.window_manager.window)
        player_table.grid(row=0, column=0)
        player_table.insert(tk.END, both_parties_tables[0])
        player_table.tag_add("green", "1.0", "1.end")
        player_table.tag_config("green", foreground="green")

        enemy_table = tk.Text(self.window_manager.window)
        enemy_table.grid(row=0, column=1)
        enemy_table.insert(tk.END, both_parties_tables[1])
        enemy_table.tag_add("red", "1.0", "1.end")
        enemy_table.tag_config("red", foreground="red")

        attack_button = tk.Button(self.window_manager.window, text="Attack", command=lambda: self.notify_observers(GUINotification.PLAYER_ATTACK))
        attack_button.grid(row=1, column=0)

        heal_button = tk.Button(self.window_manager.window, text="Heal", command=lambda: self.notify_observers(GUINotification.PLAYER_HEAL))
        heal_button.grid(row=1, column=1)

        inventory_button = tk.Button(self.window_manager.window, text="Inventory", command=lambda: self.notify_observers(GUINotification.PLAYER_INVENTORY))
        inventory_button.grid(row=1, column=2)

    def change_label_font(self, label, font):
        label.configure(font=(font, 30)) # (font)


class WindowManager:
    def __init__(self):
        self.window = None

    def start_window(self):
        self.window = tk.Tk()
        self.window.title("RPG")
        self.window.geometry("800x600")

    def update_window(self, new_title):
        self.window.title(new_title)

    def clear_frame(self):
        for widget in self.window.winfo_children():
            widget.destroy()