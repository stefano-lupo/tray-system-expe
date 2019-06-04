import asyncio
import websockets
import json
from threading import Thread
from simple_websocket_server import WebSocketServer, WebSocket
from tray_system.state import State, StatePacket
from core.config import WEBSOCKET_BASE_URL, WEBSOCKET_PORT

class SimpleEcho(WebSocket):
    def handle(self):
        # echo message back to client
        self.send_message(self.data)

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')

class WebSocketHandler:
    def __init__(self):
        self.server = WebSocketServer(WEBSOCKET_BASE_URL, WEBSOCKET_PORT, SimpleEcho)
        self.t = Thread(target=lambda: self.server.serve_forever())
        self.t.start()

    def push_state(self, next_state: StatePacket):
        # self.state = next_state
        print("Pushing state to %s clients" % len(self.server.connections.values()))
        as_json = json.dumps(next_state.get_as_dict())
        for client in self.server.connections.values():
            client.send_message(as_json)
