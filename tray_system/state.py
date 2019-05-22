from enum import Enum

from .screens.ready_screen import ReadyScreen
from .screens.door_closing import DoorClosing

class State(Enum):
    READY = ReadyScreen,
    # INVALID_RFID = 2,
    # ROLLER_FEEDING = 3,
    DOOR_CLOSING = DoorClosing,
    # IMAGE_CAPTURE = 5,
    # LOWERING = 6,
    # LOWERING_ERROR = 7,
    # LOWERING_FINISH = 8



