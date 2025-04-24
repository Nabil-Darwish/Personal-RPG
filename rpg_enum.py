from enum import Enum, auto

class FightOutcome(Enum):
    PLAYER_VICTORY = auto()
    ENEMY_VICTORY = auto()

class GUINotification(Enum):
    PLAYER_NAME_SUBMITTED = auto()
    PLAYER_ATTACK = auto()
    PLAYER_INVENTORY = auto()
    PLAYER_HEAL = auto()
    MUSIC_PLAY = auto()
    MUSIC_CHANGE = auto()
    MUSIC_MUTE = auto()