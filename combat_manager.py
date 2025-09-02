import random
import functools
from colorama import Fore
from tabulate import tabulate
import rpg_enum
import unit
from item import HealthPotion, InstantPoisonPotion, ItemUse, Item
from util import Option, OptionPicker, Subject
from rpg_enum import FightOutcome

INVALID_SELECTION = "Invalid Selection!"

# Handles the use of items
def item_use(player_unit, item, enemy_unit = None):
    if isinstance(item, HealthPotion):
        HealthPotion.heal(item, player_unit)
    elif isinstance(item, InstantPoisonPotion):
        InstantPoisonPotion.poison(item, player_unit, enemy_unit)
    else:
        raise ValueError("Unsupported item type: " + str(type(item)))

# This is the combat manager that handles combat encounters
class CombatManager(Subject):
    def __init__(self, player_party: unit.Party, enemy_party: unit.Party):
        super().__init__()
        self.player_party = player_party
        self.enemy_party = enemy_party
        self.outcome = None

    # This is how the start of each turn is handled
    # def start_battle(self):
    #     os.system('cls')
    #     self.show_party_stats()
    #     input("Press enter to proceed to turn 1.")
    #     while True:
    #         os.system('cls')
    #         self.show_party_tables()
    #         turn_order = self.get_turn_order()
    #         for unit_turn in turn_order:
    #             if unit_turn.hp == 0:
    #                 # Skip dead units
    #                 continue
    #             self.handle_unit_turn(unit_turn)
    #             if self.outcome is not None:
    #                 return self.outcome
    #         input("Press enter to proceed to next turn.")

    def start_battle(self):
        # This is how the start of each battle is done. Call on the initial stats screen and send the party stats
        self.notify_observers(rpg_enum.CombatNotification.INITIAL_STATS_SCREEN, self.show_party_stats())

    def show_party_stats(self):
        # How the party stats are displayed
        return "ALLIES: \n" + self.player_party.show_units(), "ENEMIES: \n" + self.enemy_party.show_units()

    def show_party_tables(self):
        # This is called when the GUI needs the current stat tables
        ally_table = "ALLIES: \n"
        ally_table += tabulate(self.player_party.get_units_stats_list_dict(), headers="keys", tablefmt="grid") + "\n" + self.player_party.get_status_effects_units()
        enemy_table = "ENEMIES: \n"
        enemy_table += tabulate(self.enemy_party.get_units_stats_list_dict(), headers="keys", tablefmt="grid") + "\n" + self.enemy_party.get_status_effects_units()

        # Send the information back to the GUI
        self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_SCREEN, (ally_table, enemy_table), (self.player_party.get_unit_names, self.enemy_party.get_unit_names))


    # DEPRECATED: This is how the turn order is decided. Gives list of all units sorted by speed. Higher speed first
    def get_turn_order(self):
        return sorted(self.player_party.units + self.enemy_party.units, key=lambda unit: unit.get_temp_stat("speed"), reverse=True)

    # DEPRECATED: If the unit is a player unit, hand control to the player. Otherwise, hand control to the AI
    def handle_unit_turn(self, unit: unit.Unit):
        if unit.player:
            self.handle_player_turn(unit)
        else:
            self.handle_enemy_turn(unit)

    # DEPRECATED: This is how the player's turn is handled
    def handle_player_turn(self, selected_player_unit: unit.Unit):
        self.player_turn(selected_player_unit)
        selected_player_unit.decrease_status_effect_durations()
        if len(self.enemy_party.units) == 0:
            print("Enemies Defeated!")
            self.outcome = FightOutcome.PLAYER_VICTORY

    # DEPRECATED: This is how the enemy's turn is handled
    def handle_enemy_turn(self, selected_enemy_unit: unit.Unit):
        self.enemy_turn(selected_enemy_unit)
        if len(self.player_party.units) == 0:
            print("Player Party has been defeated!")
            self.outcome = FightOutcome.ENEMY_VICTORY

    # DEPRECATED: Give the options available to the player. This is where player decision is made
    def player_turn(self, selected_unit: unit.Unit):
        print(f"{selected_unit.name}'s turn!")
        turn_options = "What do you want to do?\n1. Attack\n2. Check Inventory\n3. Use Item\n"
        has_used_item = False
        player_party = selected_unit.observers[0]
        # If there are still enemy units, loop
        while has_used_item == False and len(self.enemy_party.units) > 0:
            selection = input(turn_options)
            if selection == "1":
                if not self.player_attack(selected_unit):
                    break
            elif selection == "2":
                player_party.read_inventory()
            elif selection == "3" and has_used_item == False:
                if not self.handle_item_use(selected_unit, player_party):
                    has_used_item = True
                    turn_options = turn_options.replace("3. Use Item\n", Fore.LIGHTBLACK_EX + "3. Use Item\n" + Fore.RESET)
            else:
                print(INVALID_SELECTION)

    # DEPRECATED
    def handle_item_use(self, player_unit: unit.Unit, player_party: unit.Party):
        item_name = player_party.get_item()
        item = player_party.inventory[item_name]
        if item.item_use == ItemUse.SELF_UNIT:
            has_backed_out = self.use_item_on_self(player_unit, item)
        elif item.item_use == ItemUse.ENEMY_UNIT:
            has_backed_out = self.use_item_on_enemy_unit(player_unit, item)
        else:
            raise ValueError("Unsupported item use: " + str(item.item_use))
        player_party.remove_inventory(item_name)
        return has_backed_out

    # def use_item_on_party_member(self, player_unit, selected_item):
    #     print("in use_item_on_party_member")

    # DEPRECATED
    def use_item_on_self(self, player_unit: unit.Unit, selected_item: Item):
        item_use(player_unit, selected_item)
        return False

    # DEPRECATED
    def use_item_on_enemy_unit(self, player_unit: unit.Unit, selected_item: Item):
        options = []
        for possible_unit in self.enemy_party.units:
            options.append(Option(possible_unit.name, functools.partial(item_use, player_unit, selected_item, possible_unit)))
        item_option_picker = OptionPicker("Which enemy to use the item on?", options, INVALID_SELECTION, True)
        return item_option_picker.pick()

    # DEPRECATED
    def player_attack(self, selected_player_unit: unit.Unit, selected_enemy_unit: unit.Unit = None):
        options = []
        for enemy_unit in self.enemy_party.units:
            options.append(Option(enemy_unit.name, functools.partial(selected_player_unit.attack, enemy_unit)))
        enemy_option_picker = OptionPicker("Which enemy to attack?", options, INVALID_SELECTION, True)
        return enemy_option_picker.pick()

    # DISCONNECTED: Enemy AI. For now, just attacks
    def enemy_turn(self, selected_enemy_unit):
        selected_enemy_unit.attack(random.choice(self.player_party.units))
