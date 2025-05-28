import discord
from discord import app_commands
from discord.ext import commands
import os
import urllib.parse
import aiohttp

from keep_alive import keep_alive  # Flask server per Render

intents = discord.Intents.default()
intents.message_content = False  # Lascia pure False, se usi solo slash command

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")
    try:
        guild = discord.Object(id=1124308157418717215)  # Sostituisci col tuo server ID
        synced = await bot.tree.sync(guild=guild)
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

# ✅ Comando manuale per forzare la sincronizzazione
@bot.command()
async def sync(ctx):
    synced = await bot.tree.sync(guild=discord.Object(id=1124308157418717215))
    await ctx.send(f"✅ Comandi sincronizzati: {len(synced)}")

@bot.tree.command(name="help", description="Mostra i comandi disponibili")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Comandi disponibili",
        description=(
            "/help - Mostra questo messaggio\n"
            "/ping - Verifica se il bot è online\n"
            "/player <nickname> - Mostra il profilo del giocatore\n"
            "/clan <squadriglia> - Mostra il profilo della squadriglia"
        ),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Risponde con Pong!")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

@bot.tree.command(name="player", description="Genera il link al profilo War Thunder del giocatore")
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

@bot.tree.command(name="clan", description="Mostra il link allo squadrone War Thunder")
@app_commands.describe(nome="Il nome completo dello squadrone")
async def clan(interaction: discord.Interaction, nome: str):
    nome_url = urllib.parse.quote(nome)
    link = f"https://warthunder.com/en/community/claninfo/{nome_url}"
    embed = discord.Embed(
        title=f"Clan: {nome}",
        description=f"[Clicca qui per vedere la squadriglia]({link})",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

keep_alive()
bot.run(os.environ["TOKEN"])
