import asyncio
import websockets
import sounddevice as sd
import numpy as np

# Paramètres audio
CHUNK = 1024
FORMAT = np.int16
CHANNELS = 1
RATE = 44100

# Adresse du serveur WebSocket
SERVER_URL = "ws://monserveur-production.up.railway.app"  # Lien fourni par Railway

async def send_audio(websocket):
    # Enregistrement de l'audio à partir du micro
    def callback(indata, frames, time, status):
        if status:
            print(status)
        websocket.send(indata.tobytes())

    with sd.InputStream(callback=callback, channels=CHANNELS, samplerate=RATE, dtype=FORMAT):
        await asyncio.Future()  # L'attente permet à l'audio de continuer à être enregistré

async def receive_audio(websocket):
    # Lecture audio sur le haut-parleur
    def callback(outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = np.frombuffer(data, dtype=FORMAT)

    with sd.OutputStream(callback=callback, channels=CHANNELS, samplerate=RATE, dtype=FORMAT):
        while True:
            data = await websocket.recv()
            callback(data)

async def main():
    async with websockets.connect(SERVER_URL) as websocket:
        await asyncio.gather(
            send_audio(websocket),
            receive_audio(websocket)
        )

# Exécuter l'application
asyncio.run(main())
