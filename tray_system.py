from time import sleep
import serial
import cv2 as cv
# import pyrealsense2 as rs

from tray_system.inputs.RealSenseCapturer import RealSenseCapturer

from tray_system.screen_manager import ScreenManager
from tray_system.state import State

if __name__ == "__main__":
    # print("Starting tray system")
    # screen_manager: ScreenManager = ScreenManager()
    # # screen_manager.mainloop()
    # time.sleep(2000)
    # print("Closing doorS")

    # screen_manager.progress_state(State.DOOR_CLOSING)
    # time.sleep(2)

     ser = serial.Serial('/dev/ttyACM0', 9600)
     realsense_capturer = RealSenseCapturer()
     while True:
          # counter +=1
          # ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
          line = ser.readline()
          print("Line was %s " % line)

          realsense_capturer.capture()
          sleep(.1) # Delay for one tenth of a second
