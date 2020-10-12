from discord.ext import commands
import discord
import asyncio
from constants.messages import (
    SUCCESSFUL_UPDATE,
    REQUIRE_NUMERICAL_VALUE,
    ADMIN_CONFIG,
    ADMIN_REQUEST_SERVER_ID,
    BAD_ARGUMENT,
    REQUEST_TIMEOUT,
)
from database.add_server_config import ServerConfig


class ToxicBotAdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Generic function to give the admin an option to choose from his multiple servers
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
            # Get the server config for servers that the user is an admin
            record = server_config.getConfigFromUser(str(member.id))
        except AttributeError:  # Attribute error means the user is the admin of multiple servers
            records = server_config.getAllServers(str(member.id))  # Get a list of servers where user is admin
            servers = []
            for record in records:
                guild = self.bot.get_guild(int(record[0]))
                if guild is not None:
                    guild_name = guild.name  # Get the guild name from server id
                    servers.append(guild_name)
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            embed = self.generate_embed("Servers", servers)
            await ctx.send(embed=embed)  # Send a multi-choice option to the user to select a specific server
            message = None
            try:
                message = await self.bot.wait_for("message", timeout=5.0)  # Wait for 5 seconds for response
            except asyncio.TimeoutError:
                await ctx.send(REQUEST_TIMEOUT)  # Send a timeout message
                return
            index = None
            try:
                index = int(message.content)  # Convert the string to number
            except Exception:
                # If non-numeric characters are passed
                await ctx.send(REQUIRE_NUMERICAL_VALUE.format(entity="Server Number"))
                return
            if index > len(records):  # Check if index is out of bounds
                await ctx.send(BAD_ARGUMENT)
                return
            record = records[index - 1]  # Get the specific server
        SERVER_ID = record[0]
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""

        await ctx.send(ADMIN_CONFIG.format(guild=guild_name, count=record[1], time=record[2]))

    # Changes the toxic_count_config for that server
    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def setcount(self, ctx, arg):
        count = None
        try:
            count = int(arg)  # Value to set the count config to
        except Exception:
            # If numerical value is not passed
            await ctx.send(REQUIRE_NUMERICAL_VALUE.format(entity="Toxic Count Threshold Per User"))
            return
        member = ctx.author
        server_config = ServerConfig()
        SERVER_OWNER_ID = str(member.id)
        SERVER_ID = 0
        try:
            # Get the server config for servers that the user is an admin
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, count=count)
        except AttributeError:  # If admin of multiple servers
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            records = server_config.getAllServers(str(member.id))
            servers = []
            for record in records:
                guild = self.bot.get_guild(int(record[0]))
                if guild is not None:
                    guild_name = guild.name
                    servers.append(guild_name)
            # Give a multi-choice option to the user
            embed = self.generate_embed("Servers", servers)
            await ctx.send(embed=embed)
            message = None
            try:  # Wait for 5 seconds for reply
                message = await self.bot.wait_for("message", timeout=5.0)
            except asyncio.TimeoutError:
                await ctx.send(REQUEST_TIMEOUT)  # Send a timeout message
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
            # Modify the server config for a particular server
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, server_id=SERVER_ID, count=count)
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""
        await ctx.send(SUCCESSFUL_UPDATE.format(entity="Toxic Count Threshold Per User", server=guild_name))

    # Used to set the days_threshold value in the server config
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
            # Get the server config for servers that the user is an admin
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, threshold=days)
        except AttributeError:  # Admin of multiple servers
            await ctx.send(ADMIN_REQUEST_SERVER_ID)
            records = server_config.getAllServers(str(member.id))
            servers = []
            for record in records:
                guild = self.bot.get_guild(int(record[0]))
                if guild is not None:
                    guild_name = guild.name
                    servers.append(guild_name)
            embed = self.generate_embed("Servers", servers)
            # Multi-choice option for the user
            await ctx.send(embed=embed)
            message = None
            try:  # Wait for reply for 5 seconds
                message = await self.bot.wait_for("message", timeout=5.0)
            except asyncio.TimeoutError:
                await ctx.send(REQUEST_TIMEOUT)  # Send a timeout message
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
            # Modify the server config for a particular server
            SERVER_ID = server_config.modifyServerConfig(SERVER_OWNER_ID, server_id=SERVER_ID, threshold=days)
        guild = self.bot.get_guild(int(SERVER_ID))
        guild_name = guild.name if guild is not None else ""
        # Send a success message to the user
        await ctx.send(
            SUCCESSFUL_UPDATE.format(
                entity="Days before resetting toxic count for an user",
                server=guild_name,
            )
        )
