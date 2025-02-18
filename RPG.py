import sys
import threading
import music
import unit
from enum import Enum
from colorama import init, Fore
from item import smallHealthPotion, largeHealthPotion, smallInstantHarmingPotion, HealthPotion, InstantPoisonPotion
from unit import testingStatusEffect

class FightOutcome(Enum):
    PLAYER_VICTORY = 0
    ENEMY_VICTORY = 1

class CombatManager:
    def __init__(self, player_unit, enemy_unit):
        self.player_unit = player_unit
        self.enemy_unit = enemy_unit
        self.outcome = None

    def start_battle(self):
        while True:
            turnOrder = self.get_turn_order()
            for unit in turnOrder:
                self.handle_unit_turn(unit)
                if self.outcome is not None:
                    return self.outcome

    def get_turn_order(self):
        return sorted([self.player_unit, self.enemy_unit], key=lambda unit: unit.speed, reverse=True)

    def handle_unit_turn(self, unit):
        if unit.player:
            self.handle_player_turn()
        else:
            self.handle_enemy_turn()

    def handle_player_turn(self):
        self.player_turn()
        self.player_unit.decrease_status_effect_durations()
        if self.enemy_unit.hp <= 0:
            print("Enemy Defeated!")
            self.outcome = FightOutcome.PLAYER_VICTORY

    def handle_enemy_turn(self):
        self.enemy_turn()
        if self.player_unit.hp <= 0:
            print(f"{self.player_unit.name} has been defeated!")
            self.outcome = FightOutcome.ENEMY_VICTORY

    def player_turn(self):
        player_turn_text = "What do you want to do?\n1. Attack\n2. Check Inventory\n3. Use Item\n"
        has_used_item = False
        while True and self.enemy_unit.hp > 0:
            selection = input(player_turn_text)
            if selection == "1":
                self.player_unit.attack(self.enemy_unit)
                break
            elif selection == "2":
                self.player_unit.read_inventory()
            elif selection == "3" and has_used_item == False:
                item_name = self.player_unit.get_item()
                item = self.player_unit.inventory[item_name]
                self.item_use(self.player_unit, self.enemy_unit, item)
                self.player_unit.remove_item(item_name)
                has_used_item = True
                player_turn_text = player_turn_text.replace("3. Use Item\n", Fore.LIGHTBLACK_EX + "3. Use Item\n" + Fore.RESET)
            else:
                print("Invalid Selection!")

    def enemy_turn(self):
        self.enemy_unit.attack(self.player_unit)

    def item_use(self, player_unit, enemy_unit, item):
        if isinstance(item, HealthPotion):
            HealthPotion.heal(item, player_unit)
        elif isinstance(item, InstantPoisonPotion):
            InstantPoisonPotion.poison(item, player_unit, enemy_unit)

def pick_random_from(l):
    randomVariable = random.randint(0, len(l))
    return l[randomVariable]

def initialise_player_and_enemy(name):
    playerUnit = unit.Unit(name = name, player = True, physical = True, max_hp = 10, strength = 6, defense = 2, resistance = 8, dexterity = 30, speed = 3, luck = 30)
    enemyUnit = unit.Unit("Enemy", False, True, 10, 6, 3, 0, 10, 5, 5)
    return playerUnit, enemyUnit

def main():
    init()
    stop_event = music.initialise_music()
    music.start_music_thread(stop_event, "music/cats.wav")
    name = input("What's your name? \n")
    music.stop_current_music_thread(stop_event)
    stop_event = threading.Event()
    music.start_music_thread(stop_event, "music/riff.wav")
    playerUnit, enemyUnit = initialise_player_and_enemy(name)
    playerUnit.add_item(smallHealthPotion)
    playerUnit.add_item(largeHealthPotion)
    playerUnit.add_item(smallInstantHarmingPotion)
    playerUnit.add_status_effect(testingStatusEffect)

    combat = CombatManager(playerUnit, enemyUnit)
    combat.start_battle()

    music.stop_current_music_thread(stop_event)
    if combat.outcome == FightOutcome.PLAYER_VICTORY:
        music.stop_and_play_music('music/victory.wav')
        input("Congatulations\n")
    else:
        music.stop_and_play_music('music/game over.wav')
        input("Sorry! Try again!\n")
    

if __name__ == '__main__':
    main()