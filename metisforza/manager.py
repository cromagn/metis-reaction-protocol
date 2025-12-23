import asyncio
import logging
from typing import List, Dict, Callable, Optional
from .client import MetisClient, Color, SensorMode

logger = logging.getLogger(__name__)

class MetisManager:
    def __init__(self, addresses: List[str]):
        self.devices: Dict[str, MetisClient] = {addr: MetisClient(addr) for addr in addresses}

    def on_any_impact(self, callback: Callable[[str, float, int], None]):
        """Imposta la stessa funzione di callback per tutti i dispositivi."""
        for device in self.devices.values():
            device.set_impact_callback(callback)

    async def connect_all(self):
        logger.info(f"Tentativo di connessione a {len(self.devices)} dispositivi...")
        await asyncio.gather(*(d.connect() for d in self.devices.values()))

    async def start_all(self, **kwargs):
        """Invia il comando di init a tutti i dispositivi (accetta i parametri di init_drill)."""
        await asyncio.gather(*(d.init_drill(**kwargs) for d in self.devices.values()))

    async def stop_all(self):
        await asyncio.gather(*(d.stop() for d in self.devices.values()))

    async def disconnect_all(self):
        await asyncio.gather(*(d.disconnect() for d in self.devices.values()))