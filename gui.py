import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from typing import List

from rpg_enum import GUINotification
from util import Subject


class GUI(Subject):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.window_manager = WindowManager()

    def start_screen(self):
        # Send notification to start music
        self.notify_observers(GUINotification.MUSIC_PLAY)

        # Load starting window
        self.window_manager.start_window()
        self.starting_widgets()

        # Run mainloop
        self.window_manager.window.mainloop()

    def update_title(self, title):
        self.title = title

    def query_player_name(self):
        # Clear frame
        self.window_manager.clear_frame()

        # Ask for player name
        name_var = tk.StringVar()
        name_label = tk.Label(self.window_manager.window, text="What's your name?")
        name_entry = tk.Entry(self.window_manager.window, textvariable=name_var)

        # Add submit button. It raises the flag that player name is submitted and sends the player name to the game
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

        # Create a player textbox to preview stats
        player_text = tk.Text(self.window_manager.window)
        # player_text.grid(row=0, column=0)
        player_text.place(x=0, y=10, width = 600, height = 300)
        player_text.insert(tk.END, both_parties[0])
        player_text.tag_add("green", "1.0", "1.end")
        player_text.tag_config("green", foreground="green")

        # Create an enemy textbox to preview stats
        enemy_text = tk.Text(self.window_manager.window)
        # enemy_text.grid(row=0, column=2)
        enemy_text.place(x=600, y=10, width = 600, height = 300)
        enemy_text.insert(tk.END, both_parties[1])
        enemy_text.tag_add("red", "1.0", "1.end")
        enemy_text.tag_config("red", foreground="red")

        # Create a button to start the battle. It raises the flag calling for the current unit table
        turn_1_button = tk.Button(self.window_manager.window, text="Start battle!", command=lambda: self.notify_observers(GUINotification.REQUEST_CURRENT_UNIT_TABLE))
        turn_1_button.place(x=550, y=320, width = 100, height = 50)

    # This is called when the combat grid needs to be shown. Receives party tables and party lists
    def combat_grid_screen(self, both_parties_tables, both_parties_name_lists: List[List[str]]):
        self.window_manager.clear_frame()

        # Create a frame
        player_frame = tk.Frame(self.window_manager.window)
        player_frame.place(x=0, y=10, width = 600, height = 300)

        # Create player scrollbar
        player_scrollbar = tk.Scrollbar(player_frame, orient = tk.HORIZONTAL)
        player_scrollbar.pack(side=tk.BOTTOM, fill = tk.X)

        # Create player table
        player_table = tk.Text(player_frame, wrap=tk.NONE, xscrollcommand=player_scrollbar.set)
        player_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        player_table.insert(tk.END, both_parties_tables[0])
        player_table.tag_add("green", "1.0", "1.end")
        player_table.tag_config("green", foreground="green")

        # Configure the player scrollbar
        player_scrollbar.config(command=player_table.xview)

        # Create enemy frame
        enemy_frame = tk.Frame(self.window_manager.window)
        enemy_frame.place(x=600, y=10, width = 600, height = 300)

        # Create enemy scrollbar
        enemy_scrollbar = tk.Scrollbar(enemy_frame, orient = tk.HORIZONTAL)
        enemy_scrollbar.pack(side=tk.BOTTOM, fill = tk.X)

        # Create enemy table
        enemy_table = tk.Text(enemy_frame, wrap=tk.NONE, xscrollcommand=enemy_scrollbar.set)
        enemy_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        enemy_table.insert(tk.END, both_parties_tables[1])
        enemy_table.tag_add("red", "1.0", "1.end")
        enemy_table.tag_config("red", foreground="red")

        # Configure the enemy scrollbar
        enemy_scrollbar.config(command=enemy_table.xview)

        # Create log frame
        log_frame = tk.Frame(self.window_manager.window)
        log_frame.place(x=0, y=310, width = 800, height = 200)

        # Create log title on left
        log_title = tk.Label(log_frame, text="Combat log", font=("Arial", 12, "bold"), justify="left")
        log_title.pack(padx=2, anchor="w")

        # Create log scrollbar
        log_scrollbar = tk.Scrollbar(log_frame, orient = tk.VERTICAL)
        log_scrollbar.pack(side=tk.RIGHT, fill = tk.Y)

        # Create log textbox
        log = tk.Text(log_frame, wrap=tk.NONE, yscrollcommand=log_scrollbar.set)
        log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log.insert(tk.END, "Battle start!")

        # Create functions for activating and deactivating buttons
        def action_buttons_inactivated():
            attack_button.config(state = tk.DISABLED)
            heal_button.config(state = tk.DISABLED)
            inventory_button.config(state = tk.DISABLED)

        def action_buttons_activated():
            attack_button.config(state = tk.NORMAL)
            heal_button.config(state = tk.NORMAL)
            inventory_button.config(state = tk.NORMAL)

        # Create action buttons.
        # Attack button. Allows the player to select an enemy to attack. Sends the activation and inactivation functions to the select_one_from_enemies function
        attack_button = tk.Button(self.window_manager.window, text="Attack", command=lambda: self.select_one_from_enemies(both_parties_name_lists[1], action_buttons_inactivated, action_buttons_activated))
        attack_button.place(x=800, y=320, width = 100, height = 25)

        # Heal button. Allows the player to select an ally to heal. Sends the activation and inactivation functions to the select_one_from_allies function
        heal_button = tk.Button(self.window_manager.window, text="Heal", command=lambda: self.select_one_from_allies(both_parties_name_lists[0], action_buttons_inactivated, action_buttons_activated))
        heal_button.place(x=800, y=345, width = 100, height = 25)

        # Inventory button
        inventory_button = tk.Button(self.window_manager.window, text="Inventory", command=lambda: self.notify_observers(GUINotification.PLAYER_INVENTORY))
        inventory_button.place(x=800, y=370, width = 100, height = 25)


    def select_one_from_enemies(self, enemies: List[str], action_buttons_inactivated, action_buttons_activated):
        # Deactivate the action buttons
        action_buttons_inactivated()

        # Create selection frame
        pick_enemy_frame = tk.Frame(self.window_manager.window)
        pick_enemy_frame.place(x=900, y=400, width = 300, height = 200)

        # Create selection combobox
        pick_enemy_combobox = ttk.Combobox(pick_enemy_frame, values=enemies)
        pick_enemy_combobox.set("Pick an enemy")
        pick_enemy_combobox.place(x=100, y=0, width = 100, height = 25)

        # Create selection button
        pick_enemy_button = tk.Button(pick_enemy_frame, text="Select")
        pick_enemy_button.place(x=50, y=25, width = 100, height = 30)

        # Create back button. When clicked, it destroys the frame and re-activates the action buttons
        back_button = tk.Button(pick_enemy_frame, text="Back", command=lambda: [pick_enemy_frame.destroy(), action_buttons_activated()])
        back_button.place(x=150, y=25, width = 100, height = 30)


    def select_one_from_allies(self, allies: List[str], action_buttons_inactivated, action_buttons_activated):
        # Deactivate the action buttons
        action_buttons_inactivated()

        # Create selection frame
        pick_allies_frame = tk.Frame(self.window_manager.window)
        pick_allies_frame.place(x=900, y=400, width = 300, height = 200)

        # Create selection combobox
        pick_allies_combobox = ttk.Combobox(pick_allies_frame, values=allies)
        pick_allies_combobox.set("Pick an ally")
        pick_allies_combobox.place(x=100, y=0, width = 100, height = 25)

        # Create selection button
        pick_allies_button = tk.Button(pick_allies_frame, text="Select")
        pick_allies_button.place(x=50, y=25, width = 100, height = 30)

        # Create back button. When clicked, it destroys the frame and re-activates the action buttons
        back_button = tk.Button(pick_allies_frame, text="Back", command=lambda: [pick_allies_frame.destroy(), action_buttons_activated()])
        back_button.place(x=150, y=25, width = 100, height = 30)

    def change_label_font(self, label, font):
        label.configure(font=(font, 30)) # (font)

