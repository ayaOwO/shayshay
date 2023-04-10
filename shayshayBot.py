from orchestrator import Orchestrator

import discord
from discord import app_commands
from datetime import datetime

orchestrator = Orchestrator()
help_file_name = "help.txt"
logger = orchestrator.create_logger("shayshay")

command_interpreter = orchestrator.create_command_interpreter(logger, help_file_name)
pre = "שישי"
client = orchestrator.create_client()
tree = app_commands.CommandTree(client)

# functions
server_id = 843477859020308510


# try client.command
@tree.command(name="שבת", description="Tells you when Avishay comes back, so the grind can continue")
async def app_get_shabat(ctx):
    await ctx.response.send_message(command_interpreter.get_shabat("hello אבישי"))


@client.event
async def on_ready():
    guild = discord.Object(id=server_id)
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
    guilds_data = []
    for guild in client.guilds:
        guilds_data.append(f"Server: {guild.name}::id: {guild.id}::Members count: {len(guild.members)}")
    logger.info("<->".join(guilds_data))
    logger.info("started")


@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        if message.content.startswith(pre):
            text = message.content[len(pre):].strip()

            if message.guild is not None:
                logging_data = (str(message.id), message.guild.name, message.channel.name, message.author.name, text)
                identifier = message.guild.id
            else:
                identifier = message.author.id
                logging_data = (str(message.id), message.author.name, text)
            logger.info("<->".join(logging_data))

            response, file = command_interpreter.choose_command(message, text, identifier)

            logging_data = (str(message.id), response)
            logger.info("<->".join(logging_data))

            if response != "":
                await message.channel.send(response, file=file)

    except Exception as e:
        logger.error(e)
        raise


# running bot
token = orchestrator.create_token()
client.run(token)
