from discord.ext import commands
import discord

from constants.messages import REMOVAL_MESSAGE, ADMIN_CONFIG, PERSONAL_MESSAGE_AFTER_REMOVAL, INFO_MESSAGE, HELP_MESSAGE, REPORT_MESSAGE, ADMIN_REQUEST_SERVER_ID
from database.add_server_config import ServerConfig


class ToxicBotAdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def config(self, ctx, arg=None):
        member = ctx.author
        channel = ctx.channel
        server_config = ServerConfig()
        record = None
        try:
            record = server_config.getConfigFromUser(str(member.id))
        except AttributeError:
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            return  # Not implemented
        SERVER_ID = record[0]
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""
        
        await ctx.send(ADMIN_CONFIG.format(guild=guild_name, count=record[1], time=record[2]))
