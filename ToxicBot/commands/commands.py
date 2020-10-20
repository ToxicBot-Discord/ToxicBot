from discord.ext import commands
import discord

from helper import embed as embedded
from constants.messages import (
    ADMIN_HELP_MESSAGE,
    INFO_MESSAGE,
    HELP_MESSAGE,
)
from database.server_config import ServerConfig


class ToxicBotGeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Get information about the toxic bot
    @commands.command()
    @commands.dm_only()
    async def info(self, ctx):
        member = ctx.author
        await ctx.send(embed=embedded.info(INFO_MESSAGE.format(username=member.name)))

    """
    There are two types of Help commands, one for server admins and one for
    general users.
    HELP_MESSAGE -> For general users
    ADMIN_HELP_MESSAGE -> For admin users
    """

    @commands.command()
    @commands.dm_only()
    async def help(self, ctx):
        member = ctx.author
        server_config = ServerConfig()
        try:
            server_config.getConfigFromUser(str(member.id))
        except commands.NotOwner:  # User does not own a server
            await ctx.send(embed=embedded.help(HELP_MESSAGE.format(username=member.name)))
            return
        except AttributeError:
            pass
        await ctx.send(embed=embedded.help(ADMIN_HELP_MESSAGE.format(username=member.name)))

    # Command to report any issues
    @commands.command()
    @commands.dm_only()
    async def report(self, ctx):
        embed = discord.Embed(
            title="GitHub - ToxicBot",
            url="https://github.com/Sid200026/ToxicBot/issues",
            description="Report issues and bugs",
        )
        await ctx.send(embed=embed)
