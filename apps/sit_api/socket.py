# Standard Library
import asyncio
import json

# Third Party
import websockets


HOST = "ws://192.168.0.101:8000/"


class BleWebsocket:
    def __init__(self, mesh) -> None:
        # self._auth = Authenticator()
        # self._auth.login()
        self.mesh = mesh

    async def connect(self):
        uri = HOST + "ws/ble-scan/"
        async for websocket in websockets.connect(uri):
            try:
                # Process messages received on the connection.
                async for text_data in websocket:
                    data = json.loads(text_data)
                    if data["scan"]["state"]:
                        unprovisioned = await self.scan()
                        lst = list(unprovisioned)
                        lst = [str(i) for i in lst]
                        await websocket.send(
                            json.dumps(
                                {
                                    "type": "scanning_state",
                                    "scan": {
                                        "state": False,
                                        "message": "Scan Completed",
                                        "unprovisioned": lst,
                                    },
                                }
                            )
                        )

            except websockets.ConnectionClosedError as e:
                print(e)
                print("Connection is closed, try reconnect")
                continue

    async def scan(self):
        return await self.mesh.scan()
