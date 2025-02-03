class Item:
    def __init__(self, name, description, stack_size=1):
        self.name = name
        self.description = description
        self.stack_size = stack_size

#     def __repr__(self):

class Potion(Item):
    def __init__(self, name, description, stack_size=1):
        super().__init__(name, description, stack_size)

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
            unit.hp += heal_amount
        print(f"{unit.name} heals for {self.heal_amount}, back to {unit.hp}!")


class InstantPoisonPotion(Potion):
    def __init__(self, name, description, damage_amount):
        super().__init__(name, description)
        self.damage_amount = damage_amount

#     def __eq__(self, other):
#         if not isinstance(other, Potion):
#             return False

smallHealthPotion = HealthPotion("Small Health Potion", "Restores 5 HP", 3, 5)
largeHealthPotion = HealthPotion("Large Health Potion", "Restores 10 HP", 1, 10)