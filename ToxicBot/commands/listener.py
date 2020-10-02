from discord.ext import commands
from discord.channel import DMChannel

import re
import logging

from constants.messages import REMOVAL_MESSAGE, PERSONAL_MESSAGE_AFTER_REMOVAL, INFO_MESSAGE
from constants.regex import TOXIC_REGEX
from helper.misc import handleViolations
from classifier.classifier import predict_toxicity

logger = logging.getLogger('')


class ToxicBotListener(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.warning('Logged on as {0}!'.format(self.bot.user.name))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, DMChannel):
            return

        message_content = message.content
        toxicity = predict_toxicity(message_content)

        indexes = []
        for index, pred in enumerate(toxicity):
            if pred == 1:
                indexes.append(index)
        if len(indexes) == 0:
            return
        await message.delete()
        await message.channel.send(REMOVAL_MESSAGE.format(username=message.author.mention))
        await message.author.create_dm()

        violations = handleViolations(indexes)
        await message.author.dm_channel.send(PERSONAL_MESSAGE_AFTER_REMOVAL.format(violations=violations))
