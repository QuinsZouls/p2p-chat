import asyncio
import socket
import json
import logging
import websockets
import os
import threading
import random
from websocket import create_connection
from urllib import request
from db import DbBridge
from utils import hashPassword, validatePassword, getUserAddress, normalizeContacts, decodeUserAddress, normalizeChats, normalizeMessages, getDataUriPathImage
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError, ConnectionClosed
from responses import CONNECTED_RESPONSE, ERROR_AUTH, ERROR_USERNAME_EXIST, ERROR_CONTACT_EXITS
# Env
SERVER_WS_PORT = int(os.getenv('SERVER_WS_PORT', 6789))
SERVER_SK_PORT = int(os.getenv('SERVER_SK_PORT', 6790))
SERVER_URL = os.getenv('SERVER_URL', "127.0.0.1")
BUFFER_SIZE = 4096
# Setup logging
logging.basicConfig(filename='system.log')


class WebsocketServer():
    def __init__(self, connections):
        self.connections = connections
    # Start asyncio process

    def run(self, ):
        print('starting Websocket')
        logging.info("Starting Websocket service")
        server = websockets.serve(self.listen, SERVER_URL, SERVER_WS_PORT)
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
    # Main handler

    def requestHandler(self, websocket, request):
        if request['option'] == 'message':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.messageHandler(websocket, request['data']),))
            _thread.start()
            _thread.join()
        elif request['option'] == 'register':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.registerUser(websocket, request['data']),))
            _thread.start()
            _thread.join()
        elif request['option'] == 'auth':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.auth(websocket, request['data']),))
            _thread.start()
            _thread.join()
        elif request['option'] == 'connect':
            self.connections[str(request['data'])] = websocket
        elif request['option'] == 'disconnect':
            del self.connections[str(request['data'])]
        elif request['option'] == 'add-contact':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.addContact(websocket, request['data']),))
            _thread.start()
            _thread.join()
        elif request['option'] == 'get-contacts':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.getContacts(websocket, request['data']),))
            _thread.start()
            _thread.join()
        elif request['option'] == 'communication-request':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.enableComunication(websocket, request['data']),))
            _thread.start()
            _thread.join()
        elif request['option'] == 'accept-communication-request':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.acceptCommunication(websocket, request['data']),))
            _thread.start()
            _thread.join()
        elif request['option'] == 'get-chats':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.getChats(websocket, request['data']),))
            _thread.start()
            _thread.join()
        elif request['option'] == 'incoming-message':
            _thread = threading.Thread(target=asyncio.run, args=(
                self.incomingMessage(websocket, request['data']),))
            _thread.start()
            _thread.join()

    async def auth(self, ws, data):
        db = DbBridge()
        user = db.getOne(
            f"SELECT * FROM user WHERE username='{data['username']}'")
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
                            "id": user_id,
                            "username": data['username']
                        }
                    }
                }))
                db.close()
            else:
                await ws.send(json.dumps(ERROR_AUTH))
        else:
            await ws.send(json.dumps(ERROR_AUTH))

    async def messageHandler(self, ws, data):
        db = DbBridge()
        destination = decodeUserAddress(data['to'])
        author = decodeUserAddress(data['from'])
        attachment = 0
        if 'attachment' in data:
            attachment, _ = self.saveImage(
                data['attachment'], author['user'])
        # Generamos la conversación para el anfitrion
        if data['create_chat']:
            messageId = random.randint(0, 99999999)
            chat_id = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO chat VALUES({chat_id}, '{author['user']}', '{data['contact_id']}'  )")
            db.query(
                f"INSERT INTO message VALUES({messageId}, '{data['content']}', {attachment}, '{author['user']}', {data['created_at']}, {chat_id} )")
        else:
            messageId = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO message VALUES({messageId}, '{data['content']}', {attachment}, '{author['user']}', {data['created_at']}, {data['chat_id']} )")
        contact = db.getOne(
            f"SELECT * FROM contact WHERE user_id={author['user']} and destination='{data['to']}'")
        chat_id_foreing = db.getOne(
            f"SELECT * FROM chat WHERE user_id={author['user']} and contact_id={contact[0]}")
        if chat_id_foreing == None:
            # Creamos el chat
            chat_id = random.randint(0, 99999999)
            messageId = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO chat VALUES({chat_id}, '{destination['user']}', '{contact[0]}'  )")
            db.query(
                f"INSERT INTO message VALUES({messageId}, '{data['content']}', {attachment}, '{author['user']}', {data['created_at']}, {chat_id} )")
        else:
            messageId = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO message VALUES({messageId}, '{data['content']}', {attachment}, '{author['user']}', {data['created_at']}, {chat_id_foreing[0]} )")
        db.close()
        if destination['ip'] == SERVER_URL and str(destination['port']) == str(SERVER_SK_PORT):
            try:
                if self.connections[str(destination['user'])] != None:
                    data['user_id'] = destination['user']
                    await self.getChats(self.connections[str(destination['user'])], data)
            except KeyError:
                logging.info('El usuario no esta disponible')

            data['user_id'] = author['user']
            await self.getChats(ws, data)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to foreing node
            s.connect((destination['ip'], int(destination['port'])))

            s.sendall(json.dumps({
                "option": "message",
                "data": data
            }).encode())

            await self.getChats(self.connections[str(author['user'])], {
                "user_id":  author['user']
            })

    async def registerUser(self, ws, data):
        db = DbBridge()
        user_count = db.rowCount(
            f"SELECT * FROM user WHERE username='{data['username']}'")

        if user_count == 0:
            user_id = random.randint(0, 99999999)
            password = hashPassword(data['password']).decode()
            db.query(
                f"INSERT INTO user VALUES({user_id}, '{data['username']}', '{password}')")
            await ws.send(json.dumps({
                "status": "ok",
                "type": "registerSuccessful",
                "response": user_id
            }))
            db.close()
        else:
            await ws.send(json.dumps(ERROR_USERNAME_EXIST))

    async def addContact(self, ws, data):
        db = DbBridge()
        contact_count = db.rowCount(
            f"SELECT * FROM contact WHERE destination='{data['address']}' and user_id='{data['user_id']}'")
        if contact_count == 0:
            contact_id = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO contact VALUES({contact_id},'{data['label']}', '{data['address']}', '{data['user_id']}', 0)")
            await ws.send(json.dumps({
                "status": "ok",
                "type": "addContactSuccessful",
                "response": contact_id
            }))
            db.close()
            return contact_id
        else:
            await ws.send(json.dumps(ERROR_CONTACT_EXITS))

    async def getContacts(self, ws, data):
        db = DbBridge()
        records = db.getAll(
            f"SELECT c.id, c.label, c.destination, c.status, r.id FROM contact c LEFT JOIN chat r ON c.id = r.contact_id WHERE c.user_id='{data['user_id']}'")
        await ws.send(json.dumps({
            "status": "ok",
            "type": "getContactSuccessful",
            "response": normalizeContacts(records)
        }))
        db.close()

    async def enableComunication(self, ws, data):
        origin = decodeUserAddress(data['destination'])
        if origin['ip'] == SERVER_URL and str(origin['port']) == str(SERVER_SK_PORT):
            try:
                if self.connections[str(origin['user'])] != None:
                    print('El usuario esta connectado')
                    await self.connections[str(origin['user'])].send(json.dumps({
                        "status": "ok",
                        "type": "connectionRequest",
                        "response": data['from']
                    }))
            except KeyError:
                print('El usuario no esta disponible')
        else:
            # TODO crear conexión hacia el socket destino
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to foreing node
            s.connect((origin['ip'], int(origin['port'])))

            s.send(json.dumps({
                "option": "enable-communiaction",
                "data": data
            }).encode())
            print("Mensaje enviado")

    async def acceptCommunication(self, ws, data):
        db = DbBridge()
        origin = decodeUserAddress(data['user_address'])
        target = decodeUserAddress(data['address'])  # Dirección de destino
        data['user_id'] = origin['user']
        db.query(
            f"UPDATE contact SET status = 1 WHERE id = {data['contact_id']} ")

        contact_id = await self.addContact(ws, data)
        db.query(f"UPDATE contact SET status = 1 WHERE id = {contact_id} ")
        db.close()
        if target['ip'] == SERVER_URL and str(target['port']) == str(SERVER_SK_PORT):
            try:
                if self.connections[str(target['user'])] != None:
                    data['user_id'] = target['user']
                    await self.connections[str(target['user'])].send(json.dumps({
                        "status": "ok",
                        "type": "connectionRequestAccepted",
                        "response": "Se ha aceptado la solicitud de comunicación"
                    }))
                    await self.getContacts(self.connections[str(target['user'])], data)
            except KeyError:
                logging.info('El usuario no esta disponible')
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to foreing node
            s.connect((target['ip'], int(target['port'])))

            s.send(json.dumps({
                "option": "accept-communication-request",
                "data": data
            }).encode())
            print("Mensaje enviado")

    async def getChats(self, ws, data):
        db = DbBridge()
        records = db.getAll(
            f"SELECT r.id, c.label, c.destination FROM chat r LEFT JOIN contact c ON c.id = r.contact_id WHERE r.user_id='{data['user_id']}'")
        chats = normalizeChats(records)
        for chat in chats:
            messages = db.getAll(
                f"SELECT * FROM message WHERE chat_id={chat['id']} ORDER BY created_at")
            chat['messages'] = normalizeMessages(messages)
            for msg in chat['messages']:
                if msg['attachment'] != 0:
                    multimedia = db.getOne(
                        f"SELECT path, type FROM multimedia WHERE id={msg['attachment']}")
                    msg['multimedia'] = getDataUriPathImage(
                        multimedia[0], multimedia[1])
        await ws.send(json.dumps({
            "status": "ok",
            "type": "getChatsSuccessful",
            "response": chats
        }))
        db.close()

    def saveImage(self, attachment, user_id):
        extension = '.png'
        multimedia_id = random.randint(0, 99999999)
        db = DbBridge()
        if attachment['type'] == 'image/jpg':
            extension = '.jpg'
        path = f"./multimedia/{attachment['id']}{extension}"
        response = request.urlopen(attachment['raw'])
        with open(path, 'wb') as f:
            f.write(response.file.read())
            f.close()
        db.query(
            f"INSERT INTO multimedia VALUES({multimedia_id}, '{attachment['type']}', '{attachment['size']}', {user_id}, {attachment['id']}, '{path}')")
        db.close()
        return multimedia_id, path

    async def incomingMessage(self, data):
        try:
            if self.connections[str(data['user_id'])] != None:
                await self.getChats(self.connections[str(data['user_id'])], data)
        except KeyError:
            logging.info('El usuario no esta disponible')


