REMOVAL_MESSAGE = """
The message by {username} was deleted as it violated the channel's moral guidelines.
Multiple such violations may lead to a temporary or even a permanent ban
"""

PERSONAL_MESSAGE_AFTER_REMOVAL = """
We deleted your message because it was found to be toxic. Please refrain from using such messages in the channels. \
Repeated violations will result in stricter actions.
"""

INFO_MESSAGE = """
Hi {username}, this is Mr Toxic Bot. \
I'm responsible for ensuring a friendly environment that promotes social well being in the channel. \
Any message that I deem toxic, insulting, threatening etc will be removed and the author will be given a warning. \
"""

HELP_MESSAGE = """
Hi {username}, this is Mr Toxic Bot. \n
Here's a list of commands you can use to chat with me: \n
- /report - With this command you'll receive the link of the GitHub page of the project to report bugs and issues \n
- /info - You'll receive some info about me :D \n
- /help - You'll receive the list of commands
"""

REPORT_MESSAGE = """
Need something wrong? Here's a link to report that!
"""

ONLY_PRIVATE_DMS = """
Hey {user}, the command can only be invoked by a private DM to ToxicBot.
"""

ADMIN_MESSAGE_AFTER_BOT_JOIN = """
Howdy, I am Mr. Toxic Bot. I am responsible for ensuring that the server is family friendly. \
Any obscene or toxic message sent to the server will be immediately deleted and the author will be warned. \
Here's some configuration that is applied to the server:\n
- Toxic Count before suspending an user : 20\n
- Number of days before previous toxic count history is erased for an user : 14 days

The above configurations can be modified by the server administrator.
"""

REQUISITE_PERMISSION = """
Sorry {user}, you do not have the requisite priviledges to execute the above command.
"""

NOT_BOT_OWNER = """
Sorry {user}, only the owner of the bot can run the above command.
"""

ADMIN_REQUEST_SERVER_ID = """
It seems that you are part of multiple servers. Please select which server you want to get the information about.
"""

ADMIN_CONFIG = """
Here are the current configurations for the server {guild}:\n
- Toxic Count before suspending an user : {count}\n
- Number of days before previous toxic count history is erased for an user : {time} days
"""