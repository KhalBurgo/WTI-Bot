from discord.ext import commands
import discord
from Leaderboard import search_for_clan
from SQ_Info import fetch_squadron_info

class Clan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="clan", description="Mostra informazioni su una squadriglia di War Thunder")
    @discord.app_commands.describe(
        squadron="Il tag della squadriglia (es: WTI)",
        type="Tipo di informazione: members, points o logs"
    )
    async def clan(self, interaction: discord.Interaction,
                   squadron: str,
                   type: str = ""):
        await interaction.response.defer(ephemeral=False)

        clan_data = await search_for_clan(squadron)
        if not clan_data:
            await interaction.followup.send("❌ Squadriglia non trovata.", ephemeral=True)
            return

        squadron_name = clan_data.get("long_name")
        embed = await fetch_squadron_info(squadron_name, type)

        if embed:
            embed.set_footer(text="📊 Dati da warthunder.com")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Errore nel recupero dei dati della squadriglia.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clan(bot))