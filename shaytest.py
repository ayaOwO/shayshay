import discord
from discord.ext import commands

class MyClient(discord.Client):
    async def on_ready(self)
        print(f"Logged on as {self.user}")

@bot.command(name="את בסדר?"):
async def get_temp(con):
    await context.send("yes")

client = MyClient()
file = open("bot.token")
token = file.read()
file.close()
print(f'token is {token}')
client.run(token)

