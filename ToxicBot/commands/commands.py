from discord.ext import commands
import discord

from constants.messages import (
    ADMIN_HELP_MESSAGE,
    REMOVAL_MESSAGE,
    PERSONAL_MESSAGE_AFTER_REMOVAL,
    INFO_MESSAGE,
    HELP_MESSAGE,
    REPORT_MESSAGE,
)
from database.add_server_config import ServerConfig


class ToxicBotGeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    async def info(self, ctx):
        member = ctx.author
        channel = ctx.channel
        await ctx.send(INFO_MESSAGE.format(username=member.name))

    @commands.command()
    @commands.dm_only()
    async def help(self, ctx):
        member = ctx.author
        channel = ctx.channel
        server_config = ServerConfig()
        try:
            server_config.getConfigFromUser(str(member.id))
        except commands.NotOwner:
            await ctx.send(HELP_MESSAGE.format(username=member.name))
            return
        except AttributeError:
            pass
        await ctx.send(ADMIN_HELP_MESSAGE.format(username=member.name))

    @commands.command()
    @commands.dm_only()
    async def report(self, ctx):
        member = ctx.author
        channel = ctx.channel
        embed = discord.Embed(
            title="GitHub - ToxicBot",
            url="https://github.com/Sid200026/ToxicBot/issues",
            description="Report issues and bugs",
        )
        await ctx.send(embed=embed)
