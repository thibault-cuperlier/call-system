import asyncio
import websockets
import os

# Paramètres du serveur
PORT = int(os.getenv("PORT", 5000))  # Variable d'environnement de Railway

async def handler(websocket, path):
    print(f"[✅] Client connecté : {path}")
    try:
        while True:
            data = await websocket.recv()  # Recevoir des données audio
            if not data:
                break
            await websocket.send(data)  # Répondre avec les mêmes données (audio)
    except:
        print("[⚠️] Problème avec la connexion.")

# Lancer le serveur WebSocket
start_server = websockets.serve(handler, "0.0.0.0", PORT)

# Boucle d'événements
asyncio.get_event_loop().run_until_complete(start_server)
print(f"[🎙️] Serveur WebSocket démarré sur le port {PORT}.")

# Lancer le serveur
asyncio.get_event_loop().run_forever()
