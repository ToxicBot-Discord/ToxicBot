from discord.ext import commands
import discord
import asyncio
from constants.messages import (
    SUCCESSFUL_UPDATE,
    REQUIRE_NUMERICAL_VALUE,
    ADMIN_CONFIG,
    ADMIN_REQUEST_SERVER_ID,
    BAD_ARGUMENT,
)
from database.add_server_config import ServerConfig


class ToxicBotAdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_embed(self, topic, servers):
        embed = discord.Embed(title=topic, description="Please select a server")
        for index, server in enumerate(servers):
            index_humanize = index + 1
            embed.add_field(name=f"{index_humanize}. {server}", value=f"______", inline=False)  # noqa F541
        embed.set_footer(text="Reply with the server number")
        return embed

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def config(self, ctx):
        member = ctx.author
        server_config = ServerConfig()
        record = None
        try:
            record = server_config.getConfigFromUser(str(member.id))
        except AttributeError:
            records = server_config.getAllServers(str(member.id))
            servers = []
            for record in records:
                guild = self.bot.get_guild(int(record[0]))
                if guild is not None:
                    guild_name = guild.name
                    servers.append(guild_name)
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            embed = self.generate_embed("Servers", servers)
            await ctx.send(embed=embed)
            message = None
            try:
                message = await self.bot.wait_for("message", timeout=5.0)
            except asyncio.TimeoutError:
                return
            index = None
            try:
                index = int(message.content)
            except Exception:
                await ctx.send(REQUIRE_NUMERICAL_VALUE.format(entity="Server Number"))
                return
            if index > len(records):
                await ctx.send(BAD_ARGUMENT)
                return
            record = records[index - 1]
        SERVER_ID = record[0]
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""

        await ctx.send(ADMIN_CONFIG.format(guild=guild_name, count=record[1], time=record[2]))

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def setcount(self, ctx, arg):
        count = None
        try:
            count = int(arg)
        except Exception:
            await ctx.send(REQUIRE_NUMERICAL_VALUE.format(entity="Toxic Count Threshold Per User"))
            return
        member = ctx.author
        server_config = ServerConfig()
        SERVER_OWNER_ID = str(member.id)
        SERVER_ID = 0
        try:
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, count=count)
        except AttributeError:
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            records = server_config.getAllServers(str(member.id))
            servers = []
            for record in records:
                guild = self.bot.get_guild(int(record[0]))
                if guild is not None:
                    guild_name = guild.name
                    servers.append(guild_name)
            embed = self.generate_embed("Servers", servers)
            await ctx.send(embed=embed)
            message = None
            try:
                message = await self.bot.wait_for("message", timeout=5.0)
            except asyncio.TimeoutError:
                return
            index = None
            try:
                index = int(message.content)
            except Exception:
                await ctx.send(REQUIRE_NUMERICAL_VALUE.format(entity="Server Number"))
                return
            if index > len(records):
                await ctx.send(BAD_ARGUMENT)
            SERVER_ID = str(records[index - 1][0])
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, server_id=SERVER_ID, count=count)
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""
        await ctx.send(SUCCESSFUL_UPDATE.format(entity="Toxic Count Threshold Per User", server=guild_name))

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def setdays(self, ctx, arg):
        days = None
        try:
            days = int(arg)
        except Exception:
            await ctx.send(REQUIRE_NUMERICAL_VALUE.format(entity="Days before resetting toxic count for an user"))
        member = ctx.author
        server_config = ServerConfig()
        SERVER_OWNER_ID = str(member.id)
        SERVER_ID = 0
        try:
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, threshold=days)
        except AttributeError:
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            records = server_config.getAllServers(str(member.id))
            servers = []
            for record in records:
                guild = self.bot.get_guild(int(record[0]))
                if guild is not None:
                    guild_name = guild.name
                    servers.append(guild_name)
            embed = self.generate_embed("Servers", servers)
            await ctx.send(embed=embed)
            message = None
            try:
                message = await self.bot.wait_for("message", timeout=5.0)
            except asyncio.TimeoutError:
                return
            index = None
            try:
                index = int(message.content)
            except Exception:
                await ctx.send(REQUIRE_NUMERICAL_VALUE.format(entity="Server Number"))
                return
            if index > len(records):
                await ctx.send(BAD_ARGUMENT)
            SERVER_ID = str(records[index - 1][0])
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, server_id=SERVER_ID, threshold=days)
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""
        await ctx.send(
            SUCCESSFUL_UPDATE.format(
                entity="Days before resetting toxic count for an user",
                server=guild_name,
            )
        )
