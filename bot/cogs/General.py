import discord
from discord.ext import commands
import os

AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",")

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Shows bot response time")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Response time: {latency_ms} ms")

    @discord.app_commands.command(name="invite", description="Displays the invite code for this bot")
    async def send_invite(self, interaction: discord.Interaction):
        if str(interaction.user.id) not in AUTHORIZED_USERS:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return
        await interaction.response.send_message(f"https://discord.com/oauth2/authorize?client_id=1076664536918130780&permissions=8&integration_type=0&scope=bot+applications.commands", ephemeral=True)

async def setup(bot):
    await bot.add_cog(General(bot))