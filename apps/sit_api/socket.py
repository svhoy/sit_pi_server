# Standard Library
import asyncio
import json

# Third Party
import websockets

from .auth import Authenticator


HOST = "127.0.0.1"
PORT = 5500


class BleSocket:
    def __init__(self) -> None:
        # self._auth = Authenticator()
        # self._auth.login()
        pass

    async def hello(self):
        uri = "ws://127.0.0.1:5500/ws/ble-scan/"
        async for websocket in websockets.connect(uri):
            try:
                # Close the connection when receiving SIGTERM.
                loop = asyncio.get_running_loop()

                # Process messages received on the connection.
                async for text_data in websocket:
                    data = json.loads(text_data)
                    print(data)
                    if data["scan"]["state"]:
                        await self.scan()
                        await websocket.send(
                            json.dumps(
                                {
                                    "type": "scanning_state",
                                    "scan": {
                                        "state": False,
                                        "message": "Scan Completed",
                                    },
                                }
                            )
                        )

            except websockets.ConnectionClosedError as e:
                print(e)
                print("Connection is closed, try reconnect")
                continue

    async def scan(self):
        await asyncio.sleep(10)
