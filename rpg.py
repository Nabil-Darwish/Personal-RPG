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
        self.music_manager = music.MusicManager(True)
        self.name = "Terra Incognita"
        self.gui = None
        self.initialise_gui()

    def initialise_gui(self):
        # Initialising GUI
        self.gui = gui.GUI()

        # Adding flag observers with appropriate functions
        self.gui.add_observer(rpg_enum.GUINotification.MUSIC_PLAY, self.start_music)
        self.gui.add_observer(rpg_enum.GUINotification.MUSIC_CHANGE, self.change_music)
        self.gui.add_observer(rpg_enum.GUINotification.PLAYER_NAME_SUBMITTED, self.initialise_player_and_enemy)

        # Update
        self.gui.update_title(self.name)

        # Showing start screen
        self.gui.start_screen()

    # Initialises the player and the enemy when a name is submitted back to the game
    def initialise_player_and_enemy(self, name):
        # Generating player party
        player_unit = unit.Unit(name = name, player = True, physical = True, max_hp = 10, strength = 6, defense = 2, resistance = 0, dexterity = 30, speed = 3, luck = 30)
        licht_unit = unit.Unit("Licht", True, False, 10, 4, 0, 3, 10, 6, 5)
        player_party = unit.Party(0, 0)
        player_party.add_unit(player_unit)
        player_party.add_unit(licht_unit)

        # Generating enemy party
        enemy_unit = unit.Unit("Enemy 1", False, False, 10, 4, 3, 0, 10, 5, 5)
        enemy_unit_2 = unit.Unit("Enemy 2", False, False, 10, 4, 3, 0, 10, 5, 5)
        enemy_party = unit.Party( 0, 0)
        enemy_party.add_unit(enemy_unit)
        enemy_party.add_unit(enemy_unit_2)

        # Adding items
        player_party.add_inventory(smallHealthPotion)
        player_party.add_inventory(largeHealthPotion)
        player_party.add_inventory(smallInstantHarmingPotion)
        player_party.units[0].add_status_effect(luckyEffect)

        # Initialising combat system
        self.initialise_combat(player_party, enemy_party)

    def initialise_combat(self, player_party, enemy_party):
        # Stop music and start battle music
        self.music_manager.stop_current_music_thread()
        self.music_manager.start_music_thread("music/riff.wav")

        # Initialising the combat manager
        self.combat_manager = combat_manager.CombatManager(player_party, enemy_party)

        # Adding flag observers from gui to combat manager with appropriate functions
        self.gui.add_observer(rpg_enum.GUINotification.PLAYER_ATTACK, self.combat_manager.player_attack)
        self.gui.add_observer(rpg_enum.GUINotification.PLAYER_HEAL, self.combat_manager.player_heal)
        self.gui.add_observer(rpg_enum.GUINotification.PLAYER_INVENTORY, self.combat_manager.player_party.read_inventory)
        self.gui.add_observer(rpg_enum.GUINotification.REQUEST_CURRENT_UNIT_TABLE, self.combat_manager.show_party_tables)
        self.gui.add_observer(rpg_enum.GUINotification.REQUEST_UNIT_TURN_ORDER, self.combat_manager.get_new_turn_order)
        self.gui.add_observer(rpg_enum.GUINotification.REQUEST_NEXT_UNIT, self.combat_manager.get_next_turn_unit)

        # Adding flag observers from combat manager to GUI with appropriate functions
        self.combat_manager.add_observer(rpg_enum.CombatNotification.INITIAL_STATS_SCREEN, self.gui.initial_stats_screen)
        self.combat_manager.add_observer(rpg_enum.CombatNotification.COMBAT_GRID_SCREEN, self.gui.combat_grid_screen)
        self.combat_manager.add_observer(rpg_enum.CombatNotification.COMBAT_GRID_NEW_TURN_ORDER, self.gui.new_turn_order_received)
        self.combat_manager.add_observer(rpg_enum.CombatNotification.COMBAT_GRID_LOG_TEXT_UPDATE, self.gui.add_combat_log_text)
        self.combat_manager.add_observer(rpg_enum.CombatNotification.COMBAT_GRID_PLAYER_TABLE_UPDATE, self.gui.update_player_table)
        self.combat_manager.add_observer(rpg_enum.CombatNotification.COMBAT_GRID_ENEMY_TABLE_UPDATE, self.gui.update_enemy_table)
        self.combat_manager.add_observer(rpg_enum.CombatNotification.COMBAT_GRID_PLAYER_TURN, self.gui.player_turn)
        self.combat_manager.add_observer(rpg_enum.CombatNotification.COMBAT_GRID_ENEMY_TURN, self.gui.enemy_turn)

        # Starting the battle
        self.combat_manager.start_battle()

    #DISCONNECTED: How battles end
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

    # Command to change the music
    def change_music(self, sound_file):
        self.music_manager.stop_current_music_thread()
        self.music_manager.start_music_thread(sound_file)

    # Command to toggle the music. Not currently used
    def toggle_soundtrack_mute(self):
        self.music_manager.toggle_soundtrack_mute()

    # DISCONNECTED
    def request_unit_tables(self):
        return self.combat_manager.player_party, self.combat_manager.enemy_party

# Main gameplay loop
def main():
    TerraIncognita()

if __name__ == '__main__':
    main()
