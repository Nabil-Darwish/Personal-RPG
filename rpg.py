import os
import threading
import gui
import music
import unit
import combat_manager
from colorama import init, Fore
from item import smallHealthPotion, largeHealthPotion, smallInstantHarmingPotion
from status_effect import luckyEffect
from rpg_enum import FightOutcome

class TerraIncognita:
    def __init__(self):
        init()
        self.music_manager = music.MusicManager()
        self.gui = gui.GUI()
        self.name = "Terra Incognita"

    # Initialises the player and the enemy
    def initialise_player_and_enemy(self, name):
        player_unit = unit.Unit(name = name, player = True, physical = True, max_hp = 10, strength = 6, defense = 2, resistance = 0, dexterity = 30, speed = 3, luck = 30)
        licht_unit = unit.Unit("Licht", True, False, 10, 4, 0, 3, 10, 6, 5)
        player_party = unit.Party(0, 0)
        player_party.add_unit(player_unit)
        player_party.add_unit(licht_unit)
        enemy_unit = unit.Unit("Enemy 1", False, False, 10, 4, 3, 0, 10, 5, 5)
        enemy_unit_2 = unit.Unit("Enemy 2", False, False, 10, 4, 3, 0, 10, 5, 5)
        enemy_party = unit.Party( 0, 0)
        enemy_party.add_unit(enemy_unit)
        enemy_party.add_unit(enemy_unit_2)
        return player_party, enemy_party

# Main gameplay loop
def main():
    rpg = TerraIncognita()
    rpg.music_manager.start_music_thread("music/cats.wav")
    name = input("What's your name? \n")
    os.system('cls')
    rpg.music_manager.stop_current_music_thread()
    rpg.music_manager.start_music_thread("music/riff.wav")
    player_party, enemy_party = rpg.initialise_player_and_enemy(name)
    player_party.add_inventory(smallHealthPotion)
    player_party.add_inventory(largeHealthPotion)
    player_party.add_inventory(smallInstantHarmingPotion)
    player_party.units[0].add_status_effect(luckyEffect)

    combat = combat_manager.CombatManager(player_party, enemy_party)
    combat.start_battle()

    rpg.music_manager.stop_current_music_thread()
    if combat.outcome == FightOutcome.PLAYER_VICTORY:
        rpg.music_manager.stop_and_play_music('music/victory.wav')
        input("Congatulations\n")
    else:
        rpg.music_manager.stop_and_play_music('music/game over.wav')
        input("Sorry! Try again!\n")
    

if __name__ == '__main__':
    main()