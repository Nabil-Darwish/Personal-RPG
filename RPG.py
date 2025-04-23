import os
import threading
import music
import unit
import combat_manager
from colorama import init, Fore
from item import smallHealthPotion, largeHealthPotion, smallInstantHarmingPotion, HealthPotion, InstantPoisonPotion, \
    ItemUse
from status_effect import testingStatusEffect, testingStatusEffect2, hardenEffect, resistEffect, accuracyEffect, speedEffect, luckyEffect
from util import FightOutcome

# Initialises the player and the enemy
def initialise_player_and_enemy(name):
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
    init()
    soundtrack_mute = False
    stop_event = music.initialise_music()
    music.start_music_thread(stop_event, "music/cats.wav", soundtrack_mute)
    name = input("What's your name? \n")
    os.system('cls')
    music.stop_current_music_thread(stop_event)
    stop_event = threading.Event()
    music.start_music_thread(stop_event, "music/riff.wav", soundtrack_mute)
    player_party, enemy_party = initialise_player_and_enemy(name)
    player_party.add_inventory(smallHealthPotion)
    player_party.add_inventory(largeHealthPotion)
    player_party.add_inventory(smallInstantHarmingPotion)
    player_party.units[0].add_status_effect(luckyEffect)

    combat = combat_manager.CombatManager(player_party, enemy_party)
    combat.start_battle()

    music.stop_current_music_thread(stop_event)
    if combat.outcome == FightOutcome.PLAYER_VICTORY:
        music.stop_and_play_music('music/victory.wav', soundtrack_mute)
        input("Congatulations\n")
    else:
        music.stop_and_play_music('music/game over.wav', soundtrack_mute)
        input("Sorry! Try again!\n")
    

if __name__ == '__main__':
    main()