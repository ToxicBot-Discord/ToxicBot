import discord
from discord.ext.commands import has_permissions
import logging
from configparser import RawConfigParser
import re

import logger
from constants.messages import REMOVAL_MESSAGE, PERSONAL_MESSAGE_AFTER_REMOVAL, INFO_MESSAGE
from constants.regex import TOXIC_REGEX, INFO_REGEX
from helper import handleViolations

logger = logging.getLogger('')

config = RawConfigParser()
config.read('secrets.ini')

DISCORD_BOT_TOKEN = config.get('Discord', 'BOT_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    logger.warning('Logged on as {0}!'.format(client.user.name))


@client.event
@has_permissions(manage_messages=True)
async def on_message(message):
    if message.author == client.user:
        return
    message_content = message.content

    if message.author.dm_channel and message.channel.id == message.author.dm_channel.id:
        if re.search(INFO_REGEX, message_content, re.IGNORECASE):
            await message.channel.send(INFO_MESSAGE.format(username=message.author.mention))
    else:
        if re.search(TOXIC_REGEX, message_content, re.IGNORECASE):
            await message.delete()
            await message.channel.send(REMOVAL_MESSAGE.format(username=message.author.mention))
            await message.author.create_dm()
            violations = handleViolations([1, 2, 3])
            await message.author.dm_channel.send(PERSONAL_MESSAGE_AFTER_REMOVAL.format(violations=violations))


client.run(DISCORD_BOT_TOKEN)
