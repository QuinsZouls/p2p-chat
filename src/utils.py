import bcrypt
import os
from cryptography.fernet import Fernet

FERNET_KEY = os.getenv('FERNET_KEY', Fernet.generate_key())
SERVER_SK_PORT = os.getenv('SERVER_WS_PORT', 6790)
HOST = os.getenv('HOST', '127.0.0.1')

def hashPassword(password):
  return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def validatePassword(password, hashedpassword):
  return bcrypt.checkpw(password.encode(), hashedpassword.encode())

def getUserAddress(user_id):
  fernet = Fernet(FERNET_KEY)
  address = f"{user_id};{HOST};{SERVER_SK_PORT}"
  return fernet.encrypt(address.encode()).decode()
