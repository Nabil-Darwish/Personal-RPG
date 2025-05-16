from enum import Enum, auto

class FightOutcome(Enum):
    PLAYER_VICTORY = auto()
    ENEMY_VICTORY = auto()

# These are notifications coming from the GUI object
class GUINotification(Enum):
    PLAYER_NAME_SUBMITTED = auto()
    PLAYER_ATTACK = auto()
    PLAYER_INVENTORY = auto()
    REQUEST_CURRENT_UNIT_TABLE = auto()
    PLAYER_HEAL = auto()
    MUSIC_PLAY = auto()
    MUSIC_CHANGE = auto()
    MUSIC_MUTE = auto()

# These are notifications coming from the CombatManager
class CombatNotification(Enum):
    COMBAT_GRID_SCREEN = auto()
    INITIAL_STATS_SCREEN = auto()
    MAIN_BATTLE_SCREEN = auto()
    INVENTORY_SCREEN = auto()
    PICK_ENEMY_SCREEN = auto()
