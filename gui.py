import functools
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
        self.combat_window = None

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

        partial_attack_function = functools.partial(self.notify_observers, GUINotification.PLAYER_ATTACK)
        partial_heal_function = functools.partial(self.notify_observers, GUINotification.PLAYER_HEAL)

        self.combat_window = CombatScreen(self.window_manager.window, both_parties_tables, both_parties_name_lists, [partial_attack_function, partial_heal_function])

        # Send back request to get turn order list
        self.notify_observers(GUINotification.REQUEST_UNIT_TURN_ORDER)

    def new_turn_order_received(self, turn_text: str):
        self.combat_window.add_text_to_combat_log(turn_text)
        self.notify_observers(GUINotification.REQUEST_NEXT_UNIT)

    def player_turn(self, turn_text: str, unit_name: str):
        self.combat_window.action_buttons_activated()
        self.combat_window.active_unit_name = unit_name
        self.add_combat_log_text(turn_text)

    def enemy_turn(self, turn_text: str):
        self.combat_window.action_buttons_inactivated()
        self.add_combat_log_text(turn_text)
        # Enemy turns are handled by the combat manager

    def add_combat_log_text(self, text: str):
        self.combat_window.add_text_to_combat_log(text)

    def update_player_table(self, table_text: str):
        self.combat_window.update_player_table(table_text)

    def update_enemy_table(self, table_text: str):
        self.combat_window.update_enemy_table(table_text)

    def change_label_font(self, label, font):
        label.configure(font=(font, 30)) # (font)

    def send_notification(self, notification: GUINotification, *args):
        self.notify_observers(notification, *args)

class CombatScreen(Subject):
    def __init__(self, window, both_parties_tables, both_parties_name_lists, action_button_function_list = None):
        super().__init__()
        if action_button_function_list is None:
            self.action_button_functions = []
        else:
            self.action_button_functions = action_button_function_list

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
        self.combat_log.insert(tk.END, "Combat start! \n")

        # Configure the combat log scrollbar
        combat_log_scrollbar.config(command=self.combat_log.yview)

        # Create action buttons.
        # Attack button. Allows the player to select an enemy to attack. Sends the activation and inactivation functions to the select_one_from_enemies function

        attack_button = tk.Button(self.window, text="Attack", command=lambda: (self.select_one_from_list("Pick an enemy", self.both_parties_name_lists[1], 900, 400, self.action_button_functions[0]), self.action_buttons_inactivated()))
        attack_button.place(x=800, y=320, width = 100, height = 25)

        # Heal button. Allows the player to select an ally to heal. Sends the activation and inactivation functions to the select_one_from_allies function
        heal_button = tk.Button(self.window, text="Heal", command=lambda: (self.select_one_from_list("Pick an ally", self.both_parties_name_lists[0], 900, 400, self.action_button_functions[1]), self.action_buttons_inactivated()))
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

    def add_text_to_combat_log(self, text: str):
        self.combat_log.insert(tk.END, text)
        self.combat_log.see(tk.END)

    def update_player_table(self, table: str):
        self.player_table.delete("1.0", tk.END)
        self.player_table.insert(tk.END, table)
        self.player_table.tag_add("green", "1.0", "1.end")
        self.player_table.tag_config("green", foreground="green")

    def update_enemy_table(self, table: str):
        self.enemy_table.delete("1.0", tk.END)
        self.enemy_table.insert(tk.END, table)
        self.enemy_table.tag_add("red", "1.0", "1.end")
        self.enemy_table.tag_config("red", foreground="red")

    def select_one_from_list(self, title: str, options: List[str], x: int, y: int, function = None):
        # Create selection frame
        selection_frame = tk.Frame(self.window)
        selection_frame.place(x=x, y=y, width=300, height=200)

        # Create selection combobox
        selection_combobox = ttk.Combobox(selection_frame, values=options)
        selection_combobox.set(title)
        selection_combobox.place(x=100, y=0, width=100, height=25)

        # Create selection button
        select_button = tk.Button(selection_frame, text="Select", command=lambda: [function(selection_combobox.get()), selection_frame.destroy(), self.action_buttons_activated()])
        select_button.place(x=50, y=25, width=100, height=30)

        # Create back button. When clicked, it destroys the frame and re-activates the action buttons
        back_button = tk.Button(selection_frame, text="Back", command=lambda: [selection_frame.destroy(), self.action_buttons_activated()])
        back_button.place(x=150, y=25, width=100, height=30)

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
