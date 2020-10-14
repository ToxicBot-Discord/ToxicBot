from discord.ext import commands
from discord.channel import DMChannel

import re
import logging

from constants.messages import REMOVAL_MESSAGE, PERSONAL_MESSAGE_AFTER_REMOVAL, INFO_MESSAGE
from constants.regex import TOXIC_REGEX
from classifier.classifier import predict_toxicity

logger = logging.getLogger('')


class ToxicBotListener(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.warning('Logged on as {0}!'.format(self.bot.user.name))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.Cog.listener()
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
