from fastapi.websockets import WebSocket

from app.schemas import WebsocketSendMessage


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, set[WebSocket]] = {}

    async def connect(self, name, websocket: WebSocket):

        if name not in self.rooms:
            self.rooms[name] = set()

        self.rooms[name].add(websocket)

    def disconnect(self, name, websocket: WebSocket):
        room = self.rooms.get(name)
        if room is None:
            return

        room.discard(websocket)

        if not room:
            del self.rooms[name]

    async def broadcast(self, name, message: WebsocketSendMessage):
        room = self.rooms.get(name, set())
        dead_connections = set()
        for connection in room:
            try:
                await connection.send_json(message.model_dump())
            except Exception:
                dead_connections.add(connection)
        
        for connection in dead_connections:
            self.disconnect(name, connection)