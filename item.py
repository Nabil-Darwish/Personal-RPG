import util
from rpg_enum import Enum

# This defines how an item is used (could be changed later)
class ItemUse(Enum):
    # item affects all in own party
    SELF_PARTY = 1
    # item affects one unit in own party
    UNIT_IN_SELF_PARTY = 2
    # item affects selected unit
    SELF_UNIT = 3
    # item affects all in enemy party
    ENEMY_PARTY = 4
    # item affects one unit in enemy party
    ENEMY_UNIT = 5
    # item affects all units
    ALL_UNITS = 6
    # item can be used on any of the parties
    BOTH_PARTIES = 7


# This defines the item superclass
class Item:
    def __init__(self, name, description, item_use, stack_size=1):
        self.name = name
        self.description = description
        self.item_use = item_use
        self.stack_size = stack_size

#     def __repr__(self):

# Defines the Potion superclass
class Potion(Item):
    def __init__(self, name, description, item_use, stack_size=1):
        super().__init__(name, description, item_use, stack_size)

# Defines the HealthPotion subclass
class HealthPotion(Potion):
    def __init__(self, name, description, stack_size, heal_amount):
        super().__init__(name, description, ItemUse.SELF_UNIT, stack_size)
        self.heal_amount = heal_amount

    def __repr__(self):
        return f"{self.name}: {self.description}, ({self.stack_size})\n"

    def heal(self, unit):
        print(f"{unit.name} used {self.name}!")
        if unit.hp > (unit.max_hp - self.heal_amount):
            unit.hp = unit.max_hp
        else:
            unit.hp += self.heal_amount
        print(f"{unit.name} heals for {self.heal_amount}, back to {unit.hp}!")

# Defines poison potions that work instantly
class InstantPoisonPotion(Potion):
    def __init__(self, name, description, stack_size, damage_amount):
        super().__init__(name, description, ItemUse.ENEMY_UNIT ,stack_size)
        self.damage_amount = damage_amount

    def __repr__(self):
        return f"InstantPoisonPotion({self.name}, {self.description}, {self.stack_size}, {self.damage_amount})"

    def __str__(self):
        return f"{self.name}: {self.description}, ({self.stack_size} bottles) ({self.damage_amount} damage)"

    def poison(self, unit, enemy_unit):
        print(f"{unit.name} used {self.name} on {enemy_unit.name}!")
        enemy_unit.hp -= self.damage_amount
        enemy_unit.hp = util.not_less_zero(enemy_unit.hp)
        print(f"{unit.name} damages {enemy_unit.name} for {self.damage_amount}, with {enemy_unit.hp} HP left!\n")
        if enemy_unit.hp == 0:
            print(f"{enemy_unit.name} is dead!\n")
            enemy_unit.notify_observers()


#     def __eq__(self, other):
#         if not isinstance(other, Potion):
#             return False

smallHealthPotion = HealthPotion("Small Health Potion", "Restores 5 HP", 3, 5)
largeHealthPotion = HealthPotion("Large Health Potion", "Restores 10 HP", 1, 10)
smallInstantHarmingPotion = InstantPoisonPotion("Small Instant Poison Potion", "Inflicts 5 damage", 3, 5)