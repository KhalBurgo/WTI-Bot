from discord.ext import commands
import discord
import aiohttp

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="player", description="Genera il link al profilo War Thunder del giocatore")
    @discord.app_commands.describe(nomeplayer="Il nickname del giocatore su War Thunder")
    async def player(self, interaction: discord.Interaction, nomeplayer: str):
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

async def setup(bot):
    await bot.add_cog(Player(bot))