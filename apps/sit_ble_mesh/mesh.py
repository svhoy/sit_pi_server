# Standard Library
import logging
import logging.config
import secrets

from contextlib import AsyncExitStack, asynccontextmanager

# Third Party
from bluetooth_mesh.application import Application, Element
from bluetooth_mesh.crypto import NetworkKey
from bluetooth_mesh.messages.config import GATTNamespaceDescriptor

from .modules.scanner import ScannerModule


LOG_CONFIG_PATH = "settings/logging.conf"

logging.config.fileConfig(LOG_CONFIG_PATH)
# create logger
logger = logging.getLogger("SIT_Mesh")

MESH_MODULES = {
    "scan": ScannerModule(),
}


class MainElement(Element):
    """
    Represents the main element of the application node
    """

    LOCATION = GATTNamespaceDescriptor.MAIN
    MODELS = []


class Mesh(Application):
    COMPANY_ID = 0x05F1  # The Linux Foundation
    PRODUCT_ID = 1
    VERSION_ID = 1
    ELEMENTS = {
        0: MainElement,
    }
    CRPL = 32768
    PATH = "/org/sit/mesh"

    def __init__(self, loop):
        super().__init__(loop)

        self._primary_net_key = None

        for name, module in MESH_MODULES.items():
            module.initialize(self)

        self._initialize()

    def _generte_key(self, key_dict, name):
        logger.info(f"Generate new {name}")
        key_dict[name] = secrets.token_hex(16)
        try:
            return bytes.fromhex(key_dict[name])
        except:
            raise Exception("Invalid device key")

    def _initialize(self):
        key_dict = {}

        self.address = 1

        self._primary_net_key = NetworkKey(
            self._generte_key(key_dict, "network_key")
        )

    @property
    def primary_net_key(self):
        if not self._primary_net_key:
            raise Exception("Primary network key not ready")
        return 0, self._primary_net_key

    def scan_result(self, rssi, data, options):
        MESH_MODULES["scan"]._scan_result(rssi, data, options)

    async def scan(self):
        async with AsyncExitStack() as stack:

            # connect to daemon
            await stack.enter_async_context(self)
            await self.connect()
            unprovisioned = await MESH_MODULES["scan"].handle_cli()

        return unprovisioned

    async def run(self, args):
        async with AsyncExitStack() as stack:

            # connect to daemon
            await stack.enter_async_context(self)
            await self.connect()
            print("Test")
            if "handler" in args:
                await args.handler(args)
                return
            else:
                print(args)
