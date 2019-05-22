import time
from tray_system.screen_manager import ScreenManager
from tray_system.state import State

if __name__ == "__main__":
    print("Starting tray system")
    screen_manager: ScreenManager = ScreenManager()
    # screen_manager.mainloop()
    time.sleep(2000)
    print("Closing doorS")

    # screen_manager.progress_state(State.DOOR_CLOSING)
    # time.sleep(2)
