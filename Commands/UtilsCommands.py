# DiscordBot-BestStocks\Commands\UtilsCommands.py
import discord


def crear_tarjeta_inversion(row, titulo="📈 Acción:", descripcion="Datos de inversión:", color=0x00cc99):
   embed = discord.Embed(
      title=f"{titulo}: {row['Nombre']} [{row['Ticker']}]",
      description=descripcion,
      color=color
   )
   embed.add_field(name="💼 Sector", value=row['Sector'], inline=True)
   embed.add_field(name="🌍 País", value=row['País'], inline=True)
   embed.add_field(name="🏷️ Puntuación", value=str(row['Puntuación']), inline=True)

   embed.add_field(name="💵 Precio actual", value=f"${row['Precio ($)']:.2f}", inline=True)
   embed.add_field(name="🎯 Valor Intrínseco", value=f"${row['Valor Intrínseco ($)']:.2f}", inline=True)
   embed.add_field(name="📊 P/E", value=str(row['P/E']), inline=True)

   embed.add_field(name="📈 ROE", value=f"{row['ROE (%)']}%", inline=True)
   embed.add_field(name="💰 Dividend Yield", value=f"{row['Dividend Yield (%)']}%", inline=True)
   embed.add_field(name="📈 Crec. Ingresos", value=f"{row['Crecimiento de Ingresos (%)']}%", inline=True)

   embed.set_footer(text="Fuente: Excel de Mejores Acciones")
   return embed
