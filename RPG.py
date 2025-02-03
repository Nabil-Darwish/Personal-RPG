import random
import sys
import threading
import music
from item import HealthPotion, smallHealthPotion, largeHealthPotion

BASE_CHANCE_HIT = 50

class Unit:
    def __init__(self, name, player, physical, max_hp, strength, defense, resistance, dexterity, speed, luck, hp = None):
        self.name = name
        self.player = player
        self.physical = physical
        self.max_hp = max_hp
        self._hp = max_hp if hp is None else min(max_hp, hp)
        self.strength = strength
        self.defense = defense
        self.resistance = resistance
        self.dexterity = dexterity
        self.speed = speed
        self.luck = luck
        self.inventory = []

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))

    def __str__(self):
        return f"""Name: {self.name}
PHYS: {self.physical}
HP  : {self.hp}/{self.max_hp}   
STR : {self.strength} 
DEF : {self.defense}
RES : {self.resistance}
DEX : {self.dexterity}
SPD : {self.speed} 
LCK : {self.luck}\n"""

    def add_item(self, item):
        self.inventory.append(item)

    def read_inventory(self):
        if len(self.inventory) == 0:
            print("Inventory is empty!\n")
        for item in self.inventory:
            print(item)

    def use_inventory(self):
        for i in range(len(self.inventory)):
            print(f"{i + 1}. {self.inventory[i].name}")
        selection = input("What do you want to use?\n")
        self.use(self.inventory[(int(selection) - 1)])
        self.inventory.pop(int(selection) - 1)

    def use(self, item):
        if isinstance(item, HealthPotion):
            self.heal(item.heal_amount)
    
    def attack(self, enemy):
        input(f"\n{self.name} attacks {enemy.name}!")
        hitChance = BASE_CHANCE_HIT + self.dexterity
        randomVariable = random.randint(0, 100)
        if randomVariable < hitChance:
            randomVariable = random.randint(0, 100)
            if self.physical:
                damage = self.strength - enemy.defense
            else:
                damage = self.strength - enemy.resistance
            damage = not_less_zero(damage)
            if randomVariable < self.luck:                  # Critical Hit
                damage = damage * 2
                print("Critical Hit!")
            print(f"{self.name} hits {enemy.name} for {damage} ({hitChance})!\n")
            enemy.hp -= damage
            enemy.hp = not_less_zero(enemy.hp)
            print(enemy)
        else:
            print("Miss!\n")

    def heal(self, heal_amount):
        input("Healing!\n")
        if self.hp > (self.max_hp - heal_amount):
            self.hp = self.max_hp
        else:
            self.hp += heal_amount
        print(f"{self.name} heals for {heal_amount}, back to {self.hp}!")

#class Party:
#    def __init__(self, units):
#        self.units = units
#        self.gold = 0
#

class CombatManager:
    def __init__(self, player_unit, enemy_unit):
        self.player_unit = player_unit
        self.enemy_unit = enemy_unit

    def start_battle(self):
        while self.player_unit.hp > 0 and self.enemy_unit.hp > 0:
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

    def enemy_turn(self):
        self.enemy_unit.attack(self.player_unit)

def not_less_zero(variable):
    return max(0, variable)

def pick_random_from(l):
    randomVariable = random.randint(0, len(l))
    return l[randomVariable]

def initialise_player_and_enemy(name):
    playerUnit = Unit(name = name, player = True, physical = True, max_hp = 10, strength = 6, defense = 2, resistance = 8, dexterity = 30, speed = 3, luck = 30)
    enemyUnit = Unit("Enemy", False, True, 10, 6, 3, 0, 10, 5, 5)
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