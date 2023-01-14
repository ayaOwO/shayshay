from datetime import datetime
import json
import requests
import math


class CommandInterpreter:
    last_command = [None, None]

    def __init__(self):
        pass

    def chooseCommand(self, message, text):
        response = ""

        if text in ["מתי אבישי", "מתי אבישישי", "מתי אבשישי", "מתי שבת", "מתי אמיר"]:
            response = self.getShabat()
        elif text in ["כאפה לאבישי", "כאפה לאבשישי"]:
            response = self.slap()
        elif text in ["מי הוא אבישי", "מי הוא אבשישי", "מי אבישי", "מי אבשישי"]:
            response = self.avishayHater()
        elif text in ["עזרה", "חלפ"]:
            response = self.helpCommand()
        elif text.split(" ")[0] == "כאפה":
            if len(text.split(" ")) == 2:
                response = self.genericSlap(text.split(" ")[1])
        elif text.split(" ")[0] == "חיבוק":
            if len(text.split(" ")) == 2:
                response = self.genericHug(text.split(" ")[1])
        elif text in ["דקירה"]:
            response = self.stab()
        elif text in ["דאמ"]:
            return self.damn()
        elif text == "":
            if None not in self.last_command:
                response = self.chooseCommand(self.last_command[0], self.last_command[1])
        elif message.author.id == 237622399573557249 and message.content.startswith("הי"):
            response = "היי רון, אני שישי"
        else:
            pass

        if response != "":
            self.last_command = [message, text]
        return response

    def damn(self):
        return "מה קשור דאמ"

    def stab(self):
        return "🔪 🩸"

    def slap(self):
        return "Slap:wave: <@375656966145703946>"

    def avishayHater(self):
        return "אבישי הייטר"

    def giveCookie(self):
        return ":cookie:"

    def helpCommand(self):
        return """```
פקודות:
1. שישי מתי אבישי
2. שישי כאפה לאבישי
3. שישי כאפה @שם
4. שישי מי הוא אבישי
5. שישי דקירה
6. שישי דאמ```
    """

    def genericHug(self, username):
        gifs = ["https://tenor.com/view/love-gif-25904467"]
        index = 0
        if username.startswith("ל"):
            username = username[1:]
        if not username.startswith("<"):
            return ""
        return f"{username}\n{gifs[index]}"

    def genericSlap(self, username):
        if username.startswith("ל"):
            username = username[1:]
        if not username.startswith("<"):
            return ""
        return f"Slap:wave: {username}"

    def getYomKippur(self):
        output = "```css"
        try:
            for event in json.loads(requests.get("https://www.hebcal.com/shabbat?cfg=json;geonameid=293397").text)[
                "items"]:
                if "memo" in event.keys() and event["memo"] == "Erev Yom Kippur":
                    startTimeObj = self.extractTime(event)
                    output += startTimeObj.strftime("\nStart: %H:%M   %d.%m")
                elif "memo" in event.keys() and event["memo"] == "Yom Kippur":
                    endTimeObj = self.extractTime(event)
                    output += endTimeObj.strftime("\nEnd:   %H:%M   %d.%m")
            return output + self.prettyPrintTime(startTimeObj, endTimeObj, "Time until the start of the chom",
                                                 "Time left until you can eat", "you can eat! do eat! now!")
        except Exception as e:
            return "An error has accurred!\nPlease try again at a later date\nMake sure to let <@280034350051885057> know"

    def extractTime(self, event):
        time = event["date"].split("T")
        time[0] = time[0].split("-")
        time[1] = time[1].split(":")
        return datetime(int(time[0][0]), int(time[0][1]), int(time[0][2]), int(time[1][0]), int(time[1][1]))

    def prettyPrintTime(self, start, end, until, happening, happened):
        if datetime.now() > end:  # after the event ended
            output = "\n\n" + happened + "```"
        elif datetime.now() > start:  # in the event
            diff = end - datetime.now()
            output = "\n\n" + happening + ":\n"
            tot = diff.total_seconds()
            output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(
                math.floor(tot / 60 / 60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games```"
        else:  # before the event
            diff = start - datetime.now()  # get diff
            output = "\n\n" + until + ":\n"
            tot = diff.total_seconds()
            output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(
                math.floor(tot / 60 / 60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games```"
        return output

    def getShabat(self):
        output = "```css"
        startTimeObj = ""
        endTimeObj = ""
        try:
            for event in json.loads(requests.get("https://www.hebcal.com/shabbat?cfg=json;geonameid=293397").text)[
                "items"]:
                if ("title_orig" in event.keys() and event["title_orig"] == "Candle lighting" and startTimeObj == ""):
                    startTimeObj = self.extractTime(event)
                    output += startTimeObj.strftime("\nStart: %H:%M   %d.%m")
                elif ("title_orig" in event.keys() and event["title_orig"] == "Havdalah" and endTimeObj == ""):
                    endTimeObj = self.extractTime(event)
                    output += endTimeObj.strftime("\nEnd:   %H:%M   %d.%m")

            return output + self.prettyPrintTime(startTimeObj, endTimeObj, "time left with avishay",
                                                 "Time until avishay comes back", "Avishay is here!!")
        except Exception as e:
            with open("log.txt", "a") as logFile:
                logFile.write(f"{e}")
            return "An error has accurred!\nPlease try again at a later date\nMake sure to let <@280034350051885057> know"
