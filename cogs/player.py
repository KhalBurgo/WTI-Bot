from discord.ext import commands
import discord
import aiohttp
from config import GUILD

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="player",
        description="Genera il link al profilo War Thunder del giocatore"
    )
    @discord.app_commands.describe(nomeplayer="Il nickname del giocatore su War Thunder")
    @discord.app_commands.guilds(GUILD)
    async def player(self, interaction: discord.Interaction, nomeplayer: str):
        await interaction.response.defer()
        url = f"https://warthunder.com/en/community/userinfo?nick={nomeplayer}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                if "Page not found on server." in html:
                    await interaction.followup.send(
                        embed=discord.Embed(
                            title="❌ Giocatore non trovato",
                            description=f"Nessun profilo trovato per **{nomeplayer}**.",
                            color=discord.Color.red()
                        )
                    )
                    return

        embed = discord.Embed(
            title=f"🔎 Profilo di {nomeplayer}",
            description=(
                f"📄 Clicca sul link qui sotto per aprire il profilo War Thunder:\n"
                f"[➡️ {nomeplayer}]({url})"
            ),
            color=discord.Color.dark_blue()
        )
        embed.set_thumbnail(url="https://warthunder.com/favicon.ico")
        embed.set_footer(text="Powered by War Thunder", icon_url="https://warthunder.com/favicon.ico")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Player(bot))
