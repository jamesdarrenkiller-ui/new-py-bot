import discord
from discord.ext import commands


def embed(title: str, description: str = "", color: int = 0x5865F2) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=color)


def owner_only():
    return commands.is_owner()


def bot_permissions(**perms):
    return commands.bot_has_permissions(**perms)
