import discord
import os
import logging

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from . import customlogger

# defines bot blah blah
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",")

# basic thing
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self):
        cogs_path = os.path.join(os.path.dirname(__file__), "cogs")
        for filename in os.listdir(cogs_path):
            if filename.endswith(".py"):
                await self.load_extension(f"bot.cogs.{filename[:-3]}")
                logging.info(f"Loaded cog: {filename}")
        await self.tree.sync()

    async def on_ready(self):
        logging.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")
            logging.warning(f"Command not found: {ctx.message.content}")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing arguments for command.")
            logging.warning(f"Missing argument in command: {ctx.message.content}")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("You do not have permission to use this command.")
            logging.warning(f"Permission denied for user: {ctx.author}")
        else:
            await ctx.send("An error occurred.")
            logging.error(f"Error: {error}")
        
    @discord.app_commands.command(name="sync", description="Syncs new slash commands")
    async def sync_commands(self, interaction: discord.Interaction):
        if str(interaction.user.id) not in AUTHORIZED_USERS:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return
        await self.tree.sync()
        await interaction.response.send_message("Slash commands synced!", ephemeral=True)

bot = Bot()
bot.run(BOT_TOKEN)