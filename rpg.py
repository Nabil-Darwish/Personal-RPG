import gui
import music
import rpg_enum
import unit
import combat_manager
from colorama import init, Fore
from item import smallHealthPotion, largeHealthPotion, smallInstantHarmingPotion
from status_effect import luckyEffect
from rpg_enum import FightOutcome, GUINotification

class TerraIncognita:
    def __init__(self):
        init()
        self.combat_manager = None
        self.music_manager = music.MusicManager(False)
        self.name = "Terra Incognita"
        self.gui = None
        self.initialise_gui()

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
        player_party.add_inventory(smallHealthPotion)
        player_party.add_inventory(largeHealthPotion)
        player_party.add_inventory(smallInstantHarmingPotion)
        player_party.units[0].add_status_effect(luckyEffect)
        self.initialise_combat(player_party, enemy_party)

    def initialise_gui(self):
        self.gui = gui.GUI()
        self.gui.add_observer(rpg_enum.GUINotification.MUSIC_PLAY, self.start_music)
        self.gui.add_observer(rpg_enum.GUINotification.MUSIC_CHANGE, self.change_music)
        self.gui.add_observer(rpg_enum.GUINotification.PLAYER_NAME_SUBMITTED, self.initialise_player_and_enemy)
        self.gui.change_title(self.name)
        self.gui.start_screen()

    def initialise_combat(self, player_party, enemy_party):
        self.music_manager.stop_current_music_thread()
        self.music_manager.start_music_thread("music/riff.wav")
        self.combat_manager = combat_manager.CombatManager(player_party, enemy_party)
        self.gui.add_observer(rpg_enum.GUINotification.PLAYER_ATTACK, self.combat_manager.player_attack)
        self.gui.add_observer(rpg_enum.GUINotification.PLAYER_INVENTORY, self.combat_manager.player_inventory)
        self.combat_manager.start_battle()
        self.end_combat()

    def end_combat(self):
        self.music_manager.stop_current_music_thread()
        if self.combat_manager.outcome == FightOutcome.PLAYER_VICTORY:
            self.music_manager.stop_and_play_music('music/victory.wav')
            input("Congatulations\n")
        else:
            self.music_manager.stop_and_play_music('music/game over.wav')
            input("Sorry! Try again!\n")

    def start_music(self):
        self.music_manager.start_music_thread("music/cats.wav")

    def change_music(self, sound_file):
        self.music_manager.stop_current_music_thread()
        self.music_manager.start_music_thread(sound_file)

# Main gameplay loop
def main():
    TerraIncognita()
    

if __name__ == '__main__':
    main()