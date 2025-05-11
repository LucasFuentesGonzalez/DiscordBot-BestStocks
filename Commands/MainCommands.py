# DiscordBot-BestStocks\Commands\MainCommands.py
import sys, os, re, io
import pandas as pd
import unicodedata
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Ajustar el path para permitir imports entre carpetas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Commands.UtilsCommands import *


# Cargar el archivo .env
load_dotenv()
# Obtener la ruta desde el archivo .env
sRUTA_EXCEL = os.getenv('RUTA_EXCEL')

# Cargar los datos
try:
   df = pd.read_excel(sRUTA_EXCEL)
except Exception as e:
   print(f"Error al cargar el archivo Excel: {e}")


# Comando: Obtener información de una acción
@commands.command()
async def accion(ctx, ticker: str):
   row = df[df["Ticker"].str.upper() == ticker.upper()]
   if row.empty:
      await ctx.send(f"Ticker `{ticker}` no encontrado.")
      return
   info = row.iloc[0]
   embed = crear_tarjeta_inversion(
            info,
            titulo="📌 Acción buscada",
            descripcion="Información detallada")
   await ctx.send(embed=embed)


# Comando: Top 5 acciones mejor calificadas
@commands.command()
async def mejores(ctx):
   top = df.sort_values(by="Puntuación", ascending=False).head(5)
   for i, (_, row) in enumerate(top.iterrows(), start=1):
      embed = crear_tarjeta_inversion(
               row,
               titulo=f"🏆 Top {i}",
               descripcion="Datos destacados de inversión",
               color=0x00cc99)
      await ctx.send(embed=embed)


# Comando: Buscar por campo
@commands.command()
async def buscar(ctx, campo: str, *, valor: str):
   # Normalizar directamente los nombres de las columnas y el campo ingresado
   columnas_norm = {''.join(c for c in unicodedata.normalize('NFKD', col) if not unicodedata.combining(c)).lower(): col for col in df.columns}
   campo_normalizado = ''.join(c for c in unicodedata.normalize('NFKD', campo) if not unicodedata.combining(c)).lower()

   # Verificar si hay coincidencia
   if campo_normalizado not in columnas_norm:
      await ctx.send(f"Campo `{campo}` no válido. Intenta con uno de estos: {', '.join(df.columns)}")
      return

   columna_real = columnas_norm[campo_normalizado]

   # Buscar resultados
   resultado = df[df[columna_real].astype(str).str.contains(valor, case=False, na=False)]
   if resultado.empty:
      await ctx.send("No se encontraron resultados.")
      return

   for i, (_, row) in enumerate(resultado.head(5).iterrows(), start=1):
      embed = crear_tarjeta_inversion(
               row,
               titulo=f"🔎 {i}º Resultado de búsqueda",
               descripcion=f"Coincidencia en **{columna_real}**: `{valor}`",
               color=0x9933ff)
      await ctx.send(embed=embed)


# Comando: Infravaloradas (Precio < Valor Intrínseco)
@commands.command()
async def infravaloradas(ctx):
   resultado = df[df['Precio ($)'] < df['Valor Intrínseco ($)']]
   if resultado.empty:
      await ctx.send("No se encontraron acciones infravaloradas.")
      return

   for i, (_, row) in enumerate(resultado.head(5).iterrows(), start=1):
      # Calcular la diferencia entre el Precio y el Valor Intrínseco
      diferencia = row['Valor Intrínseco ($)'] - row['Precio ($)']
      
      embed = crear_tarjeta_inversion(
         row,
         titulo=f"📉 {i}º Acción Infravalorada",
         descripcion=f"Precio actual: ${row['Precio ($)']} \n Valor intrínseco: ${row['Valor Intrínseco ($)']} \n Diferencia: ${diferencia:.2f}",
         color=0x2ecc71)
      await ctx.send(embed=embed)


# Comando: Sobrevaloradas
@commands.command()
async def sobrevaloradas(ctx):
   resultado = df[df['Precio ($)'] > df['Valor Intrínseco ($)']]
   if resultado.empty:
      await ctx.send("No se encontraron acciones sobrevaloradas.")
      return

   for i, (_, row) in enumerate(resultado.head(5).iterrows(), start=1):
      # Calcular la diferencia entre el Precio y el Valor Intrínseco
      diferencia = row['Precio ($)'] - row['Valor Intrínseco ($)']
      
      embed = crear_tarjeta_inversion(
         row,
         titulo=f"📈 {i}º Acción Sobrevalorada",
         descripcion=f"Precio actual: ${row['Precio ($)']} \n Valor intrínseco: ${row['Valor Intrínseco ($)']} \n Diferencia: ${diferencia:.2f}",
         color=0xe74c3c)
      await ctx.send(embed=embed)


