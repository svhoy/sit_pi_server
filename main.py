#!/usr/bin/env python

# Standard Library
import asyncio

from contextlib import suppress

# Library
from apps.sit_api.socket import BleWebsocket
from apps.sit_ble_mesh.mesh import Mesh


def main():
    loop = asyncio.new_event_loop()
    loop2 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mesh = Mesh(loop2)
    socket = BleWebsocket(mesh)

    loop.run_until_complete(socket.connect())


if __name__ == "__main__":
    main()
