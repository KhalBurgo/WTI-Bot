import discord
from discord import app_commands
from discord.ext import commands
import os
import urllib.parse
import aiohttp

from keep_alive import keep_alive  # Per mantenere attivo su Render

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
            "/clan <squadriglia> - Mostra il profilo della squadriglia"
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

# comando /clan
@bot.tree.command(name="clan", description="Mostra informazioni su una squadriglia di War Thunder")
@app_commands.describe(
    squadron="Il tag della squadriglia (es: WTI)",
    type="Tipo di informazione da mostrare: members oppure points"
)
async def clan(interaction: discord.Interaction,
               squadron: str = "",
               type: str = ""):
    await interaction.response.defer(ephemeral=False)

    filename = "SQUADRONS.json"
    squadrons_json = client.download_as_text(filename)
    squadrons = json.loads(squadrons_json)
    guild_id = str(interaction.guild_id)

    if not squadron:
        if guild_id in squadrons:
            squadron_name = squadrons[guild_id]["SQ_LongHandName"]
        else:
            embed = discord.Embed(
                title="Errore",
                description="Nessuna squadriglia specificata e nessuna configurata per questo server.",
                color=discord.Color.red())
            embed.set_footer(text="Meow :3")
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
    else:
        clan_data = await search_for_clan(squadron.lower())
        if not clan_data:
            await interaction.followup.send("Squadriglia non trovata.", ephemeral=True)
            return

        squadron_name = clan_data.get("long_name")

    embed = await fetch_squadron_info(squadron_name, type)

    if embed:
        embed.set_footer(text="Meow :3")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("Errore durante il recupero delle informazioni.", ephemeral=True)
# Fine comando /clan

keep_alive()
bot.run(os.environ["TOKEN"])
