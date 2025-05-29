import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from config import GUILD  # ← Assicurati che GUILD sia impostato correttamente

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

        wt_url = f"https://warthunder.com/en/community/userinfo?nick={nomeplayer}"
        ts_url = f"https://thunderskill.com/en/stat/{nomeplayer}"

        avatar_url = None

        async with aiohttp.ClientSession() as session:
            async with session.get(wt_url) as response:
                html = await response.text()
                if "Page not found on server." in html:
                    await interaction.followup.send(f"❌ Giocatore **{nomeplayer}** non trovato.")
                    return
                soup = BeautifulSoup(html, "lxml")

                # Cerca immagine avatar con src che inizia con URL base avatar WT
                for img in soup.find_all("img"):
                    src = img.get("src", "")
                    if src.startswith("https://avatars.warthunder.com/img/"):
                        avatar_url = src
                        break

        embed = discord.Embed(
            title=f"Profilo di {nomeplayer}",
            description=(
                f"[Profilo War Thunder]({wt_url})\n\n"  # doppia riga vuota per separazione
                f"[Profilo Thunderskill]({ts_url})"
            ),
            color=discord.Color.blue()
        )

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)

        # Footer con data/ora corrente
        now = datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")
        embed.set_footer(text=f"Informazioni richieste il {now}")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Player(bot))



