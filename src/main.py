import multiprocessing

from comunications import SocketServer, WebsocketServer

if __name__ == "__main__":
  socket = SocketServer()
  websocket = WebsocketServer()
  # creating processes
  socketProcess = multiprocessing.Process(target=socket.run, args=( ))
  websocketProcess = multiprocessing.Process(target=websocket.run, args=( ))

  # starting process 1
  socketProcess.start()
  # starting process 2
  websocketProcess.start()

  # wait until process 1 is finished
  socketProcess.join()
  # wait until process 2 is finished
  websocketProcess.join()
  # both processes finished
  print("Done!")