import util

# This defines the item superclass
class Item:
    def __init__(self, name, description, stack_size=1):
        self.name = name
        self.description = description
        self.stack_size = stack_size

#     def __repr__(self):

# Defines the Potion superclass
class Potion(Item):
    def __init__(self, name, description, stack_size=1):
        super().__init__(name, description, stack_size)

# Defines the HealthPotion subclass
class HealthPotion(Potion):
    def __init__(self, name, description, stack_size, heal_amount):
        super().__init__(name, description, stack_size)
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
        super().__init__(name, description, stack_size)
        self.damage_amount = damage_amount

    def __repr__(self):
        return f"{self.name}: {self.description}, ({self.stack_size})\n"

    def poison(self, unit, enemy_unit):
        print(f"{unit.name} used {self.name} on {enemy_unit.name}!")
        enemy_unit.hp -= self.damage_amount
        enemy_unit.hp = util.not_less_zero(enemy_unit.hp)
        print(f"{unit.name} damages {enemy_unit.name} for {self.damage_amount}, back to {enemy_unit.hp}!\n")
        print(enemy_unit)


#     def __eq__(self, other):
#         if not isinstance(other, Potion):
#             return False

smallHealthPotion = HealthPotion("Small Health Potion", "Restores 5 HP", 3, 5)
largeHealthPotion = HealthPotion("Large Health Potion", "Restores 10 HP", 1, 10)
smallInstantHarmingPotion = InstantPoisonPotion("Small Instant Poison Potion", "Inflicts 5 damage", 3, 5)