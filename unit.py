import random
import util
import math

BASE_CHANCE_HIT = 50

class InsufficientGoldError(Exception):
    pass

class UnitNotFoundError(Exception):
    pass

class InsufficientRationsError(Exception):
    pass

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
        self.observers = []

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
STR : {self.get_stat_with_effects("strength")}
DEF : {self.get_stat_with_effects("defense")}
RES : {self.get_stat_with_effects("resistance")}
DEX : {self.get_stat_with_effects("dexterity")}
SPD : {self.get_stat_with_effects("speed")}
LCK : {self.get_stat_with_effects("luck")}

Status Effects:\n""" + (', '.join(map(str, self.status_effects.values())))

    def acronymised_stats(self):
        acronym_map = {
            "strength": "STR",
            "defense": "DEF",
            "resistance": "RES",
            "dexterity": "DEX",
            "speed": "SPD",
            "luck": "LCK"
        }
        return {acronym_map[k]: self.get_stat_with_effects(k) for k, v in self.stats.items()}

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def add_status_effect(self, added_status_effect):
        # Get the status effect from the list of status effects applied to the unit by name
        self.status_effects[added_status_effect.name] = added_status_effect
        for stat, value in {k:v for k, v in added_status_effect.effects.items() if v != 0}.items():
            if "percent" in stat:
                stat_affected = stat.split('_')[1]
                self.temporary_stats[stat_affected]["percent_increase"] += value
            else:
                self.temporary_stats[stat]["flat_increase"] += value

    def get_status_effects_str(self):
        return ', '.join(map(str, self.status_effects.values()))

    # This only occurs if the status effect is popped out of the list
    def delete_temp_stats(self, removed_status_effect):
        #  From the list of stats that are affected by the status effect
        for stat, value in {k:v for k, v in removed_status_effect.effects.items() if v != 0}.items():
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

    def get_stat_with_effects(self, stat):
        return str(self.stats[stat]) + " (" + str(self.get_temp_stat(stat)) + ")"

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
        print(f"\n{self.name} attacks {enemy.name}!")
        util.pause(500)
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
            enemy.hp -= damage
            enemy.hp = util.not_less_zero(enemy.hp)
            print(f"{self.name} hits {enemy.name} for {damage} ({hit_chance})! {enemy.name} has {enemy.hp} HP left!\n")
            util.pause(800)
            if enemy.hp == 0:
                print(f"{enemy.name} is dead!\n")
                util.pause(500)
                enemy.notify_observers()
        else:
            print("Miss!\n")

    def heal(self, heal_amount):
        print("Healing!\n")
        util.pause(500)
        if self.hp > (self.max_hp - heal_amount):
            self.hp = self.max_hp
        else:
            self.hp += heal_amount
        print(f"{self.name} heals for {heal_amount}, back to {self.hp}!")



class Party:
   def __init__(self, gold, rations):
       self.units = []
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

   def show_units(self):
       for unit in self.units:
           print(unit)

   def is_player_party(self):
       return self.units[0].player

   def get_units_stats_list_dict(self):
       units_stats_list_dict = []
       for unit in self.units:
           unit_stats = {"Name": unit.name, "HP/Full HP": str(unit.hp) + "/" + str(unit.max_hp), **unit.acronymised_stats()}
           units_stats_list_dict.append(unit_stats)
       return units_stats_list_dict

   def get_status_effects_units(self):
       party_status_effects_txt = ""
       for unit in self.units:
           if len(unit.status_effects) > 0:
               party_status_effects_txt += unit.name + ":\n"
               party_status_effects_txt += unit.get_status_effects_str() + "\n"
       return party_status_effects_txt

   @property
   def unit_count(self):
       return len(self.units)

   def update(self, unit):
       self.remove_unit(unit)

   def add_unit(self, unit):
       self.units.append(unit)
       unit.add_observer(self)

   def remove_unit(self, unit):
       if unit not in self.units:
           raise UnitNotFoundError("Unit not found!")
       unit.remove_observer(self)
       self.units.remove(unit)

   def add_gold(self, added_gold):
       self.gold += added_gold

   def remove_gold(self, removed_gold):
       if (self.gold - removed_gold) < 0:
           raise InsufficientGoldError("Not enough gold!")
       self.gold -= removed_gold

   def add_rations(self, added_rations):
       self.rations += added_rations

   def remove_rations(self, removed_rations):
       if (self.rations - removed_rations) < 0:
           raise InsufficientRationsError("Not enough rations!")
       self.rations -= removed_rations

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

   def add_inventory(self, item):
       if item.name in self.inventory:
           self.inventory[item.name].stack_size += item.stack_size
       else:
           self.inventory[item.name] = item

   def remove_inventory(self, item_name):
       if self.inventory[item_name].stack_size > 1:
           self.inventory[item_name].stack_size -= 1
       else:
           self.inventory.pop(item_name)