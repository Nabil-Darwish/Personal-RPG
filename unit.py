import random
import util
import math
from item import HealthPotion, InstantPoisonPotion

BASE_CHANCE_HIT = 50

# Unit class. A unit is a character that is the main entity in a combat scenasrio
class Unit:
    def __init__(self, name, player, physical, max_hp, strength, defense, resistance, dexterity, speed, luck, hp = None):
        self.name = name
        self.player = player
        self.physical = physical
        self.max_hp = max_hp
        self._hp = max_hp if hp is None else min(max_hp, hp)
        self.stats = {
            "strength": strength,
            "defense": defense,
            "resistance": resistance,
            "dexterity": dexterity,
            "speed": speed,
            "luck": luck
        }
        self.inventory = {}
        self.status_effects = {}
        # First value is the flat increase, second value is the percentage increase
        self.temporary_stats = {
            "strength": {"flat_increase": 0, "percent_increase": 0},
            "defense": {"flat_increase": 0, "percent_increase": 0},
            "resistance": {"flat_increase": 0, "percent_increase": 0},
            "dexterity": {"flat_increase": 0, "percent_increase": 0},
            "speed": {"flat_increase": 0, "percent_increase": 0},
            "luck": {"flat_increase": 0, "percent_increase": 0}
        }

    def __repr__(self):
        return (
            f"Unit(name={self.name}, player={self.player}, physical={self.physical}, max_hp={self.max_hp}, hp={self._hp})\n"
            f"  Stats: {self.stats}\n"
            f"  Inventory: {self.inventory}\n"
            f"  Status Effects: {self.status_effects}\n"
            f"  Temporary Stats: {self.temporary_stats}"
        )

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
STR : {self.stats["strength"]} ({self.get_temp_stat("strength")})
DEF : {self.stats["defense"]} ({self.get_temp_stat("defense")})
RES : {self.stats["resistance"]} ({self.get_temp_stat("resistance")})
DEX : {self.stats["dexterity"]} ({self.get_temp_stat("dexterity")})
SPD : {self.stats["speed"]} ({self.get_temp_stat("speed")})
LCK : {self.stats["luck"]} ({self.get_temp_stat("luck")})

