import sys
import threading
import music
import unit
from item import HealthPotion, smallHealthPotion, largeHealthPotion

class CombatManager:
    def __init__(self, player_unit, enemy_unit):
        self.player_unit = player_unit
        self.enemy_unit = enemy_unit

    def start_battle(self):
        while True:
            turnOrder = sorted([self.player_unit, self.enemy_unit], key = lambda unit: unit.speed, reverse = True)
            for unit in turnOrder:
                if unit.player:
                    self.player_turn()
                    if self.enemy_unit.hp <= 0:
                        print("Enemy Defeated!")
                        return 0
                else:
                    self.enemy_turn()
                    if self.player_unit.hp <= 0:
                        print(f"{self.player_unit.name} has been defeated!")
                        return 1

    def player_turn(self):
        while True:
            selection = input("What do you want to do?\n1. Attack\n2. Check Inventory\n3. Use Item\n")
            if selection == "1":
                self.player_unit.attack(self.enemy_unit)
                break
            elif selection == "2":
                self.player_unit.read_inventory()
            elif selection == "3":
                self.player_unit.use_inventory()
            else:
                print("Invalid Selection!")

    def enemy_turn(self):
        self.enemy_unit.attack(self.player_unit)

def pick_random_from(l):
    randomVariable = random.randint(0, len(l))
    return l[randomVariable]

def initialise_player_and_enemy(name):
    playerUnit = unit.Unit(name = name, player = True, physical = True, max_hp = 10, strength = 6, defense = 2, resistance = 8, dexterity = 30, speed = 3, luck = 30)
    enemyUnit = unit.Unit("Enemy", False, True, 10, 6, 3, 0, 10, 5, 5)
    return playerUnit, enemyUnit

def main():
    stop_event = music.initialise_music()
    music.start_music_thread(stop_event, "music/cats.wav")
    name = input("What's your name? \n")
    music.stop_current_music_thread(stop_event)
    stop_event = threading.Event()
    music.start_music_thread(stop_event, "music/riff.wav")
    playerUnit, enemyUnit = initialise_player_and_enemy(name)
    playerUnit.add_item(smallHealthPotion)
    playerUnit.add_item(largeHealthPotion)

    combat = CombatManager(playerUnit, enemyUnit)
    outcome = combat.start_battle()

    music.stop_current_music_thread(stop_event)
    if outcome == 0:
        music.stop_and_play_music('music/victory.wav')
        input("Congatulations\n")
    else:
        music.stop_and_play_music('music/game over.wav')
        input("Sorry! Try again!\n")
    

if __name__ == '__main__':
    main()