# Comando: Baratas (bajo P/E o PEG)
@commands.command()
async def baratas(ctx):
   resultado = df.sort_values(by=['P/E', 'PEG']).head(5)
   if resultado.empty:
      await ctx.send("No se encontraron acciones baratas.")
      return

   for i, (_, row) in enumerate(resultado.iterrows(), start=1):
      embed = crear_tarjeta_inversion(
               row,
               titulo=f"💰 {i}º Acción Barata",
               descripcion=f"P/E: {row['P/E']} \n PEG: {row['PEG']}",
               color=0xf1c40f)
      await ctx.send(embed=embed)


# Comando: Dividendos
@commands.command()
async def dividendos(ctx):
   resultado = df[df['Dividend Yield (%)'] > 4.0].sort_values(by='Dividend Yield (%)', ascending=False)
   if resultado.empty:
      await ctx.send("No se encontraron acciones con buenos dividendos.")
      return

   for i, (_, row) in enumerate(resultado.head(5).iterrows(), start=1):
      embed = crear_tarjeta_inversion(
               row,
               titulo=f"💸 {i}º Acción con Buen Dividendo",
               descripcion=f"Dividend Yield: {row['Dividend Yield (%)']}%",
               color=0x3498db)
      await ctx.send(embed=embed)


# Comando: Crecimiento
@commands.command()
async def crecimiento(ctx):
   resultado = df[df['Crecimiento de Ingresos (%)'] > 20].sort_values(by='Crecimiento de Ingresos (%)', ascending=False)
   if resultado.empty:
      await ctx.send("No se encontraron acciones con alto crecimiento.")
      return

   for i, (_, row) in enumerate(resultado.head(5).iterrows(), start=1):
      embed = crear_tarjeta_inversion(
               row,
               titulo=f"📈 {i}º Acción con Alto Crecimiento",
               descripcion=f"Crecimiento de Ingresos: {row['Crecimiento de Ingresos (%)']}%",
               color=0x8e44ad)
      await ctx.send(embed=embed)


# Comando: Comparar 2 acciones
@commands.command()
async def comparar(ctx, ticker1: str, ticker2: str):
   r1 = df[df['Ticker'].str.upper() == ticker1.upper()]
   r2 = df[df['Ticker'].str.upper() == ticker2.upper()]
   
   if r1.empty or r2.empty:
      await ctx.send("Uno o ambos tickers no fueron encontrados.")
      return

   info1 = r1.iloc[0]
   info2 = r2.iloc[0]

   # Crear tarjetas de inversión para ambos tickers
   embed1 = crear_tarjeta_inversion(
            info1,
            titulo=f"📊 Comparación: {ticker1.upper()}",
            descripcion="Datos del primer ticker",
            color=0x1abc9c)

   embed2 = crear_tarjeta_inversion(
            info2,
            titulo=f"📊 Comparación: {ticker2.upper()}",
            descripcion="Datos del segundo ticker",
            color=0xe67e22)

   await ctx.send(embed=embed1)
   await ctx.send(embed=embed2)


# Comando: ROE alto
@commands.command()
async def toproe(ctx):
   resultado = df.sort_values(by='ROE (%)', ascending=False).head(5)
   if resultado.empty:
      await ctx.send("No se encontraron acciones con buen ROE.")
      return

   for i, (_, row) in enumerate(resultado.iterrows(), start=1):
      embed = crear_tarjeta_inversion(
               row,
               titulo=f"📊 {i}º Top ROE",
               descripcion=f"ROE: {row['ROE (%)']}%",
               color=0x1abc9c)
      await ctx.send(embed=embed)


