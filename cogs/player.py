from discord.ext import commands
import discord
import aiohttp
from config import GUILD  # Usa un file config.py per evitare problemi

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="player",
        description="Genera i link ai profili War Thunder e ThunderSkill del giocatore"
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

        embed = discord.Embed(
            title=f"🔎 Profilo di {nomeplayer}",
            description=(
                f"\n📄 **War Thunder:** [Apri il profilo ufficiale]({wt_url})\n"
                f"📊 **ThunderSkill:** [Statistiche avanzate]({ts_url})"
            ),
            color=discord.Color.dark_blue()
        )
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/2/2e/War_Thunder_logo.png")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Player(bot))
