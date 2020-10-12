from discord.ext import commands
from discord.channel import DMChannel
from discord.utils import find

import logging

from constants.messages import (
    REMOVAL_MESSAGE,
    PERSONAL_MESSAGE_AFTER_REMOVAL,
    ADMIN_MESSAGE_AFTER_BOT_JOIN,
)
from classifier.classifier import predict_toxicity
from database.add_toxic_count import AddToxicCount
from database.add_server_config import ServerConfig

toxic_bot_adder = AddToxicCount()
logger = logging.getLogger("")


class ToxicBotListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.warning("Logged on as {0}!".format(self.bot.user.name))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server_config = ServerConfig()
        SERVER_ID = str(guild.id)
        SERVER_OWNER_ID = str(guild.owner_id)
        server_config.createServerConfig(SERVER_ID, SERVER_OWNER_ID)

        await self.bot.wait_until_ready()

        # Doesn't work as it returns None always
        owner = self.bot.get_user(int(SERVER_OWNER_ID))
        if owner is None:
            general = find(lambda x: x.name == "general", guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                await general.send(ADMIN_MESSAGE_AFTER_BOT_JOIN)
        else:
            await owner.create_dm()
            await owner.dm_channel.send(ADMIN_MESSAGE_AFTER_BOT_JOIN)

    @commands.Cog.listener()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, DMChannel):
            return

        message_content = message.content
        toxicity = predict_toxicity(message_content)

        if toxicity == 0:
            return
        await message.delete()
        await message.channel.send(REMOVAL_MESSAGE.format(username=message.author.mention))
        await message.author.create_dm()

        await message.author.dm_channel.send(PERSONAL_MESSAGE_AFTER_REMOVAL)

        USER_ID = str(message.author.id)
        SERVER_ID = str(message.guild.id)
        SERVER_OWNER_ID = str(message.guild.owner_id)

        if USER_ID == SERVER_OWNER_ID:
            return
        try:
            toxic_bot_adder.addToxicCount(SERVER_ID, USER_ID)
        except AttributeError:
            await message.guild.kick(message.author, reason="Toxic Message Limit Exceeded")
