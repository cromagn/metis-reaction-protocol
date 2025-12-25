import asyncio
import logging
from enum import IntEnum
from typing import Callable, Optional
from bleak import BleakClient

logger = logging.getLogger(__name__)


class Color(IntEnum):
    RED = 0x00
    YELLOW = 0x01
    BLUE = 0x02
    GREEN = 0x03


class SensorMode(IntEnum):
    PROXIMITY_CLOSE = 0x00
    PROXIMITY_FAR = 0x01
    VIBRATION_LOW = 0x02
    VIBRATION_HIGH = 0x03


class MetisClient:
    CMD_HANDLE = 0x0003
    NOTIF_HANDLE = 0x0005

    def __init__(self, address: str):
        self.address = address
        self.client: Optional[BleakClient] = None
        self._keep_alive_task: Optional[asyncio.Task] = None
        self._impact_callback: Optional[Callable[[str, float, int], None]] = None

    def set_impact_callback(self, callback: Callable[[str, float, int], None]):
        self._impact_callback = callback

    async def _notification_handler(self, sender, data):
        if data and data[0] == 0x03 and len(data) >= 4:
            reaction_time = data[2] / 100.0
            force = data[3]
            if self._impact_callback:
                self._impact_callback(self.address, reaction_time, force)

    async def connect(self):
        logger.info(f"Connessione a {self.address}...")
        self.client = BleakClient(self.address)
        await self.client.connect()
        await self.client.start_notify(self.NOTIF_HANDLE, self._notification_handler)
        self._keep_alive_task = asyncio.create_task(self._run_keep_alive())
        logger.info(f"Dispositivo {self.address} pronto.")

    async def _run_keep_alive(self):
        try:
            while self.client and self.client.is_connected:
                await self.client.write_gatt_char(self.CMD_HANDLE, bytearray([0x20]), response=False)
                await asyncio.sleep(3)
        except asyncio.CancelledError:
            pass

    async def init_drill(self, color: Color = Color.RED, mode: SensorMode = SensorMode.PROXIMITY_CLOSE,
                         flash: bool = False, sound: bool = True, start_snd: bool = False):
        config_byte = 0x01
        config_byte |= (mode.value << 6)
        config_byte |= (0x20 if flash else 0x00)
        config_byte |= (0x00 if sound else 0x10)  # Logica invertita
        config_byte |= (0x08 if start_snd else 0x00)
        config_byte |= (color.value << 1)

        await self.client.write_gatt_char(self.CMD_HANDLE, bytearray([0x02, config_byte]), response=False)

    async def stop(self):
        await self.client.write_gatt_char(self.CMD_HANDLE, bytearray([0x04, 0x05]), response=False)
        await asyncio.sleep(0.05)
        await self.client.write_gatt_char(self.CMD_HANDLE, bytearray([0x05]), response=False)

    async def disconnect(self):
        if self._keep_alive_task:
            self._keep_alive_task.cancel()
        if self.client:
            await self.client.disconnect()