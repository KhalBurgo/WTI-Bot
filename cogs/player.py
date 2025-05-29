from discord.ext import commands
import discord
import aiohttp
import asyncio
from datetime import datetime
from config import GUILD  # Importa il tuo ID server da config.py

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="player",
        description="Mostra i profili War Thunder e ThunderSkill del giocatore"
    )
    @discord.app_commands.describe(nomeplayer="Il nickname del giocatore su War Thunder")
    @discord.app_commands.guilds(GUILD)
    async def player(self, interaction: discord.Interaction, nomeplayer: str):
        await interaction.response.defer()

        wt_url = f"https://warthunder.com/en/community/userinfo?nick={nomeplayer}"
        ts_url = f"https://thunderskill.com/en/stat/{nomeplayer}"

        async with aiohttp.ClientSession() as session:
            async with session.get(wt_url) as response:
                html = await response.text()
                if "Page not found on server." in html:
                    await interaction.followup.send(f"❌ Giocatore **{nomeplayer}** non trovato.")
                    return

        await asyncio.sleep(1)  # In futuro utile per scraping dinamico

        embed = discord.Embed(
            title=f"Profilo di {nomeplayer}",
            description=(
                f"🌐 [Profilo War Thunder]({wt_url})\n\n"
                f"📊 [Profilo ThunderSkill]({ts_url})"
            ),
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url="attachment://default.jpg")
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        embed.set_footer(text=f"Richiesta il {now}")

        file = discord.File("avatar/default.jpg", filename="default.jpg")
        await interaction.followup.send(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Player(bot))
