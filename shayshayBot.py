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
async def AppGetShabat(ctx):
    await ctx.response.send_message(command_interpreter.getShabat())


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
            response = command_interpreter.chooseCommand(message, text)
            if response != "":
                await message.channel.send(response)

    except Exception as e:
        with open("log.txt", "w") as filer:
            filer.write(str(e))
            filer.write("\n")
            filer.write(str(datetime.now()))
        raise


# running bot
file = open("bot.token")
token = file.read()
file.close()
print(f'token is {token}')
client.run(token)
