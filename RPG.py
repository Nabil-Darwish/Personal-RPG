import random
import os
import sys
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading

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
    
    def attack(self, enemy):
        input("Press Enter to continue \n")                 ##Might need to remove this later
        print(f"{self.name} attacks {enemy.name}!")
        hitChance = 70 + self.dexterity
        randomVariable = random.randint(0, 100)
        if randomVariable < hitChance:
            randomVariable = random.randint(0, 100)
            if self.physical:
                damage = self.strength - enemy.defense
            else:
                damage = self.strength - enemy.resistance
            damage = not_less_zero(damage)
            if randomVariable < self.luck:                  ## Critical Hit
                damage = damage * 2
            print(f"{self.name} hits {enemy.name} for {damage} ({hitChance})!")
            enemy.hp -= damage
            enemy.hp = not_less_zero(enemy.hp)
            print(enemy)
        else:
            print("Miss!")

class Party:
    def __init__

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
        self.player_unit.attack(self.enemy_unit)

    def enemy_turn(self):
        self.enemy_unit.attack(self.player_unit)

def not_less_zero(variable):
    return max(0, variable)

def pick_random_from(l):
    randomVariable = random.randint(0, len(l))
    return l[randomVariable]

def start_music_thread(stop_event, sound_file):
    music_thread = threading.Thread(target=looping_music, args=(stop_event, sound_file), daemon=True)
    music_thread.start()

def stop_current_music_thread(stop_event):
    stop_event.set()
    time.sleep(0.1)

def looping_music(stop_event, sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(-1)  # Play music in a loop
    while not stop_event.is_set():
        time.sleep(0.1)
    pygame.mixer.music.stop()

def stop_and_play_music(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()


def main():
    pygame.mixer.init()
    stop_event = threading.Event()
    start_music_thread(stop_event, "music/cats.wav")
    name = input("What's your name? \n")
    stop_current_music_thread(stop_event)
    stop_event = threading.Event()
    start_music_thread(stop_event, "music/riff.wav")
    playerUnit = Unit(name = name, player = True, physical = False, max_hp = 5, strength = 6, defense = 2, resistance = 8, dexterity = 30, speed = 3, luck = 100)
    enemyUnit = Unit("Enemy", False, False, 5, 6, 3, 0, 10, 5, 5)
    print(playerUnit)
    print(enemyUnit)
    combat = CombatManager(playerUnit, enemyUnit)
    outcome = combat.start_battle()
    stop_current_music_thread(stop_event)
    if outcome == 0:
        stop_and_play_music('music/victory.wav')
        input("Congatulations\n")
    else:
        stop_and_play_music('music/game over.wav')
        input("Sorry! Try again!\n")
    

if __name__ == '__main__':
    main()