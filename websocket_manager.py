from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.active_connections = []


    async def connect(self, websocket: WebSocket):

        await websocket.accept()

        self.active_connections.append(websocket)

        print("Client Connected")


    def disconnect(self, websocket: WebSocket):

        self.active_connections.remove(websocket)

        print("Client Disconnected")


    async def broadcast(self, data):

        print("Broadcasting:", data)

        for connection in self.active_connections:

            await connection.send_json(data)


manager = ConnectionManager()