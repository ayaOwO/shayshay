import discord
from discord import app_commands 
from discord.ext import tasks, commands
import datetime
from commandInterpreter import CommandInterpreter

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# functions
pre = "שישי"
command_inteprpreter = CommandInterpreter()
bot = commands.Bot(command_prefix=pre, intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="שבת", description="Tells you when avishays comes back, so the grind can continue", guild=discord.Object(id=843477859020308510))
async def AppGetShabat(ctx):
    await ctx.response.send_message(command_inteprpreter.getShabat())

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=843477859020308510))

@client.event
async def on_message(message):
    try:
        global lastCommand
        if (message.author == client.user):
            return

        if message.content.startswith(pre):
            text = message.content[len(pre):].strip()
            response = command_inteprpreter.chooseCommand(message, text)
            await message.channel.send(response)

    except Exception as e:
        with open("log.txt", "w") as filer:
            filer.write(e)
            filer.write(datetime.now())
        raise


# running bot
file = open("bot.token")
token = file.read()
file.close()
print(f'token is {token}')
client.run(token) 

