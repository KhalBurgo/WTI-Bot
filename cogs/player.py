from discord.ext import commands
import discord
import aiohttp
from bs4 import BeautifulSoup
from config import GUILD
from datetime import datetime

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

        avatar_url = None

        async with aiohttp.ClientSession() as session:
            async with session.get(wt_url) as response:
                html = await response.text()
                if "Page not found on server." in html:
                    await interaction.followup.send(f"❌ Giocatore **{nomeplayer}** non trovato.")
                    return

                # Parse HTML per trovare l'avatar
                soup = BeautifulSoup(html, "lxml")
                # Di solito l'avatar è in <img class="user-info__avatar-img" ...>
                avatar_img = soup.find("img", class_="user-info__avatar-img")
                if avatar_img and avatar_img.has_attr("src"):
                    avatar_url = avatar_img["src"]
                    # Controlla se è URL completo o relativo
                    if avatar_url.startswith("//"):
                        avatar_url = "https:" + avatar_url

        embed = discord.Embed(
            title=f"🔎 Profilo di {nomeplayer}",
            description=(
                f"\n📄 **War Thunder:** [Apri il profilo ufficiale]({wt_url})\n\n"
                f"📊 **ThunderSkill:** [Statistiche avanzate]({ts_url})"
            ),
            color=discord.Color.dark_blue()
        )

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)
        else:
            # fallback
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/2/2e/War_Thunder_logo.png")

        now = datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")
        embed.set_footer(text=f"Richiesto il {now}")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Player(bot))


