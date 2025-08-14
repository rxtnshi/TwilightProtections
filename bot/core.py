import discord
import os
import customlogger
import logging

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from glob import glob

# defines bot blah blah
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS")
COGS = [path.split("\\")[-1][:-3] for path in glob(".bot/cogs/*.py")]

# basic thing
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self):
        for cog in COGS:
            logging.info(f"{cog} loaded!")
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


bot = Bot()
bot.run(BOT_TOKEN)