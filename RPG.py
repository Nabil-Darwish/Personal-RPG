import random
import os
import sys
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading

class Unit:
    def __init__(self, name, hp, strength, defense, dexterity):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.defense = defense
        self.dexterity = dexterity

    def __str__(self):
        return f"""Name: {self.name}
HP  : {self.hp}   
STR : {self.strength} 
DEF : {self.defense}
DEX : {self.dexterity} \n"""
    
    def attack(self, enemy):
        input("Press Enter to continue \n")                 ##Might need to remove this later
        print(f"{self.name} attacks {enemy.name}!")
        hitChance = 70 + self.dexterity
        randomVariable = random.randint(0, 100)
        if randomVariable < hitChance:
            damage = self.strength - enemy.defense
            damage = not_less_zero(damage)
            print(f"{self.name} hits {enemy.name} for {damage} ({hitChance})!")
            enemy.hp -= damage
            enemy.hp = not_less_zero(enemy.hp)
            print(enemy)
        else:
            print("Miss!")

class CombatManager:
    def __init__(self, player_unit, enemy_unit):
        self.player_unit = player_unit
        self.enemy_unit = enemy_unit

    def start_battle(self):
        while self.player_unit.hp > 0 and self.enemy_unit.hp > 0:
            self.player_turn()
            if self.enemy_unit.hp <= 0:
                print("Enemy Defeated!")
                return 0

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

def battle(playerUnit, enemyUnit):
    while enemyUnit.hp > 0:
        playerUnit.attack(enemyUnit)

def looping_music(stop_event, sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(-1)  # Play music in a loop
    while not stop_event.is_set():
        time.sleep(0.1)
    pygame.mixer.music.stop()


def main():
    name = input("What's your name? \n")
    stop_event = threading.Event()
    music_thread = threading.Thread(target=looping_music, args=(stop_event, "music/riff.wav"), daemon=True)
    music_thread.start()
    playerUnit = Unit(name, 5, 6, 2, 10)
    enemyUnit = Unit("Enemy", 5, 6, 3, 10)
    print(playerUnit)
    print(enemyUnit)
    combat = CombatManager(playerUnit, enemyUnit)
    outcome = combat.start_battle()
    stop_event.set()
    time.sleep(0.1)
    if outcome == 0:
        pygame.mixer.music.load('music/victory.wav')
        pygame.mixer.music.play()
        input("Congatulations\n")
    else:
        pygame.mixer.music.load('music/game over.wav')
        pygame.mixer.music.play()
        input("Sorry! Try again!\n")
    

if __name__ == '__main__':
    main()
