import asyncio
from metis_forza import MetisManager, Color, SensorMode

async def main():
    # 1. Lista dei MAC dei tuoi dispositivi
    macs = ["C1:A2:B3:D4:E5:F6", "D2:B3:C4:E5:F6:A7"]
    manager = MetisManager(macs)

    # 2. Definiamo cosa fare all'impatto
    def segna_punteggio(mac, tempo, forza):
        print(f"🎯 [POD {mac}] COLPITO! Tempo: {tempo}s | Forza: {forza}")

    manager.on_any_impact(segna_punteggio)

    try:
        # 3. Connessione parallela
        await manager.connect_all()

        # 4. Start (Tutti Gialli, Vibrazione Alta, con Suono)
        await manager.start_all(
            color=Color.YELLOW,
            mode=SensorMode.VIBRATION_HIGH,
            flash=True
        )

        print("In ascolto per 20 secondi...")
        await asyncio.sleep(20)

        await manager.stop_all()

    finally:
        await manager.disconnect_all()

if __name__ == "__main__":
    asyncio.run(main())