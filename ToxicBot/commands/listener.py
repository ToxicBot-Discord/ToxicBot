from discord.ext import commands
from discord.channel import DMChannel
from discord.utils import find

import logging

from constants.messages import (
    REMOVAL_MESSAGE,
    PERSONAL_MESSAGE_AFTER_REMOVAL,
    ADMIN_MESSAGE_AFTER_BOT_JOIN,
    WELCOME_MESSAGE,
)
from classifier.classifier import predict_toxicity
from database.toxic_count import ToxicCount
from database.server_config import ServerConfig

toxic_bot_adder = ToxicCount()
logger = logging.getLogger("")


class ToxicBotListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Run when the bot is up and running
    @commands.Cog.listener()
    async def on_ready(self):
        logger.warning("Logged on as {0}!".format(self.bot.user.name))

    # Run when someone joins the channel
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(WELCOME_MESSAGE.format(member, member.guild))
        if channel is None:
            await member.create_dm()
            await member.dm_channel.send(WELCOME_MESSAGE.format(member, member.guild))
        
    # When the bot is added to a server
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server_config = ServerConfig()
        SERVER_ID = str(guild.id)
        SERVER_OWNER_ID = str(guild.owner_id)
        # Create the configurations for the server
        server_config.createServerConfig(SERVER_ID, SERVER_OWNER_ID)

        # Doesn't work as it returns None always ( BUG )
        owner = self.bot.get_user(int(SERVER_OWNER_ID))
        if owner is None:
            # Send a message to the general channel
            general = find(lambda x: x.name == "general", guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                await general.send(ADMIN_MESSAGE_AFTER_BOT_JOIN)
        else:
            await owner.create_dm()
            await owner.dm_channel.send(ADMIN_MESSAGE_AFTER_BOT_JOIN)

    # When a message is sent in the guild
    @commands.Cog.listener()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def on_message(self, message):
        if message.author == self.bot.user:
            return  # Ignore messages sent by the bpt
        if isinstance(message.channel, DMChannel):
            return  # Ignore Private DMs

        message_content = message.content
        toxicity = predict_toxicity(message_content)  # Predict the toxicity of the message

        if toxicity == 0:
            return
        await message.delete()  # Delete the message
        await message.channel.send(REMOVAL_MESSAGE.format(username=message.author.mention))
        await message.author.create_dm()
        # Warn the author
        await message.author.dm_channel.send(PERSONAL_MESSAGE_AFTER_REMOVAL)

        USER_ID = str(message.author.id)
        SERVER_ID = str(message.guild.id)
        SERVER_OWNER_ID = str(message.guild.owner_id)

        if USER_ID == SERVER_OWNER_ID:
            return  # Do not add to database if user is the bot owner
        try:
            toxic_bot_adder.addToxicCount(SERVER_ID, USER_ID)  # Add to the database
        except AttributeError:  # If an attribute error is thrown, kick out the author
            await message.guild.kick(message.author, reason="Toxic Message Limit Exceeded")
