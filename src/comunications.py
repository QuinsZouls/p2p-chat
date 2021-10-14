import asyncio
import socket
import json
import logging
import websockets
import os
import threading
import random
from db import DbBridge
from utils import hashPassword, validatePassword, getUserAddress
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError, ConnectionClosed
from responses import CONNECTED_RESPONSE, ERROR_AUTH, ERROR_USERNAME_EXIST
# Env
SERVER_WS_PORT = os.getenv('SERVER_WS_PORT', 6789)
SERVER_SK_PORT = os.getenv('SERVER_WS_PORT', 6790)
SERVER_URL = os.getenv('SERVER_URL', "127.0.0.1")
BUFFER_SIZE = 4096
# Setup logging
logging.basicConfig(filename='system.log')
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
        except ConnectionClosedOK:
          #print('Connection close')
          await websocket.close()
        except ConnectionClosedError:
          await websocket.close()
        except ConnectionClosed:
          await websocket.close()
        except:
          logging.exception("Error in ws request")
    def requestHandler(self, websocket, request):
      if request['option'] == 'message':
        _thread = threading.Thread(target=asyncio.run, args=(self.messageHandler(request),))
        _thread.start()
      elif request['option'] == 'register':
        _thread = threading.Thread(target=asyncio.run, args=(self.registerUser(websocket, request['data']),))
        _thread.start()
      elif request['option'] == 'auth':
        _thread = threading.Thread(target=asyncio.run, args=(self.auth(websocket, request['data']),))
        _thread.start()
    async def auth(self, ws, data):
      db = DbBridge()
      user = db.getOne(f"SELECT * FROM user WHERE username='{data['username']}'")
      # if user exits
      if len(user) == 3:
        user_id, _, passwordHashed = user
        if validatePassword(data['password'], passwordHashed):
          await ws.send(json.dumps({
            "status": "ok",
            "type": "authSuccessful",
            "response": {
              "address": getUserAddress(user_id),
              "user": {
                "id": user_id
              }
            }
          }))
          db.close()
        else:
          await ws.send(json.dumps(ERROR_AUTH))
      else:
        await ws.send(json.dumps(ERROR_AUTH))
    async def messageHandler(self, request):
      print(request)
    async def registerUser(self,ws, data):
      db = DbBridge()
      user_count = db.rowCount(f"SELECT * FROM user WHERE username='{data['username']}'")

      if user_count == 0:
        user_id = random.randint(0, 99999999)
        password = hashPassword(data['password']).decode()
        db.query(f"INSERT INTO user VALUES({user_id}, '{data['username']}', '{password}')")
        await ws.send(json.dumps({
          "status": "ok",
          "type": "registerSuccessful",
          "response": user_id
        }))
        db.close()
      else:
        await ws.send(json.dumps(ERROR_USERNAME_EXIST))
class SocketServer():
    def __init__(self):
        try:
          self.socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
          logging.exception('Error initializing socket service')
    def run(self):
      print('starting socket')
      logging.info("Starting Socket service")
      self.socket_instance.bind((SERVER_URL, SERVER_SK_PORT))
      self.socket_instance.listen(10)
      self.listen()
    def stop(self):
      self.socket_instance.close()
      os._exit(0)
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
        except KeyboardInterrupt:
          self.stop()
        except:
          logging.exception("Unknown error")
