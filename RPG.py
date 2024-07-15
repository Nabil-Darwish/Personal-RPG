import random
import os
import sys
import time

class Unit:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def __str__(self):
        return f"Name: {self.name} \nHP  : {self.hp}   \n"
    
    def attack(self, enemy):
        input("Press Enter to continue \n")
        print(f"{self.name} attacks {enemy.name}!")
        randomVariable = random.randint(0, 100)
        if randomVariable < 70:
            print("Hit!")
            enemy.hp -= 1
        else:
            print("Miss!")


def main():
    name = input("What's your name? \n")
    playerUnit = Unit(name, 5)
    enemyUnit = Unit("Enemy", 5)
    print(playerUnit)
    print(enemyUnit)
    while enemyUnit.hp > 0:
        playerUnit.attack(enemyUnit)
    print("Enemy defeated")
if __name__ == '__main__':
    sys.exit(main())
