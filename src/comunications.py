import asyncio
import socket
import json
import logging
import websockets
import os
import threading
# Env
SERVER_WS_PORT = os.getenv('SERVER_PORT', 6789)
SERVER_URL = os.getenv('SERVER_URL', "localhost")
BUFFER_SIZE = 4096
# Setup logging
logging.basicConfig(filename='system.log')
CONNECTED_RESPONSE = {
    "status": "ok",
    "type": "info",
    "response": "Connection established"
}

class WebsocketServer():
    #Start asyncio process
    def __init__(self):
        self.server_instance = websockets.serve(self.listen, SERVER_URL, SERVER_WS_PORT)
    def run(self):
        print('starting Websocket')
        logging.info("Starting Websocket service")
        asyncio.get_event_loop().run_until_complete(self.server_instance)
        asyncio.get_event_loop().run_forever()

    async def listen(self, websocket):
        try:
            await websocket.send(json.dumps(CONNECTED_RESPONSE))
            async for message in websocket:
                data = json.loads(message)
                self.requestHandler(websocket, data)
        except:
            logging.error("Error starting server")
    def requestHandler(self, websocket, request):
        if request['option'] == 'sendImage':
            _thread = threading.Thread(target=asyncio.run, args=(self.messageHandler(request['image']),))
            _thread.start()
    async def messageHandler(self, request):
        print(request)
class SocketServer():
    def __init__(self):
        self.socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        print('starting socket')
        logging.info("Starting Socket service")
        self.socket_instance.bind(("localhost", 6791))
        self.socket_instance.listen(10)
        asyncio.get_event_loop().run_until_complete(self.listen)
        asyncio.get_event_loop().run_forever()
    def listen(self):
        try:
                # accept connections from outside
                (clientsocket, address) = self.socket_instance.accept()
                # now do something with the clientsocket
                # in this case, we'll pretend this is a threaded server
                request = clientsocket.recv(BUFFER_SIZE).decode()
                parsedReq = json.loads(request)
                if parsedReq['option'] == 'message':
                    #Process menssage
                    print(parsedReq)
        except:
            logging.exception("Unknown error")

class CommunicationDriver:
    def start(self):
        try:
            websocket = WebsocketServer()
            socket = SocketServer()
            _thread1 =  threading.Thread(target=asyncio.run, args=(websocket.run(),))
            _thread2 =  threading.Thread(target=asyncio.run, args=(socket.run(),))
            _thread2.start()
            _thread1.start()

        except:
            logging.exception("Error with communication thread")
