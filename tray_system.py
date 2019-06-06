from time import sleep
import cv2 as cv
import serial
import asyncio

from tray_system.real_sense_capturer import RealSenseCapturer
from backend.detection.scan_handler import ScanHandler


from core.scan_request import ScanRequest
from tray_system.data_pusher import DataPusher
from tray_system.web_socket_handler import WebSocketHandler
from tray_system.state import State, StatePacket

PORT = '/dev/ttyACM0'
BAUD = 115200
COMPUTE_LOCAL = True

class TraySystem:

    def __init__(self, initial_state: StatePacket = StatePacket()):
        self.data_pusher = DataPusher()
        self.web_socket_handler = WebSocketHandler()
        self.scan_handler = ScanHandler()
        self.serial_link = None#serial.Serial(PORT, BAUD)
        self.realsense_capturer = RealSenseCapturer()
        self.state_packet = initial_state
        self.last_rfid = None
    
    def progress_state(self):
        states = list(State)
        self.state_packet = StatePacket(states[(states.index(self.state_packet.state) + 1) % len(states)])
        self.handle_state_change()

    def mock(self):
        while True:
            self.progress_state()
            sleep(2)

    def poll_serial(self):
        while True:
            line = self.serial_link.readline()
            self.state_packet = StatePacket.from_string(line)
            print("Received state update to %s" % self.state_packet.state.name)

            self.handle_state_change()
    
    def handle_state_change(self):
        if self.state_packet.state == State.IMAGE_START:
            scan_id = self.scan()
            self.state_packet = StatePacket(State.IMAGE_FINISHED, scan_id)
        if self.state_packet.state == State.RFID_READ:
            self.last_rfid = self.state_packet.data
        self.web_socket_handler.push_state(self.state_packet)


    def scan(self):
        if self.last_rfid is None:
            print("Tried to scan without RFID")
            return
        
        colour_img, depth_img = self.realsense_capturer.capture()
        print(colour_img.shape) 
        menu_item_id = 1 # Get this from RFID
        user_id = 1
        scan_request = ScanRequest(colour_img, depth_img, menu_item_id, user_id)
        if COMPUTE_LOCAL:
            return self.scan_handler.handle_local_scan(scan_request)

        return self.data_pusher.push_scan(scan_request)


if __name__ == "__main__":
    print("Starting tray system")
    tray_system = TraySystem()
    tray_system.last_rfid = 1
   
    while True:
        input("Press Enter to progress state...")
        tray_system.state_packet = StatePacket(State.IMAGE_START)
        tray_system.handle_state_change()
    # tray_system.poll_serial()
    # tray_system.mock()


