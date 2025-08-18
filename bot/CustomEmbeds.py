import discord
import datetime

from datetime import datetime

def create_embed(type, message):
    if type == "ban":
        embed = discord.Embed(
            title = "User has been added to banlist!",
            description = message,
            color = discord.Color.orange()
        )
        embed.set_thumbnail(url="https://media.tenor.com/d0VNnBZkSUkAAAAM/bongocat-banhammer.gif")
        embed.timestamp = datetime.now()
    
    elif type == "ping":
        embed = discord.Embed(
            title = "Ping Test",
            description = f"Pong! Response time: {message} ms",
            color = discord.Color.green()
        )
        embed.set_thumbnail(url="https://media.tenor.com/euLKuyD9Bn4AAAAM/dancing-security-guard.gif")
        embed.timestamp = datetime.now()

    elif type == "error":
        embed = discord.Embed(
            title = "Uh Oh! I ran into an error!",
            description = message,
            color = discord.Color.red()
        )
        embed.set_thumbnail(url="https://media.tenor.com/Wv6zVQPZFtcAAAAM/error.gif")
        embed.timestamp = datetime.now()

    else:
        embed = discord.Embed(
            title = "TwilightProtections",
            description = message,
            color = discord.Color.og_blurple()
        )
        embed.set_thumbnail(url="https://media.tenor.com/euLKuyD9Bn4AAAAM/dancing-security-guard.gif")
        embed.timestamp = datetime.now()

    return embed