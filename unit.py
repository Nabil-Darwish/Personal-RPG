import random
import util
from item import HealthPotion, InstantPoisonPotion

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
        self.inventory = {}

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

    # If there are no items of the type, then add entry to dictionary. Otherwise, add stack size
    def add_item(self, item):
        if item.name in self.inventory:
            self.inventory[item.name].stack_size += item.stack_size
        else:
            self.inventory[item.name] = item

    def read_inventory(self):
        if len(self.inventory) == 0:
            print("Inventory is empty!\n")
        for key in self.inventory:
            print(self.inventory[key])

    def use_inventory(self):
        for index, (key, value) in enumerate(self.inventory.items()):
            print(f"{index + 1}. {self.inventory[key]}")

        while True:
            choice = input("What do you want to use?\n")
            if choice.isdigit() and 1 <= int(choice) <= len(self.inventory):
                choice = int(choice) - 1
                break
            else:
                print("Please enter a valid number!\n")

        item_name = list(self.inventory.keys())[choice]
        item = self.inventory[item_name]

        self.use(item)
        self.remove_item(item_name)

    def remove_item(self, item_name):
        if self.inventory[item_name].stack_size > 1:
            self.inventory[item_name].stack_size -= 1
        else:
            self.inventory.pop(item_name)

    def use(self, item):
        if isinstance(item, HealthPotion):
            HealthPotion.heal(item, self)
        elif isinstance(item, InstantPoisonPotion):
            InstantPoisonPotion.poison(item, self, enemy)

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
            damage = util.not_less_zero(damage)
            if randomVariable < self.luck:                  # Critical Hit
                damage = damage * 2
                print("Critical Hit!")
            print(f"{self.name} hits {enemy.name} for {damage} ({hitChance})!\n")
            enemy.hp -= damage
            enemy.hp = util.not_less_zero(enemy.hp)
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