import bcrypt
import os
import base64
from cryptography.fernet import Fernet

FERNET_KEY = os.getenv('FERNET_KEY', Fernet.generate_key())
SERVER_SK_PORT = int(os.getenv('SERVER_SK_PORT', 6790))
HOST = os.getenv('HOST', '127.0.0.1')


def hashPassword(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validatePassword(password, hashedpassword):
    return bcrypt.checkpw(password.encode(), hashedpassword.encode())


def getUserAddress(user_id):
    fernet = Fernet(FERNET_KEY)
    address = f"{user_id};{HOST};{SERVER_SK_PORT}"
    return fernet.encrypt(address.encode()).decode()


def decodeUserAddress(address):
    fernet = Fernet(FERNET_KEY)
    origin = fernet.decrypt(address.encode()).decode().split(';')
    return {
        "user": origin[0],
        "ip": origin[1],
        "port": origin[2]
    }


def normalizeContacts(contacts):
    newContacts = []
    for contact in contacts:
        newContacts.append({
            "id": contact[0],
            "label": contact[1],
            "destination": contact[2],
            "status": contact[3],
            "chat_id": contact[4]
        })
    return newContacts


def normalizeChats(chats):
    newRecords = []
    for chat in chats:
        newRecords.append({
            "id": chat[0],
            "label": chat[1],
            "destination": chat[2],
        })
    return newRecords


def normalizeMessages(messages):
    newRecords = []
    for message in messages:
        newRecords.append({
            "id": message[0],
            "content": message[1],
            "attachment": message[2],
            "author": message[3],
            "created_at": message[4],
        })
    return newRecords


def getDataUriPathImage(path, type):
    with open(path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    text = f"data:{type};base64,{b64_string.decode('utf-8')}"
    return text
