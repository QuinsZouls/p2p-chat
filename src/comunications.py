import asyncio
import socket
import json
import logging
import websockets
import os
import threading
# Env
SERVER_WS_PORT = os.getenv('SERVER_WS_PORT', 6789)
SERVER_SK_PORT = os.getenv('SERVER_WS_PORT', 6790)
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
    def run(self):
        print('starting Websocket')
        logging.info("Starting Websocket service")
        server =  websockets.serve(self.listen, SERVER_URL, SERVER_WS_PORT)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()

    async def listen(self, websocket, path):
        while True:
            try:
                await websocket.send(json.dumps(CONNECTED_RESPONSE))
                async for message in websocket:
                    data = json.loads(message)
                    self.requestHandler(websocket, data)
            except:
                logging.error("Error in ws request")
    def requestHandler(self, websocket, request):
        if request['option'] == 'message':
            _thread = threading.Thread(target=asyncio.run, args=(self.messageHandler(request),))
            _thread.start()
        elif request['option'] == 'register':
            pass
    async def messageHandler(self, request):
        print(request)
    def registerUser(self, data):
        pass
class SocketServer():
    def __init__(self):
        try:
            self.socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            logging.exception('Error initializing socket service')
    def run(self):
        print('starting socket')
        logging.info("Starting Socket service")
        self.socket_instance.bind(("localhost", SERVER_SK_PORT))
        self.socket_instance.listen(10)
        self.listen()
    def listen(self):
        while True:
            try:
                # accept connections from outside
                (clientsocket, address) = self.socket_instance.accept()
                # now do something with the clientsocket
                # in this case, we'll pretend this is a threaded server
                request =  clientsocket.recv(BUFFER_SIZE).decode()
                parsedReq = json.loads(request)
                if parsedReq['option'] == 'message':
                    #Process menssage
                    print(parsedReq)
            except:
                logging.exception("Unknown error")
