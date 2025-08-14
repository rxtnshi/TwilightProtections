import discord
from discord.ext import commands
import json
import os

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

    @discord.app_commands.command(name="globalban", description="Show global bans")
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str):
        if str(interaction.user.id) not in AUTHORIZED_USERS:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return
        
        try:
            await interaction.guild.ban(user, reason=reason)
        except Exception as error:
            await interaction.response.send_message(f"Failed to ban user: {error}")
            return
        
        json_path = os.path.join(os.path.dirname(__file__), "..", "data", "ban_configs.json")
        if not os.path.exists(json_path):
            bans = []
        else:
            with open(json_path, "r") as f:
                try:
                    bans = json.load(f)
                except json.JSONDecodeError:
                    bans = []

        ban_entry = {
            "user_id": str(user.id),
            "reason": reason,
            "guild_id": str(interaction.guild.id)
        }
        bans.append(ban_entry)
        with open(json_path, "w") as f:
            json.dump(bans, f, indent=2)

        await interaction.response.send_message(
            f"User {user.mention} has been banned from Twilight Protected servers for: {reason}."
        )
        
        

async def setup(bot):
    await bot.add_cog(GlobalBans(bot))