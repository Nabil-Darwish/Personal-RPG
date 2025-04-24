import random
import functools
import os
from colorama import Fore
from tabulate import tabulate
from item import HealthPotion, InstantPoisonPotion, ItemUse
from util import Option, OptionPicker
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
class CombatManager:
    def __init__(self, player_party, enemy_party):
        self.player_party = player_party
        self.enemy_party = enemy_party
        self.outcome = None

    # This is how the start of each turn is handled
    def start_battle(self):
        os.system('cls')
        self.show_party_stats()
        input("Press enter to proceed to turn 1.")
        while True:
            os.system('cls')
            self.show_party_tables()
            turn_order = self.get_turn_order()
            for unit_turn in turn_order:
                if unit_turn.hp == 0:
                    # Skip dead units
                    continue
                self.handle_unit_turn(unit_turn)
                if self.outcome is not None:
                    return self.outcome
            input("Press enter to proceed to next turn.")

    def show_party_stats(self):
        print(Fore.GREEN + "ALLIES: \n" + Fore.RESET)
        self.player_party.show_units()
        print(Fore.RED + "ENEMIES: \n" + Fore.RESET)
        self.enemy_party.show_units()

    def show_party_tables(self):
        os.system('cls')
        print(Fore.GREEN + "ALLIES: \n" + Fore.RESET)
        player_table = tabulate(self.player_party.get_units_stats_list_dict(), headers="keys", tablefmt="grid")
        print(player_table)
        print(f"{self.player_party.get_status_effects_units()}")
        print(Fore.RED + "ENEMIES: \n" + Fore.RESET)
        enemy_table = tabulate(self.enemy_party.get_units_stats_list_dict(), headers="keys", tablefmt="grid")
        print(enemy_table)
        print(f"{self.enemy_party.get_status_effects_units()}")


    # This is how the turn order is decided
    def get_turn_order(self):
        return sorted(self.player_party.units + self.enemy_party.units, key=lambda unit: unit.get_temp_stat("speed"), reverse=True)

    # If the unit is a player unit, hand control to the player. Otherwise, hand control to the AI
    def handle_unit_turn(self, unit):
        if unit.player:
            self.handle_player_turn(unit)
        else:
            self.handle_enemy_turn(unit)

    # This is how the player's turn is handled
    def handle_player_turn(self, selected_player_unit):
        self.player_turn(selected_player_unit)
        selected_player_unit.decrease_status_effect_durations()
        if len(self.enemy_party.units) == 0:
            print("Enemies Defeated!")
            self.outcome = FightOutcome.PLAYER_VICTORY

    # This is how the enemy's turn is handled
    def handle_enemy_turn(self, selected_enemy_unit):
        self.enemy_turn(selected_enemy_unit)
        if len(self.player_party.units) == 0:
            print("Player Party has been defeated!")
            self.outcome = FightOutcome.ENEMY_VICTORY

    # Give the options available to the player. This is where player decision is made
    def player_turn(self, selected_unit):
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

    def handle_item_use(self, player_unit, player_party):
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

    def use_item_on_party_member(self, player_unit, selected_item):
        print("in use_item_on_party_member")

    def use_item_on_self(self, player_unit, selected_item):
        item_use(player_unit, selected_item)
        return False

    def use_item_on_enemy_unit(self, player_unit, selected_item):
        options = []
        for possible_unit in self.enemy_party.units:
            options.append(Option(possible_unit.name, functools.partial(item_use, player_unit, selected_item, possible_unit)))
        item_option_picker = OptionPicker("Which enemy to use the item on?", options, INVALID_SELECTION, True)
        return item_option_picker.pick()

    def player_attack(self, selected_player_unit):
        options = []
        for enemy_unit in self.enemy_party.units:
            options.append(Option(enemy_unit.name, functools.partial(selected_player_unit.attack, enemy_unit)))
        enemy_option_picker = OptionPicker("Which enemy to attack?", options, INVALID_SELECTION, True)
        return enemy_option_picker.pick()

    # Enemy AI. For now, just attacks
    def enemy_turn(self, selected_enemy_unit):
        selected_enemy_unit.attack(random.choice(self.player_party.units))