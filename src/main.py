import multiprocessing
from db import DbBridge
from comunications import SocketServer, WebsocketServer


if __name__ == "__main__":
    db = DbBridge()
    db.initDB()
    connectionsClients = {}
    socket = SocketServer(connectionsClients)
    websocket = WebsocketServer(connectionsClients)
    try:
        # creating processes
        socketProcess = multiprocessing.Process(target=socket.run, args=())
        websocketProcess = multiprocessing.Process(
            target=websocket.run, args=())
        db.close()
        # starting process 1
        socketProcess.start()
        # starting process 2
        websocketProcess.start()

        # wait until process 1 is finished
        socketProcess.join()
        # wait until process 2 is finished
        websocketProcess.join()
    except KeyboardInterrupt:
        socket.stop()
