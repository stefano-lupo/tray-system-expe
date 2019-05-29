from enum import Enum


class State(Enum):
    READY = 1,
    INVALID_RFID = 2,
    RFID_READ = 3,
    ROLLER_FEEDING = 4,
    DOOR_CLOSING = 5,
    IMAGE_CAPTURE = 6,
    LOWERING = 7,
    LOWERING_ERROR = 8,
    LOWERING_FINISH = 9