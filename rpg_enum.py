from enum import Enum, auto

class FightOutcome(Enum):
    PLAYER_VICTORY = auto()
    ENEMY_VICTORY = auto()

# These are notifications coming from the GUI object. This represents commands that come from the GUI
class GUINotification(Enum):
    PLAYER_NAME_SUBMITTED = auto()
    PLAYER_ATTACK = auto()
    PLAYER_HEAL = auto()
    PLAYER_INVENTORY = auto()
    REQUEST_CURRENT_UNIT_TABLE = auto()
    REQUEST_UNIT_TURN_ORDER = auto()
    REQUEST_NEXT_UNIT = auto()
    MUSIC_PLAY = auto()
    MUSIC_CHANGE = auto()
    MUSIC_MUTE = auto()

# These are notifications coming from the CombatManager. This should represent the screens that need to be shown to the player
class CombatNotification(Enum):
    COMBAT_GRID_SCREEN = auto()
    COMBAT_GRID_NEW_TURN_ORDER = auto()
    COMBAT_GRID_UNIT_TURN_END = auto()
    COMBAT_GRID_LOG_TEXT_UPDATE = auto()
    COMBAT_GRID_PLAYER_TABLE_UPDATE = auto()
    COMBAT_GRID_ENEMY_TABLE_UPDATE = auto()
    COMBAT_GRID_PLAYER_TURN = auto()
    COMBAT_GRID_ENEMY_TURN = auto()
    COMBAT_GRID_BATTLE_END = auto()
    COMBAT_GRID_UPDATE_ATTACK_BUTTON = auto()
    COMBAT_GRID_UPDATE_HEAL_BUTTON = auto()
    COMBAT_GRID_UNIT_CANNOT_HEAL = auto()
    INITIAL_STATS_SCREEN = auto()
    MAIN_BATTLE_SCREEN = auto()
    INVENTORY_SCREEN = auto()
    PICK_ENEMY_SCREEN = auto()
