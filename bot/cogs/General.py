import sys
import os
sys.path.append(os.path.abspath("bot"))

import discord
import os

from CustomEmbeds import create_embed
from discord.ext import commands


AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",")
INVITE_LINK = os.getenv("INVITE_LINK")

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Shows bot response time")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(embed=create_embed("ping", f"{latency_ms}"))

    @discord.app_commands.command(name="invite", description="Displays the invite code for this bot")
    async def send_invite(self, interaction: discord.Interaction):
        if str(interaction.user.id) not in AUTHORIZED_USERS:
            await interaction.response.send_message(":x: You are not authorized to use this command.", ephemeral=True)
            return
        await interaction.response.send_message(INVITE_LINK, ephemeral=True)\

async def setup(bot):
    await bot.add_cog(General(bot))