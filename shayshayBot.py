import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from commandInterpreter import CommandInterpreter

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# functions
server_id = 843477859020308510
pre = "שישי"
command_interpreter = CommandInterpreter()
bot = commands.Bot(command_prefix=pre, intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="שבת", description="Tells you when Avishay comes back, so the grind can continue",
              guild=discord.Object(id=server_id))
async def app_get_shabat(ctx):
    await ctx.response.send_message(command_interpreter.get_shabat("hello אבישי"))


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))


@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        if message.content.startswith(pre):
            text = message.content[len(pre):].strip()
            response, file = command_interpreter.chooseCommand(message, text)
            if response != "":
                await message.channel.send(response, file=file)

    except Exception as e:
        with open("log.txt", "w") as filer:
            filer.write(str(e))
            filer.write("\n")
            filer.write(str(datetime.now()))
        raise


# running bot
token_file = open("bot.token")
token = token_file.read()
token_file.close()
print(f'token is {token}')
client.run(token)
