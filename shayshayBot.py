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
    output = "```css"

    for event in json.loads(requests.get("https://www.hebcal.com/shabbat?cfg=json;geonameid=294421").text)["items"]:
        if ("title_orig" in event.keys() and event["title_orig"] == "Candle lighting"):
            startTimeObj = extractTime(event)
            if (startTimeObj.weekday() == 4):  # shabat starts at Friday
                output += startTimeObj.strftime("\nStart: %H:%M   %d.%m")
        elif ("title_orig" in event.keys() and event["title_orig"] == "Havdalah"):
            endTimeObj = extractTime(event)
            if (endTimeObj.weekday() == 5):  # shabat ends at Saturday
                output += endTimeObj.strftime("\nEnd:   %H:%M   %d.%m")
    return output + prettyPrintTime(startTimeObj, endTimeObj, "avishay comes back", "Avishay is here!!")

def slap():
    return "Slap:wave: <@375656966145703946>"

def avishayHater():
    return "אבישי הייטר"
def giveCookie():
    return ":cookie:"

def getItay():
    #workEnd = datetime.datetime(18, 0)
    return "Time left with Itay:\n" #, datetime.datetime(18, 0) - datetime.datetime.now()
 

def getYomKippur():
    for event in json.loads(requests.get("https://www.hebcal.com/shabbat?cfg=json;geonameid=294421").text)["items"]:
        if "title" in event.keys() and event["title"] == "Erev Yom Kippur":
            print("hu")

    return 1#prettyPrintTime()


def extractTime(event):
    time = event["date"].split("T")
    time[0] = time[0].split("-")
    time[1] = time[1].split(":")
    return datetime.datetime(int(time[0][0]), int(time[0][1]), int(time[0][2]), int(time[1][0]), int(time[1][1]))

def prettyPrintTime(start, end, until, happened):
    if (datetime.datetime.now() > end):
        output = "\n\n" + happened + "```"
    elif (datetime.datetime.now() > start):
        diff = end - datetime.datetime.now()
        output = "\n\nTime until" + until + ":\n"
        tot = diff.total_seconds()
        output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(math.floor(tot / 60/60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games```"
    else:
        diff = start - datetime.datetime.now() # get diff
        output = "\n\nTime left with avishay:\n"
        tot = diff.total_seconds()
        output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(math.floor(tot / 60/60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games```"
    return output


commands = {"מתי אבישי": getShabat, "מתי אבישישי": getShabat, "מתי אבשישי": getShabat, "מתי שבת": getShabat,
    "כאפה לאבישי": slap, "כאפה לאבשישי": slap,
    "מי הוא אבישי": avishayHater, "מי הוא אבשישי": avishayHater, "מי אבישי": avishayHater, "מי אבשישי": avishayHater,
    "מתי איתי": getItay,
    "שישי אני רעב": getYomKippur, "שישי אני רעבה": getYomKippur}

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
