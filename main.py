
import discord
from discord import app_commands
from discord.ext import commands
import os
import urllib.parse
import aiohttp

from keep_alive import keep_alive  # Per mantenere attivo su Render
from SQ_Info import fetch_squadron_info  # Importa dal file SQ_Info.py

intents = discord.Intents.default()
intents.message_content = True  # Non serve se usi solo slash command

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1124308157418717215
GUILD = discord.Object(id=GUILD_ID)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"✅ Bot connesso come {bot.user}")
    try:
        synced = await bot.tree.sync(guild=GUILD)
        print(f"🔄 Comandi slash sincronizzati: {len(synced)}")
        for cmd in synced:
            print(f"🔸 {cmd.name}")
    except Exception as e:
        print(f"❌ Errore sync: {e}")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    print(f"❌ Errore comando slash: {error}")
    try:
        await interaction.response.send_message("❌ Si è verificato un errore nel comando.", ephemeral=True)
    except Exception:
        pass

@bot.command()
async def sync(ctx):
    synced = await bot.tree.sync(guild=GUILD)
    await ctx.send(f"✅ Comandi sincronizzati: {len(synced)}")

@bot.tree.command(name="help", description="Mostra i comandi disponibili", guild=GUILD)
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Comandi disponibili",
        description=(
            "/help - Mostra questo messaggio\n"
            "/ping - Verifica se il bot è online\n"
            "/player <nickname> - Mostra il profilo del giocatore\n"
            "/clan <tag> - Mostra info dettagliate della squadriglia"
        ),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Risponde con Pong!", guild=GUILD)
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

@bot.tree.command(name="player", description="Genera il link al profilo War Thunder del giocatore", guild=GUILD)
@app_commands.describe(nomeplayer="Il nickname del giocatore su War Thunder")
async def player(interaction: discord.Interaction, nomeplayer: str):
    await interaction.response.defer()
    url = f"https://warthunder.com/en/community/userinfo?nick={nomeplayer}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            if "Page not found on server." in html:
                await interaction.followup.send(f"❌ Giocatore **{nomeplayer}** non trovato.")
                return
    embed = discord.Embed(
        title=f"Profilo di {nomeplayer}",
        description=f"[Clicca qui per aprire il profilo]({url})",
        color=discord.Color.blue()
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="clan", description="Mostra informazioni su una squadriglia di War Thunder", guild=GUILD)
@app_commands.describe(
    squadron="Il tag della squadriglia (es: WTI)",
    type="Tipo di informazione: members, points o logs"
)
async def clan(interaction: discord.Interaction,
               squadron: str,
               type: str = ""):
    await interaction.response.defer(ephemeral=False)

    embed = await fetch_squadron_info(squadron.upper(), type)

    if embed:
        embed.set_footer(text="📊 Dati da warthunder.com")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Squadriglia non trovata o errore nel recupero dati.", ephemeral=True)

keep_alive()
bot.run(os.environ["TOKEN"])
