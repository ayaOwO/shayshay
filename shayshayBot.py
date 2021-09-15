import discord
from discord.ext import tasks, commands
import json # shabat
import requests
import datetime
import math

client = discord.Client()
# functions
bot = commands.Bot(command_prefix='שישי')

pre = "שישי"
def getShabat():
    output = "```css\nStart: "

    for event in json.loads(requests.get("https://www.hebcal.com/shabbat?cfg=json;geonameid=294421").text)["items"]:
        if ("title_orig" in event.keys() and event["title_orig"] == "Candle lighting"):
            #date = daytime.date(2021)
            startTime = event["date"].split("T")
            startTime[0] = startTime[0].split("-")
            startTime[1] = startTime[1].split(":")
            startTimeObj = datetime.datetime(int(startTime[0][0]), int(startTime[0][1]), int(startTime[0][2]), int(startTime[1][0]), int(startTime[1][1]))
            output += startTime[1][0] + ":" + startTime[1][1] + "   " + ".".join(startTime[0][:0:-1]) + "\nEnd:   "
        elif ("title_orig" in event.keys() and event["title_orig"] == "Havdalah"):
            #output += event["title"][event["title"].find(':')+2:] + " " + event["date"][5:10]
            endTime = event["date"].split("T")
            endTime[0] = endTime[0].split("-")
            endTime[1] = endTime[1].split(":")
            endTimeObj = datetime.datetime(int(endTime[0][0]), int(endTime[0][1]), int(endTime[0][2]), int(endTime[1][0]), int(endTime[1][1]))
            output += endTime[1][0] + ":" + endTime[1][1] + "   " + ".".join(endTime[0][:0:-1])
    if (datetime.datetime.now() > endTimeObj):
        output += "\n\nAvishay is here!!```"
    elif (datetime.datetime.now() > startTimeObj):
        diff = endTimeObj - datetime.datetime.now()
        output += "\n\nTime until avishay comes back:\n"
        tot = diff.total_seconds()
        output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(math.floor(tot / 60/60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games```"
    else:
        diff = startTimeObj - datetime.datetime.now() # get diff
        output += "\n\nTime left with avishay:\n"
        tot = diff.total_seconds()
        output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(math.floor(tot / 60/60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games```"
    return output

def slap():
    return "Slap:wave: <@375656966145703946>"

def avishayHater():
    return "אבישי הייטר"
def giveCookie():
    return ":cookie:"

def getItay():
    #workEnd = datetime.datetime(18, 0)
    return "Time left with Itay:\n" #, datetime.datetime(18, 0) - datetime.datetime.now()
    

#shabatChannel = client.get_channel(863821474951725086)
#print(shabatChannel)
#shabatChannel.send('hello')
commands = {"מתי אבישי": getShabat, "מתי אבישישי": getShabat, "מתי אבשישי": getShabat, "מתי שבת": getShabat,
    "כאפה לאבישי": slap, "כאפה לאבשישי": slap,
    "מי הוא אבישי": avishayHater, "מי הוא אבשישי": avishayHater, "מי אבישי": avishayHater, "מי אבשישי": avishayHater,
    "מתי איתי": getItay}

@client.event
async def on_ready():
    print("LOGGED IN", client.user)
@client.event

async def on_message(message):
    if (message.author == client.user):
        return

    if message.content.startswith(pre):
        msg = message.content[len(pre):].strip()
        if (msg in commands):
            await message.channel.send(commands[msg.strip()]())

# running bot
file = open("bot.token")
token = file.read()
file.close()
client.run(token) 