class CombatScreen(Subject):
    def __init__(self, window, both_parties_tables, both_parties_name_lists):
        super().__init__()
        self.window = window
        self.both_parties_tables = both_parties_tables
        self.both_parties_name_lists = both_parties_name_lists

        # Create player frame
        player_frame = tk.Frame(self.window)
        player_frame.place(x=0, y=10, width = 600, height = 300)

        # Create player scrollbar
        player_scrollbar = tk.Scrollbar(player_frame, orient = tk.HORIZONTAL)
        player_scrollbar.pack(side=tk.BOTTOM, fill = tk.X)

        # Create player table
        self.player_table = tk.Text(player_frame, wrap=tk.NONE, xscrollcommand=player_scrollbar.set)
        self.player_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.player_table.insert(tk.END, both_parties_tables[0])
        self.player_table.tag_add("green", "1.0", "1.end")
        self.player_table.tag_config("green", foreground="green")

        # Configure the player scrollbar
        player_scrollbar.config(command=self.player_table.xview)

        # Create enemy frame
        enemy_frame = tk.Frame(self.window)
        enemy_frame.place(x=600, y=10, width = 600, height = 300)

        # Create enemy scrollbar
        enemy_scrollbar = tk.Scrollbar(enemy_frame, orient = tk.HORIZONTAL)
        enemy_scrollbar.pack(side=tk.BOTTOM, fill = tk.X)

        # Create enemy table
        self.enemy_table = tk.Text(enemy_frame, wrap=tk.NONE, xscrollcommand=enemy_scrollbar.set)
        self.enemy_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.enemy_table.insert(tk.END, both_parties_tables[1])
        self.enemy_table.tag_add("red", "1.0", "1.end")
        self.enemy_table.tag_config("red", foreground="red")

        # Configure the enemy scrollbar
        enemy_scrollbar.config(command=self.enemy_table.xview)

        # Create combat log frame
        combat_log_frame = tk.Frame(self.window)
        combat_log_frame.place(x=0, y=310, width = 800, height = 200)

        # Create combat log title on left
        combat_log_title = tk.Label(combat_log_frame, text="Combat log", font=("Arial", 12, "bold"), justify="left")
        combat_log_title.pack(padx=2, anchor="w")

        # Create combat log scrollbar
        combat_log_scrollbar = tk.Scrollbar(combat_log_frame, orient = tk.VERTICAL)
        combat_log_scrollbar.pack(side=tk.RIGHT, fill = tk.Y)

        # Create combat log textbox
        self.combat_log = tk.Text(combat_log_frame, wrap=tk.NONE, yscrollcommand=combat_log_scrollbar.set, xscrollcommand=combat_log_scrollbar.set)
        self.combat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the combat log scrollbar
        combat_log_scrollbar.config(command=self.combat_log.yview)

        # Create action buttons.
        # Attack button. Allows the player to select an enemy to attack. Sends the activation and inactivation functions to the select_one_from_enemies function
        attack_button = tk.Button(self.window, text="Attack", command=lambda: (self.select_one_from_enemies(self.both_parties_name_lists[1]), self.action_buttons_inactivated()))
        attack_button.place(x=800, y=320, width = 100, height = 25)

        # Heal button. Allows the player to select an ally to heal. Sends the activation and inactivation functions to the select_one_from_allies function
        heal_button = tk.Button(self.window, text="Heal", command=lambda: (self.select_one_from_allies(self.both_parties_name_lists[0]), self.action_buttons_inactivated()))
        heal_button.place(x=800, y=345, width = 100, height = 25)

        # Inventory button
        inventory_button = tk.Button(self.window, text="Inventory", command=lambda: self.notify_observers(GUINotification.PLAYER_INVENTORY))
        inventory_button.place(x=800, y=370, width = 100, height = 25)

        self.action_buttons = [attack_button, heal_button, inventory_button]

    def action_buttons_activated(self):
        for button in self.action_buttons:
            button.config(state = tk.NORMAL)

    def action_buttons_inactivated(self):
        for button in self.action_buttons:
            button.config(state = tk.DISABLED)

    def select_one_from_enemies(self, enemies: List[str]):
        # Create selection frame
        pick_enemy_frame = tk.Frame(self.window)
        pick_enemy_frame.place(x=900, y=400, width = 300, height = 200)

        # Create selection combobox
        pick_enemy_combobox = ttk.Combobox(pick_enemy_frame, values=enemies)
        pick_enemy_combobox.set("Pick an enemy")
        pick_enemy_combobox.place(x=100, y=0, width = 100, height = 25)

        # Create selection button
        pick_enemy_button = tk.Button(pick_enemy_frame, text="Select")
        pick_enemy_button.place(x=50, y=25, width = 100, height = 30)

        # Create back button. When clicked, it destroys the frame and re-activates the action buttons
        back_button = tk.Button(pick_enemy_frame, text="Back", command=lambda: [pick_enemy_frame.destroy(), self.action_buttons_activated()])
        back_button.place(x=150, y=25, width = 100, height = 30)

    def select_one_from_allies(self, allies: List[str]):
        # Create selection frame
        pick_allies_frame = tk.Frame(self.window)
        pick_allies_frame.place(x=900, y=400, width = 300, height = 200)

        # Create selection combobox
        pick_allies_combobox = ttk.Combobox(pick_allies_frame, values=allies)
        pick_allies_combobox.set("Pick an ally")
        pick_allies_combobox.place(x=100, y=0, width = 100, height = 25)

        # Create selection button
        pick_allies_button = tk.Button(pick_allies_frame, text="Select")
        pick_allies_button.place(x=50, y=25, width = 100, height = 30)

        # Create back button. When clicked, it destroys the frame and re-activates the action buttons
        back_button = tk.Button(pick_allies_frame, text="Back", command=lambda: [pick_allies_frame.destroy(), self.action_buttons_activated()])
        back_button.place(x=150, y=25, width = 100, height = 30)


class WindowManager:
    def __init__(self):
        self.window = None

    def start_window(self):
        self.window = tk.Tk()
        self.window.title("RPG")
        self.window.geometry("1200x550")
        self.window.resizable(False, False)

    def update_window(self, new_title):
        self.window.title(new_title)

    def clear_frame(self):
        for widget in self.window.winfo_children():
            widget.destroy()
