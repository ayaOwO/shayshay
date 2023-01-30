import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from commandInterpreter import CommandInterpreter
from LeaferaCode import LeaferaCode

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
        
#leafera
marked_rooms = set()

@client.event
async def on_voice_state_update(member, before, after):
    #open new room and move them in
    marked_rooms.add(await LeaferaCode.OpenOffice(member, before, after))

    # Check if the new room is now empty
    if before.channel is not None and before.channel.id in marked_rooms and len(before.channel.members) == 0:
        await before.channel.delete()

@client.event
async def on_voice_channel_delete(channel):
    # Remove the room from the set of marked rooms
    marked_rooms.discard(channel.id)


# running bot
file = open("bot.token")
token = file.read()
file.close()
print(f'token is {token}')
client.run(token)
