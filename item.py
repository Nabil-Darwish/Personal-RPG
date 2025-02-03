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

class InstantPoisonPotion(Potion):
    def __init__(self, name, description, damage_amount):
        super().__init__(name, description)
        self.damage_amount = damage_amount

#     def __eq__(self, other):
#         if not isinstance(other, Potion):
#             return False

smallHealthPotion = HealthPotion("Small Health Potion", "Restores 5 HP", 3, 5)
largeHealthPotion = HealthPotion("Large Health Potion", "Restores 10 HP", 3, 10)