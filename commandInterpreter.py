from datetime import datetime
import json

import discord
import requests
import math

from PIL import Image
from requests import get
from io import BytesIO


class CommandInterpreter:
    last_command = {}

    def __init__(self, help_file_name):
        self.help_file_name = help_file_name

    def choose_command(self, message, text, identifier):
        response = ""
        file = None

        if text == "":
            if identifier in self.last_command:
                server_last_command = self.last_command[identifier]
                if None not in server_last_command:
                    message, text = server_last_command[0], server_last_command[1]

        if len(text.split(" ")) == 2 and text.split(" ")[0] == "מתי":
            response = self.get_shabat(text)
        elif text in ["כאפה לאבישי", "כאפה לאבשישי"]:
            response = self.slap()
        elif text in ["מי הוא אבישי", "מי הוא אבשישי", "מי אבישי", "מי אבשישי"]:
            response = self.avishay_hater()
        elif text in ["עזרה", "חלפ"]:
            response = self.help_command()
        elif text.split(" ")[0] == "כאפה":
            if len(text.split(" ")) == 2:
                response = self.generic_slap(text.split(" ")[1])
        elif text.split(" ")[0] == "חיבוק":
            if len(text.split(" ")) == 2:
                response = self.generic_hug(text.split(" ")[1])
        elif text in ["דקירה"]:
            response = self.stab()
        elif text in ["דאמ"]:
            response = self.damn()
        elif message.author.id == 237622399573557249 and message.content.startswith("הי"):
            response = "היי רון, אני שישי"
        if text in ["אני פיתה"]:
            response, file = self.get_pita(message.author.id)
        else:
            pass

        if response != "" and text != "אני פיתה":
            self.last_command[identifier] = (message, text)
        return response, file

    def damn(self):
        return "מה קשור דאמ"

    def stab(self):
        return "🔪 🩸"

    def slap(self):
        return "Slap:wave: <@375656966145703946>"

    def avishay_hater(self):
        return "אבישי הייטר"

    def give_cookie(self):
        return ":cookie:"

    def help_command(self):
        with open(self.help_file_name, "r") as help_file:
            text = help_file.read()
        return text

    def generic_hug(self, username):
        gifs = ["https://tenor.com/view/love-gif-25904467"]
        index = 0
        if username.startswith("ל"):
            username = username[1:]
        if not username.startswith("<"):
            return ""
        return f"{username}\n{gifs[index]}"

    def generic_slap(self, username):
        if username.startswith("ל"):
            username = username[1:]
        if not username.startswith("<"):
            return ""
        return f"Slap:wave: {username}"

    def _extract_time(self, event):
        time = event["date"].split("T")
        time[0] = time[0].split("-")
        time[1] = time[1].split(":")
        return datetime(int(time[0][0]), int(time[0][1]), int(time[0][2]), int(time[1][0]), int(time[1][1]))

    def _format_time(self, start, end, until, happening, happened):
        if datetime.now() > end:  # after the event ended
            output = "\n\n" + happened
        elif datetime.now() > start:  # in the event
            diff = end - datetime.now()
            output = "\n\n" + happening + ":\n"
            tot = diff.total_seconds()
            output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(
                math.floor(tot / 60 / 60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games"
        else:  # before the event
            diff = start - datetime.now()  # get diff
            output = "\n\n" + until + ":\n"
            tot = diff.total_seconds()
            output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(
                math.floor(tot / 60 / 60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games"
        return output

    def _format_get_shabat(self, shabat_times, input_name):
        output = "```css"
        output += shabat_times[0].strftime("\nStart: %H:%M   %d.%m")
        output += shabat_times[1].strftime("\nEnd:   %H:%M   %d.%m")
        names = {"אבישי": "Avishay", "אבשישי": "Avishay", "אבישישי": "Avishay", "אמיר": "Amir", "שבת": "Shabat"}
        if input_name in names:
            name = names[input_name]
        else:
            name = input_name
        output += self._format_time(shabat_times[0], shabat_times[1], f"Time left with {name}",
                                    f"Time until {name} comes back", f"{name} is here!!")
        return output + "```"

    def get_shabat(self, text):
        shabat_times = self._get_shabat_times()
        name = text.split(" ")[1]
        return self._format_get_shabat(shabat_times, name)

    def _get_shabat_times(self):
        shabat_times = [None, None]
        try:
            for event in json.loads(requests.get("https://www.hebcal.com/shabbat?cfg=json;geonameid=293397").text)["items"]:
                if "title_orig" in event.keys() and event["title_orig"] == "Candle lighting" and shabat_times[0] is None:
                    shabat_times[0] = self._extract_time(event)
                elif "title_orig" in event.keys() and event["title_orig"] == "Havdalah" and shabat_times[1] is None:
                    shabat_times[1] = self._extract_time(event)
            return shabat_times
        except Exception as e:
            with open("log.txt", "a") as logFile:
                logFile.write(f"{e}")
            return "An error has accurred!\nPlease try again at a later date\nMake sure to let <@280034350051885057> know"

    def get_pita(self, userid):
        discord_api = "https://discord.com/api"
        discord_cdn = "https://cdn.discordapp.com"

        with open("bot.token", "r") as f:
            token = f.read().rstrip("\n")
        headers = {
            'authorization': f'Bot {token}'
        }

        url = f"{discord_api}/users/{userid}"
        res = get(url, headers=headers)
        avatar_token = res.json()["avatar"]

        res = get(f"{discord_cdn}/avatars/{userid}/{avatar_token}.png?size=64")
        file = BytesIO(res.content)
        pfp = Image.open(file).convert('RGBA')

        pita = Image.open("pita.png").convert('RGBA')
        center_width, center_height = pita.size
        center_width, center_height = (center_width // 2 - pfp.size[0] // 2, center_height // 2 - pfp.size[1] // 2)

        pita.paste(pfp, (center_width, center_height), pfp)
        pita.save("me.png")
        return "בתיאבון" + " " + f"<@{userid}>", discord.File("me.png")
