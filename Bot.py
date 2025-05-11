# DiscordBot-BestStocks\Bot.py
import re, sys, os
import asyncio
from dotenv import load_dotenv

import discord
from discord.ext import commands


# Cargar el archivo .env
load_dotenv()
# Obtener la ruta desde el archivo .env
sTOKEN = os.getenv('TOKEN')

# Inicializar bot
intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer el contenido de los mensajes
bot = commands.Bot(command_prefix="!", intents=intents)


# Evento cuando el bot está listo
@bot.event
async def on_ready():
   print(f'Bot conectado como {bot.user}')


# Cargar la extensión de comandos
async def main():
   async with bot:
      # Cargar los comandos desde el archivo MainCommands.py
      await bot.load_extension("Commands.MainCommands")
      await bot.start(sTOKEN)

if __name__ == "__main__":
   # Verificar si el token es válido
   if not sTOKEN:
      print("Error: El token no está configurado en el archivo .env.")
   else:
      asyncio.run(main())
      