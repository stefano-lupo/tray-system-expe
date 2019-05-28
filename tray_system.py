from time import sleep
import serial
import cv2 as cv
# import pyrealsense2 as rs

from tray_system.inputs.real_sense_capturer import RealSenseCapturer

# from tray_system.screen_manager import ScreenManager
# from tray_system.state import State

from core.scan_request import ScanRequest
from tray_system.data_pusher import DataPusher

PORT = '/dev/ttyACM0'
BAUD = 9600

class TraySystem:

    def __init__(self):
        self.data_pusher = DataPusher()
        # self.serial_link = serial.Serial(PORT, BAUD)
        self.realsense_capturer = RealSenseCapturer()


    def poll_keyboard(self):
        while True:
            # if cv.waitKey(1) & 0xFF == ord('q'):
            #     return
            if cv.waitKey(1) & 0xFF == ord(' '):
                self.scan()

    def poll_serial(self):
        while True:
            line = self.serial_link.readline()
            print("Serial message was %s " % line)
            self.scan()

    def scan(self):
        colour_img, depth_img = self.realsense_capturer.capture()
        print(colour_img.shape)
        print(depth_img.shape)
        scan_request = ScanRequest(colour_img, depth_img, 1, 1)

        self.data_pusher.push_scan(scan_request)
        sleep(.1)


if __name__ == "__main__":
    print("Starting tray system")
    tray_system = TraySystem()
    tray_system.poll_keyboard()
    # tray_system.poll_serial()



