import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from config import GUILD # ← OK ORA

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
        synced = await bot.tree.sync(guild=GUILD)
        print(f"🔄 Comandi slash sincronizzati: {len(synced)}")
        for cmd in synced:
            print(f"🔸 {cmd.name}")
    except Exception as e:
        print(f"❌ Errore sync: {e}")

# Sync manuale
@bot.command()
async def sync(ctx):
    synced = await bot.tree.sync(guild=GUILD)
    await ctx.send(f"✅ Comandi sincronizzati: {len(synced)}")

# Gestione errori dei comandi slash
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    print(f"❌ Errore comando slash: {error}")
    try:
        await interaction.response.send_message("❌ Si è verificato un errore nel comando.", ephemeral=True)
    except Exception:
        pass

keep_alive()
bot.run(os.environ["TOKEN"])
