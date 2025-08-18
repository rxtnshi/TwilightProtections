import sys
import os
sys.path.append(os.path.abspath("bot"))

import discord
import json
import logging
import customlogger
import BanHandler

from discord.ext import commands
from CustomEmbeds import create_embed

AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",")

class BanMenu(discord.ui.View):
    def __init__(self, bans):
        super().__init__(timeout=60)
        options = [
            discord.SelectOption(label=f"User {ban['user_id']}", description=ban['reason'])
            for ban in bans
        ]
        self.add_item(discord.ui.Select(placeholder="Select a banned user...", options=options, custom_id="ban_select"))

class GlobalBans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="checkbans", description="Show global bans")
    async def checkbans(self, interaction: discord.Interaction):
        # Load bans from JSON
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "ban_configs.json")
        with open(json_path, "r") as f:
            bans = json.load(f)

        if not bans:
            await interaction.response.send_message("No bans found.", ephemeral=True)
            return

        view = BanMenu(bans)
        await interaction.response.send_message("Select a banned user to view reason:", view=view, ephemeral=True)

    @discord.app_commands.command(name="globalban", description="Ban a user from all TwilightProtected servers")
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str):
        if str(interaction.user.id) not in AUTHORIZED_USERS:
            await interaction.response.send_message(":x: You are not authorized to use this command.", ephemeral=True)
            return
        
        try:
            await interaction.guild.ban(user, reason=f"Action requested by {interaction.user} ({interaction.user.id}). User has been removed from Twlight Protected servers for: {reason}")
        except Exception as error:
            await interaction.response.send_message(embed=create_embed("error", f"Failed to ban user: {error}"))
            return
        
        BanHandler.add_ban(user.id, reason, interaction.guild_id)
        logging.info(f"{interaction.user} ({interaction.user.id}) has banned {user.name} ({user.id}) for {reason} in {interaction.guild} ({interaction.guild_id})")

        await interaction.response.send_message(
            embed=create_embed("ban",f"User {user.mention} has been added to the ban list for `{reason}` and has been removed from TwilightProtected servers.")
        )

        

async def setup(bot):
    await bot.add_cog(GlobalBans(bot))