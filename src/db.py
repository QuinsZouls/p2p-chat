import sqlite3
from sqlite3 import Error

class DbBridge:
  def __init__(self):
    try:
      self.connection = sqlite3.connect('main.db')
    except Error:
      print(Error)
  def initDB(self):
    cursor = self.connection.cursor()
    #Creamos la tabla para los usuarios
    cursor.execute("CREATE TABLE IF NOT EXISTS user(id integer PRIMARY KEY, username text, password text)")
    #Creamos la tabla para los contactos
    cursor.execute("CREATE TABLE IF NOT EXISTS contact(id integer PRIMARY KEY, label text, destination text, user_id integer, status integer)")
    #Creamos la tabla para los chats
    cursor.execute("CREATE TABLE IF NOT EXISTS chat(id integer PRIMARY KEY, user_id integer, contact_id integer)")
    #Creamos la tabla de multimedia
    cursor.execute("CREATE TABLE  IF NOT EXISTS multimedia(id integer PRIMARY KEY, type text, size integer, user_id integer, created_at integer, path text)")
    #Creamos la tabla para los mensajes
    cursor.execute("CREATE TABLE IF NOT EXISTS message(id integer PRIMARY KEY, content text, attachment integer, author integer, created_at integer, chat_id text)")
    #Apply changes
    self.connection.commit()
  def query(self, statement):
    cursor = self.connection.cursor()
    cursor.execute(statement)
    self.connection.commit()
  def getOne(self, statement):
    cursor = self.connection.cursor()
    cursor.execute(statement)
    return cursor.fetchone()
  def getAll(self, statement):
    cursor = self.connection.cursor()
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows
  def rowCount(self, statement):
    cursor = self.connection.cursor()
    cursor.execute(statement)
    rows = cursor.fetchall()
    return len(rows)
  def close(self):
    self.connection.close()
