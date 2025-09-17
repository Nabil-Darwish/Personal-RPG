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
        self.turn_order_list = []
        self.current_unit = None
        self.current_turn = 0

    def partial_log_update_function(self):
        return functools.partial(self.notify_observers, rpg_enum.CombatNotification.COMBAT_GRID_LOG_TEXT_UPDATE)

    def start_battle(self):
        # This is how the start of each battle is done. Call on the initial stats screen and send the party stats
        self.notify_observers(rpg_enum.CombatNotification.INITIAL_STATS_SCREEN, self.show_party_stats())

    def show_party_stats(self):
        # How the party stats are displayed
        return "ALLIES: \n" + self.player_party.show_units(), "ENEMIES: \n" + self.enemy_party.show_units()

    def show_party_tables(self):
        # This is called when the GUI needs the current stat tables after the initial party stats
        ally_table = self.get_ally_table()
        enemy_table = self.get_enemy_table()

        # Send the information back to the GUI
        self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_SCREEN, (ally_table, enemy_table), (self.player_party.get_unit_names, self.enemy_party.get_unit_names))

    def get_ally_table(self):
        ally_table = "ALLIES: \n"
        ally_table += tabulate(self.player_party.get_units_stats_list_dict(), headers="keys", tablefmt="grid") + "\n" + self.player_party.get_status_effects_units()
        return ally_table

    def get_enemy_table(self):
        enemy_table = "ENEMIES: \n"
        enemy_table += tabulate(self.enemy_party.get_units_stats_list_dict(), headers="keys", tablefmt="grid") + "\n" + self.enemy_party.get_status_effects_units()
        return enemy_table

    # Get the new turn order
    def get_new_turn_order(self):
        self.current_turn += 1
        self.turn_order_list = sorted(self.player_party.units + self.enemy_party.units, key=lambda current_unit: current_unit.get_temp_stat("speed"), reverse=True)
        turn_text = "TURN " + str(self.current_turn) + "\n"
        self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_NEW_TURN_ORDER, turn_text)

    def get_next_turn_unit(self):
        self.current_unit = self.turn_order_list.pop(0)
        self.handle_unit_turn(self.current_unit)

    # If the unit is a player unit, hand control to the player. Otherwise, hand control to the AI
    def handle_unit_turn(self, unit: unit.Unit):
        if unit.player:
            self.handle_player_turn(unit)
        else:
            self.handle_enemy_turn(unit)

    # This is how the player's turn is handled
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

    # Give the options available to the player. This is where player decision is made
    def player_turn(self, selected_unit: unit.Unit):
        self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_PLAYER_TURN, f"{selected_unit.name}'s turn! \n", selected_unit.name)

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

    def handle_turn_order(self):
        if len(self.turn_order_list) == 0:
            self.get_new_turn_order()
        else:
            self.get_next_turn_unit()

    def player_attack(self, selected_enemy_unit_name: str):
        self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_LOG_TEXT_UPDATE, f"{self.current_unit.name} attacks {selected_enemy_unit_name}!\n")
        try:
            selected_unit = self.enemy_party.get_unit(selected_enemy_unit_name)
            # partial_enemy_table_update_function = functools.partial(self.notify_observers, rpg_enum.CombatNotification.COMBAT_GRID_ENEMY_TABLE_UPDATE)
            self.current_unit.attack(selected_unit, self.partial_log_update_function())
            self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_ENEMY_TABLE_UPDATE, self.get_enemy_table())
        except KeyError:
            print("Invalid Selection")
            return

        if len(self.turn_order_list) == 0:
            self.get_new_turn_order()
        else:
            self.get_next_turn_unit()

    def player_heal(self, selected_target_name: str, is_player: bool):
        self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_LOG_TEXT_UPDATE, f"{self.current_unit.name} heals {selected_target_name}!\n")

    # Enemy AI. For now, just attacks
    def enemy_turn(self, selected_enemy_unit):
        self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_ENEMY_TURN, f"{selected_enemy_unit.name}'s turn!\n")
        selected_enemy_unit.attack(random.choice(self.player_party.units), self.partial_log_update_function())
        self.notify_observers(rpg_enum.CombatNotification.COMBAT_GRID_PLAYER_TABLE_UPDATE, self.get_ally_table())

        self.get_next_turn_unit()