class SocketServer():
    def __init__(self, connections):
        self.connections = connections
        try:
            self.socket_instance = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        except:
            logging.exception('Error initializing socket service')

    def run(self):
        print('starting socket')
        logging.info("Starting Socket service")
        self.socket_instance.bind((SERVER_URL, SERVER_SK_PORT))
        self.socket_instance.listen(100)
        self.listen()

    def stop(self):
        self.socket_instance.close()
        os._exit(0)

    def recvFile(self, client, data, user_id):
        extension = '.png'
        multimedia_id = random.randint(0, 99999999)
        db = DbBridge()
        if data['type'] == 'image/jpg':
            extension = '.jpg'
        path = f"./multimedia/{data['id']}{extension}"
        response = request.urlopen(data['raw'])
        with open(path, 'wb') as f:
            f.write(response.file.read())
            f.close()
        client.close()
        db.query(
            f"INSERT INTO multimedia VALUES({multimedia_id}, '{data['type']}', '{data['size']}', {user_id}, {data['id']}, '{path}')")
        db.close()
        return multimedia_id

    async def handleMessage(self, client, data):
        db = DbBridge()
        destination = decodeUserAddress(data['to'])
        author = decodeUserAddress(data['from'])
        attachment = 0
        if 'attachment' in data:
            attachment = self.recvFile(
                client, data['attachment'], author['user'])
        # Generamos la conversación para el anfitrion
        if data['create_chat']:
            messageId = random.randint(0, 99999999)
            chat_id = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO chat VALUES({chat_id}, '{author['user']}', '{data['contact_id']}'  )")
            db.query(
                f"INSERT INTO message VALUES({messageId}, '{data['content']}', {attachment}, '{author['user']}', {data['created_at']}, {chat_id} )")
        else:
            messageId = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO message VALUES({messageId}, '{data['content']}', {attachment}, '{author['user']}', {data['created_at']}, {data['chat_id']} )")
        contact = db.getOne(
            f"SELECT * FROM contact WHERE user_id={destination['user']} and destination='{data['to']}'")
        chat_id_foreing = db.getOne(
            f"SELECT * FROM chat WHERE user_id={destination['user']} and contact_id={contact[0]}")
        if chat_id_foreing == None:
            # Creamos el chat
            chat_id = random.randint(0, 99999999)
            messageId = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO chat VALUES({chat_id}, '{destination['user']}', '{contact[0]}'  )")
            db.query(
                f"INSERT INTO message VALUES({messageId}, '{data['content']}', {attachment}, '{author['user']}', {data['created_at']}, {chat_id} )")
        else:
            messageId = random.randint(0, 99999999)
            db.query(
                f"INSERT INTO message VALUES({messageId}, '{data['content']}', {attachment}, '{author['user']}', {data['created_at']}, {chat_id_foreing[0]} )")
        db.close()

        try:
            ws_client = create_connection(
                f"ws://{SERVER_URL}:{SERVER_WS_PORT}/")
            ws_client.send(json.dumps({
                "option": "incoming-message",
                "data": {
                    "user_id": destination['user']
                }
            }))
            ws_client.close()
            client.close()
        except KeyError:
            logging.info('El usuario no esta disponible')

    async def enableComunication(self, client, data):
        try:
            ws_client = create_connection(
                f"ws://{SERVER_URL}:{SERVER_WS_PORT}/")
            ws_client.send(json.dumps({
                "option": "communication-request",
                "data": data
            }))
            ws_client.close()
            client.close()
        except KeyError:
            logging.info('El usuario no esta disponible')

    async def acceptCommunicationRequest(self, client, data):
        try:
            ws_client = create_connection(
                f"ws://{SERVER_URL}:{SERVER_WS_PORT}/")
            ws_client.send(json.dumps({
                "option": "accept-communication-request",
                "data": data
            }))
            ws_client.close()
            client.close()
        except KeyError:
            logging.info('El usuario no esta disponible')

    def listen(self):
        while True:
            try:
                # accept connections from outside
                (clientsocket, address) = self.socket_instance.accept()
                # now do something with the clientsocket
                # in this case, we'll pretend this is a threaded server
                request = clientsocket.recv(BUFFER_SIZE).decode()
                parsedReq = json.loads(request)
                print(parsedReq)
                if parsedReq['option'] == 'message':
                    # Process menssage
                    _thread = threading.Thread(target=asyncio.run, args=(
                        self.handleMessage(clientsocket, parsedReq['data']),))
                    _thread.start()
                    _thread.join()
                elif parsedReq['option'] == 'enable-communiaction':
                    _thread = threading.Thread(target=asyncio.run, args=(
                        self.enableComunication(clientsocket, parsedReq['data']),))
                    _thread.start()
                    _thread.join()
                elif parsedReq['option'] == 'accept-communication-request':
                    _thread = threading.Thread(target=asyncio.run, args=(
                        self.acceptCommunicationRequest(clientsocket, parsedReq['data']),))
                    _thread.start()
                    _thread.join()

            except KeyboardInterrupt:
                self.stop()
            except:
                logging.exception("Unknown error")
