from enum import Enum

class State(Enum):
    READY = 1,
    INVALID_RFID = 2,
    RFID_READ = 3,
    ROLLER_FEEDING = 4,
    DOOR_CLOSING = 5,
    IMAGE_START = 6,
    IMAGE_ANALYZING = 12,
    IMAGE_FINISHED = 7,
    LOWERING = 8,
    LOWERING_ERROR = 9,
    LOWERING_FINISH = 10,
    UNKNOWN = 11

class StatePacket:

    def __init__(self, state = State.READY, data = {}):
        self.state = state
        self.data = data

    def get_as_dict(self):
        return {
            "state": self.state.name,
            "data": self.data
        }

    @classmethod
    def from_string(cls, line: str):
        state_string = str(line)
        state_string = state_string[2:-5]
        data_string = ""
        
        # state = None
        if "-" in state_string:
            [state_string, data_string] = state_string.split("-")
        
        print("Had state_string: %s, data_string %s" % (state_string, data_string))

        try:
            # print("Getting from enum %s" % state_string)
            state: State = State[state_string]
            # print("Parsed state was %s" % state.name)
        except KeyError:
            print("ARDUINO LOG: %s" % state_string)
            return cls(State.UNKNOWN)

        print("State: %s" % state.name)
        print("Data: %s" % data_string)
        return cls(state, data_string)