import threading
import music
import unit
import functools
from enum import Enum
from colorama import init, Fore
from item import smallHealthPotion, largeHealthPotion, smallInstantHarmingPotion, HealthPotion, InstantPoisonPotion, \
    ItemUse
from status_effect import testingStatusEffect, testingStatusEffect2, hardenEffect, resistEffect, accuracyEffect, speedEffect, luckyEffect
from util import Option, OptionPicker, pick_random_from

INVALID_SELECTION = "Invalid Selection!"
class FightOutcome(Enum):
    PLAYER_VICTORY = 0
    ENEMY_VICTORY = 1
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
        while True:
            turn_order = self.get_turn_order()
            for unit_turn in turn_order:
                if unit_turn.hp == 0:
                    # Skip dead units
                    continue
                self.handle_unit_turn(unit_turn)
                if self.outcome is not None:
                    return self.outcome

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
        print(selected_enemy_unit)
        self.enemy_turn(selected_enemy_unit)
        if len(self.player_party.units) == 0:
            print("Player Party has been defeated!")
            self.outcome = FightOutcome.ENEMY_VICTORY

    # Give the options available to the player. This is where player decision is made
    def player_turn(self, selected_player_unit):
        print(selected_player_unit)
        player_turn_text = "What do you want to do?\n1. Attack\n2. Check Inventory\n3. Use Item\n"
        has_used_item = False
        player_party = selected_player_unit.observers[0]
        # If there are still enemy units, loop
        while has_used_item == False and len(self.enemy_party.units) > 0:
            selection = input(player_turn_text)
            if selection == "1":
                self.player_attack(selected_player_unit)
                break
            elif selection == "2":
                player_party.read_inventory()
            elif selection == "3" and has_used_item == False:
                self.handle_item_use(selected_player_unit, player_party)
                has_used_item = True
                player_turn_text = player_turn_text.replace("3. Use Item\n", Fore.LIGHTBLACK_EX + "3. Use Item\n" + Fore.RESET)
            else:
                print(INVALID_SELECTION)

    def handle_item_use(self, player_unit, player_party):
        item_name = player_party.get_item()
        item = player_party.inventory[item_name]
        if item.item_use == ItemUse.SELF_UNIT:
            self.use_item_on_self(player_unit, item)
        elif item.item_use == ItemUse.ENEMY_UNIT:
            self.use_item_on_enemy_unit(player_unit, item)
        else:
            raise ValueError("Unsupported item use: " + str(item.item_use))
        player_party.remove_inventory(item_name)

    def use_item_on_party_member(self, player_unit, selected_item):
        print("in use_item_on_party_member")

    def use_item_on_self(self, player_unit, selected_item):
        item_use(player_unit, selected_item)

    def use_item_on_enemy_unit(self, player_unit, selected_item):
        options = []
        for possible_unit in self.enemy_party.units:
            options.append(Option(possible_unit.name, functools.partial(item_use, player_unit, selected_item, possible_unit)))
        item_option_picker = OptionPicker("Which enemy to use the item on?", options, INVALID_SELECTION )
        item_option_picker.pick()

    def player_attack(self, selected_player_unit):
        options = []
        for enemy_unit in self.enemy_party.units:
            options.append(Option(enemy_unit.name, functools.partial(selected_player_unit.attack, enemy_unit)))
        enemy_option_picker = OptionPicker("Which enemy to attack?", options, INVALID_SELECTION )
        enemy_option_picker.pick()

    # Enemy AI. For now, just attacks
    def enemy_turn(self, selected_enemy_unit):
        selected_enemy_unit.attack(pick_random_from(self.player_party.units))


# Initialises the player and the enemy
def initialise_player_and_enemy(name):
    player_unit = unit.Unit(name = name, player = True, physical = True, max_hp = 10, strength = 6, defense = 2, resistance = 0, dexterity = 30, speed = 3, luck = 30)
    licht_unit = unit.Unit("Licht", True, False, 10, 4, 0, 3, 10, 6, 5)
    player_party = unit.Party(0, 0)
    player_party.add_unit(player_unit)
    player_party.add_unit(licht_unit)
    enemy_unit = unit.Unit("Enemy 1", False, False, 10, 4, 3, 0, 10, 5, 5)
    enemy_unit_2 = unit.Unit("Enemy 2", False, False, 10, 4, 3, 0, 10, 5, 5)
    enemy_party = unit.Party( 0, 0)
    enemy_party.add_unit(enemy_unit)
    enemy_party.add_unit(enemy_unit_2)
    return player_party, enemy_party

# Main gameplay loop
def main():
    init()
    soundtrack_mute = True
    stop_event = music.initialise_music()
    music.start_music_thread(stop_event, "music/cats.wav", soundtrack_mute)
    name = input("What's your name? \n")
    music.stop_current_music_thread(stop_event)
    stop_event = threading.Event()
    music.start_music_thread(stop_event, "music/riff.wav", soundtrack_mute)
    player_party, enemy_party = initialise_player_and_enemy(name)
    player_party.add_inventory(smallHealthPotion)
    player_party.add_inventory(largeHealthPotion)
    player_party.add_inventory(smallInstantHarmingPotion)
    player_party.units[0].add_status_effect(luckyEffect)

    combat = CombatManager(player_party, enemy_party)
    combat.start_battle()

    music.stop_current_music_thread(stop_event)
    if combat.outcome == FightOutcome.PLAYER_VICTORY:
        music.stop_and_play_music('music/victory.wav', soundtrack_mute)
        input("Congatulations\n")
    else:
        music.stop_and_play_music('music/game over.wav', soundtrack_mute)
        input("Sorry! Try again!\n")
    

if __name__ == '__main__':
    main()