Status Effects:\n""" + (', '.join(map(str, self.status_effects.values())))

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

    def get_item(self):
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

        return item_name

    def remove_item(self, item_name):
        if self.inventory[item_name].stack_size > 1:
            self.inventory[item_name].stack_size -= 1
        else:
            self.inventory.pop(item_name)

    def add_status_effect(self, status_effect):
        # Get the status effect from the list of status effects applied to the unit by name
        self.status_effects[status_effect.name] = status_effect
        for stat, value in {k:v for k, v in status_effect.effects.items() if v != 0}.items():
            if "percent" in stat:
                stat_affected = stat.split('_')[1]
                self.temporary_stats[stat_affected]["percent_increase"] += value
            else:
                self.temporary_stats[stat]["flat_increase"] += value

    # This only occurs if the status effect is popped out of the list
    def delete_temp_stats(self, status_effect):
        #  From the list of stats that are affected by the status effect
        for stat, value in {k:v for k, v in status_effect.effects.items() if v != 0}.items():
            if "percent" in stat:
                stat_affected = stat.split('_')[1]
                self.temporary_stats[stat_affected]["percent_increase"] = self.temporary_stats[stat_affected]["percent_increase"] - value
            else:
                self.temporary_stats[stat]["flat_increase"] = self.temporary_stats[stat]["flat_increase"] - value

    def read_temp_stat(self, temp_stat):
        if temp_stat in self.temporary_stats:
            return '(' + str(self.temporary_stats[temp_stat]) + ')'
        else:
            return ''

    def get_temp_stat(self, temp_stat):
        # Add flat increase and multiply percentage increase with the current stat
        return math.floor(self.stats[temp_stat] * (self.temporary_stats[temp_stat]["percent_increase"] + 100) / 100 + self.temporary_stats[temp_stat]["flat_increase"])

    def decrease_status_effect_durations(self):
        if len(self.status_effects) == 0:
            return
        for status_effect_name in list(self.status_effects.keys()):
            status_effect = self.status_effects[status_effect_name]
            if status_effect.duration > 1:
                status_effect.duration -= 1
            else:
                self.status_effects.pop(status_effect_name)
                self.delete_temp_stats(status_effect)

    def attack(self, enemy):
        input(f"\n{self.name} attacks {enemy.name}!")
        hit_chance = BASE_CHANCE_HIT + self.get_temp_stat("dexterity")
        print(f"Hit chance: {hit_chance}")
        random_variable = random.randint(0, 100)
        if random_variable <= hit_chance:
            random_variable = random.randint(0, 100)
            if self.physical:
                damage = self.get_temp_stat("strength") - enemy.get_temp_stat("defense")
            else:
                damage = self.get_temp_stat("strength") - enemy.get_temp_stat("resistance")
            damage = util.not_less_zero(damage)
            if random_variable <= self.get_temp_stat("luck"):                  # Critical Hit
                damage = damage * 2
                print("Critical Hit!")
            print(f"{self.name} hits {enemy.name} for {damage} ({hit_chance})!\n")
            enemy.hp -= damage
            enemy.hp = util.not_less_zero(enemy.hp)
        else:
            print("Miss!\n")

    def heal(self, heal_amount):
        input("Healing!\n")
        if self.hp > (self.max_hp - heal_amount):
            self.hp = self.max_hp
        else:
            self.hp += heal_amount
        print(f"{self.name} heals for {heal_amount}, back to {self.hp}!")



class Party:
   def __init__(self, units, gold, rations):
       self.units = units
       self.gold = gold
       self.rations = rations
       self.inventory = {}

   def __str__(self):
       unit_text = ""
       for unit in self.units:
           unit_text += str(unit) + "\n"
       return unit_text + "Gold: " + str(self.gold) + "\nRations: " + str(self.rations)

   def __repr__(self):
        units_repr = [repr(unit) for unit in self.units]
        return f"Party(units={units_repr}, gold={self.gold}, rations={self.rations}, inventory={self.inventory})"



class StatusEffect:
    def __init__(self, name, duration, description):
        self.name = name
        self.duration = duration
        self.description = description
        self.effects = {
            "strength": 0,
            "percent_strength": 0,
            "defense": 0,
            "percent_defense": 0,
            "resistance": 0,
            "percent_resistance": 0,
            "dexterity": 0,
            "percent_dexterity": 0,
            "speed": 0,
            "percent_speed": 0,
            "luck": 0,
            "percent_luck": 0
        }

    def __str__(self):
        return f"{self.name}: {self.description} ({self.duration} Turn/s)\n" + self.read_effects()

    def __repr__(self):
        return f"StatusEffect(name={self.name}, duration={self.duration}, description={self.description}, effects={self.effects})"

    def read_effects(self):
        effects = ""
        for key in self.effects:
            if self.effects[key] != 0:
                if self.effects[key] > 0:
                    effects += f"{key.capitalize()}: +{self.effects[key]}"
                elif self.effects[key] < 0:
                    effects += f"{key.capitalize()}: {self.effects[key]}"
                if "percent" in key:
                    effects += "%"
                effects += "\n"
        return effects

    def apply_effect(self, stat, value):
        if stat in self.effects:
            self.effects[stat] = value
        else:
            print("Invalid stat!")

testingStatusEffect = StatusEffect("Testing", 3, "Testing Effects")
testingStatusEffect.apply_effect("strength", 10)

testingStatusEffect2 = StatusEffect("More Testing", 1, "Bees")
testingStatusEffect2.apply_effect("percent_strength", -10)

hardenEffect = StatusEffect("Harden", 3, "Minor defense increase")
hardenEffect.apply_effect("defense", 10)

resistEffect = StatusEffect("Resist", 3, "Minor resistance increase")
resistEffect.apply_effect("resistance", 10)

accuracyEffect = StatusEffect("Accuracy", 3, "Minor dexterity increase")
accuracyEffect.apply_effect("dexterity", 20)

speedEffect = StatusEffect("Speed", 3, "Minor speed increase")
speedEffect.apply_effect("speed", 10)

luckyEffect = StatusEffect("Lucky", 3, "Minor luck increase")
luckyEffect.apply_effect("luck", 70)