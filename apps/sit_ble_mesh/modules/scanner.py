# Standard Library
import asyncio
import logging
import logging.config

from uuid import UUID

from . import Module


LOG_CONFIG_PATH = "settings/logging.conf"

logging.config.fileConfig(LOG_CONFIG_PATH)
# create logger
logger = logging.getLogger("mesh_scanner")


class ScannerModule(Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._unprovisioned = set()

    def _scan_result(self, rssi, data, options):
        """
        The method is called from the bluetooth-meshd daemon when a
        unique UUID has been seen during UnprovisionedScan() for
        unprovsioned devices.
        """

        try:
            uuid = UUID(bytes=data[:16])
            self._unprovisioned.add(uuid)
            logger.info(f"Found unprovisioned node: {uuid}")
        except:
            logger.exception("Failed to retrieve UUID")

    async def handle_cli(self, args=None):
        await self.scan()
        # print user friendly results
        print(self._unprovisioned)
        print(f"\nFound {len(self._unprovisioned)} nodes:")
        for uuid in self._unprovisioned:
            print(f"\t{uuid}")

        return self._unprovisioned

    async def scan(self):
        logger.info("Scanning for unprovisioned devices...")

        await self.app.management_interface.unprovisioned_scan(seconds=10)
        await asyncio.sleep(10.0)
