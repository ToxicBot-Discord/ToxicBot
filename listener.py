from discord.ext import commands

import re
import logging

from constants.messages import REMOVAL_MESSAGE, PERSONAL_MESSAGE_AFTER_REMOVAL, INFO_MESSAGE
from constants.regex import TOXIC_REGEX
from helper import handleViolations

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
        message_content = message.content
        if re.search(TOXIC_REGEX, message_content, re.IGNORECASE):
            await message.delete()
            await message.channel.send(REMOVAL_MESSAGE.format(username=message.author.mention))
            await message.author.create_dm()
            violations = handleViolations([1, 2, 3])
            await message.author.dm_channel.send(PERSONAL_MESSAGE_AFTER_REMOVAL.format(violations=violations))
