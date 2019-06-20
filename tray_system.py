############################################
# Run me to actually run the prototype!
# Wow, useful!
############################################

from time import sleep

import serial

from backend.detection.scan_handler import ScanHandler
from core.scan_request import ScanRequest
from tray_system.data_pusher import DataPusher
from tray_system.real_sense_capturer import RealSenseCapturer
from tray_system.state import State, StatePacket
from tray_system.web_socket_handler import WebSocketHandler

PORT = '/dev/ttyACM0'
BAUD = 115200

# Switch whether we want to run the CNN locally (on the prototype)
# or remotely (on the server)
# Idk how fast the CNN would run on the PI
# If we run it remotely we need some more code to send the response back to the prototype
# to display it to the canteen wankers
COMPUTE_LOCAL = True


class TraySystem:

    def __init__(self, initial_state: StatePacket = StatePacket()):
        self.data_pusher = DataPusher()
        self.web_socket_handler = WebSocketHandler()
        self.scan_handler = ScanHandler()
        self.serial_link = serial.Serial(PORT, BAUD)
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

    """
    Waits for messages from the arduino to indicate state of system
    """
    def poll_serial(self):
        while True:
            line = self.serial_link.readline()
            self.state_packet = StatePacket.from_string(line)

            # Any Serial.println() from arduino will end up here
            # So its quite likely we will get some messages we don't care about
            if self.state_packet.state == State.UNKNOWN:
                continue

            print("Received state update to %s" % self.state_packet.state.name)
            self.handle_state_change()
    
    def handle_state_change(self):

        # Arduino tells us to take the picture
        if self.state_packet.state == State.IMAGE_START:

            # Inform prototype dashboard that we are analyzing the image
            self.state_packet = StatePacket(State.IMAGE_ANALYZING)
            self.web_socket_handler.push_state(self.state_packet)

            # Run the scan
            scan_id = self.scan()

            # Inform the proto dash that we are done and tell it what the scan id was
            self.state_packet = StatePacket(State.IMAGE_FINISHED, scan_id)
            self.web_socket_handler.push_state(self.state_packet)

            # Wait for awhile before allowing the state to progress so we don't accept new trays
            # while showing the old results (gross hack)
            sleep(4)

            # Inform arduino that we are ready for next tray
            self.serial_link.write(bytes(b'IMAGE_FINISH'))

        # Since RFID read happens before we need to take the picture
        # we need to keep track of it in memory
        # Also inform dash that we have succesfully read the tray
        elif self.state_packet.state == State.RFID_READ:
            self.last_rfid = self.state_packet.data
            self.web_socket_handler.push_state(self.state_packet)

        # Forward the state update to the dashboard
        else:
            self.web_socket_handler.push_state(self.state_packet)

    def scan(self):

        # This shouldn't happen
        if self.last_rfid is None:
            print("Tried to scan without RFID")
            self.last_rfid = 1
            # return

        colour_img, depth_img = self.realsense_capturer.capture()
        menu_item_id = self.last_rfid
        user_id = 1     # Haven't implemented user specific RFID stuff yet
        scan_request = ScanRequest(colour_img, depth_img, menu_item_id, user_id)

        # Either handle scan locally or push to server.
        if COMPUTE_LOCAL:
            return self.scan_handler.handle_local_scan(scan_request)

        return self.data_pusher.push_scan(scan_request)


if __name__ == "__main__":
    print("Starting tray system - using baud rate %d, compute local %s" % (BAUD, COMPUTE_LOCAL))
    tray_system = TraySystem()
    tray_system.poll_serial()


