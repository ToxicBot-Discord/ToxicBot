from discord.ext import commands
import discord

from constants.messages import (
    SUCCESSFUL_UPDATE,
    REQUIRE_NUMERICAL_VALUE,
    REMOVAL_MESSAGE,
    ADMIN_CONFIG,
    PERSONAL_MESSAGE_AFTER_REMOVAL,
    INFO_MESSAGE,
    HELP_MESSAGE,
    REPORT_MESSAGE,
    ADMIN_REQUEST_SERVER_ID,
)
from database.add_server_config import ServerConfig


class ToxicBotAdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def config(self, ctx):
        member = ctx.author
        channel = ctx.channel
        server_config = ServerConfig()
        record = None
        try:
            record = server_config.getConfigFromUser(str(member.id))
        except AttributeError:
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            return  # Implement asking for specific server
        SERVER_ID = record[0]
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""

        await ctx.send(
            ADMIN_CONFIG.format(guild=guild_name, count=record[1], time=record[2])
        )

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def setcount(self, ctx, arg):
        count = None
        try:
            count = int(arg)
        except Exception:
            await ctx.send(
                REQUIRE_NUMERICAL_VALUE.format(entity="Toxic Count Threshold Per User")
            )
            return
        member = ctx.author
        channel = ctx.channel
        server_config = ServerConfig()
        SERVER_OWNER_ID = str(member.id)
        SERVER_ID = 0
        try:
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, count=count)
        except AttributeError:
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            return  # Implement asking for specific server
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""
        await ctx.send(
            SUCCESSFUL_UPDATE.format(
                entity="Toxic Count Threshold Per User", server=guild_name
            )
        )

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def setdays(self, ctx, arg):
        days = None
        try:
            days = int(arg)
        except Exception:
            await ctx.send(
                REQUIRE_NUMERICAL_VALUE.format(
                    entity="Days before resetting toxic count for an user"
                )
            )
        member = ctx.author
        channel = ctx.channel
        server_config = ServerConfig()
        SERVER_OWNER_ID = str(member.id)
        SERVER_ID = 0
        try:
            SERVER_ID = server_config.modifyServerConfig(
                SERVER_OWNER_ID, threshold=days
            )
        except AttributeError:
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            return  # Implement asking for specific server
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""
        await ctx.send(
            SUCCESSFUL_UPDATE.format(
                entity="Days before resetting toxic count for an user",
                server=guild_name,
            )
        )

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def ban(self, ctx, arg):
        pass