# Comando: Beta baja
@commands.command()
async def betabaja(ctx):
   resultado = df.sort_values(by='Beta').head(5)
   if resultado.empty:
      await ctx.send("No se encontraron acciones con baja volatilidad (Beta).")
      return

   for i, (_, row) in enumerate(resultado.iterrows(), start=1):
      embed = crear_tarjeta_inversion(
               row,
               titulo=f"📉 {i}º Acción con Baja Volatilidad (Beta)",
               descripcion=f"Beta: {row['Beta']}",
               color=0x3498db)
      await ctx.send(embed=embed)


# Comando: Menos deuda
@commands.command()
async def menosdeuda(ctx):
   resultado = df.sort_values(by='Deuda/Capital (%)').head(5)
   if resultado.empty:
      await ctx.send("No se encontraron acciones con baja deuda.")
      return

   for i, (_, row) in enumerate(resultado.iterrows(), start=1):
      embed = crear_tarjeta_inversion(
               row,
               titulo=f"💳 {i}º Acción con Menos Deuda",
               descripcion=f"Deuda/Capital: {row['Deuda/Capital (%)']}%",
               color=0xf39c12)
      await ctx.send(embed=embed)


# Comando: Descargar excel de empresas
@commands.command()
async def descargar(ctx):
   try:
      # Crear un buffer en memoria
      buffer = io.BytesIO()
      df.to_excel(buffer, index=False)
      buffer.seek(0)  # Volver al inicio del archivo

      await ctx.send(
         content="📂 Aquí tienes el archivo Excel con los datos de acciones:",
         file=discord.File(fp=buffer, filename=sRUTA_EXCEL)
      )
   except Exception as e:
      await ctx.send(f"❌ Error al generar el archivo: {e}")


# Comando: ayuda personalizada
@commands.command()
async def ayuda(ctx):
   embed = discord.Embed(
      title="📘 Lista de Comandos Disponibles",
      description="Aquí tienes todos los comandos que puedes usar para explorar acciones y datos financieros:\n",
      color=0x3498db
   )

   embed.add_field(name="🔍 Búsqueda y Datos Generales", value=(
      "`!accion [ticker]` - Info detallada de una acción\n"
      "`!buscar [campo] [valor]` - Buscar por campo\n"
      "`!comparar [tick1] [tick2]` - Comparar 2 acciones\n"
   ), inline=False)

   embed.add_field(name="🏆 Rankings y Selecciones", value=(
      "`!mejores` - Top 5 por puntuación\n"
      "`!toproe` - Mejores por ROE\n"
      "`!betabaja` - Acciones con menor riesgo (Beta)\n"
      "`!menosdeuda` - Empresas con bajo endeudamiento\n"
   ), inline=False)

   embed.add_field(name="📊 Valoraciones", value=(
      "`!infravaloradas` - Precio < Valor Intrínseco\n"
      "`!sobrevaloradas` - Precio > Valor Intrínseco\n"
      "`!baratas` - Acciones con bajo P/E o PEG\n"
   ), inline=False)

   embed.add_field(name="💸 Rendimiento", value=(
      "`!dividendos` - Dividend Yield > 4%\n"
      "`!crecimiento` - Crecimiento de Ingresos > 20%\n"
   ), inline=False)

   embed.add_field(name="📂 Archivo", value=(
      "`!descargar` - Descargar el archivo Excel con los datos\n"
   ), inline=False)

   await ctx.send(embed=embed)


@commands.command()
async def limpiar(ctx):
   await ctx.channel.purge()
   await ctx.send(f"Se han eliminado los mensajes.")


# Evento: Error al usar un comando
async def on_command_error(ctx, error):
   if isinstance(error, CommandNotFound):
      await ctx.send("❌ Comando no reconocido. Usa `!ayuda` para ver los comandos disponibles.")
   else:
      # Si quieres ver otros errores en consola, pero no al usuario
      print(f"[ERROR] {error}")


# Función de configuración: Registrar los comandos
async def setup(bot):
   bot.add_command(accion)
   bot.add_command(mejores)
   bot.add_command(buscar)
   bot.add_command(infravaloradas)
   bot.add_command(sobrevaloradas)
   bot.add_command(baratas)
   bot.add_command(dividendos)
   bot.add_command(crecimiento)
   bot.add_command(comparar)
   bot.add_command(toproe)
   bot.add_command(betabaja)
   bot.add_command(menosdeuda)
   bot.add_command(descargar)
   bot.add_command(ayuda)
   bot.add_command(limpiar)
   bot.add_listener(on_command_error, "on_command_error")
