import json # shabat
import requests
import math

class CommandInterpreter:
    def __init__(self):
        pass

    def chooseCommand(self, message, text):
        response = ""

        if text in ["מתי אבישי", "מתי אבישישי", "מתי אבשישי", "מתי שבת"]:
            response = self.getShabat()
        elif text in ["כאפה לאבישי", "כאפה לאבשישי"]:
            response = self.slap()
        elif text in ["מי הוא אבישי", "מי הוא אבשישי", "מי אבישי", "מי אבשישי"]:
            response = self.avishayHater()
        elif text in ["עזרה", "חלפ"]:
            response = self.helpCommand()
        elif (text.split(" ")[0] == "כאפה"):
            response = self.genericSlap(text.split(" ")[-1])
        elif text in ["דקירה"]:
            response = self.stab()
        elif text == "":
            "LAst command"
        elif message.author.id == 237622399573557249 and message.content.startswith("היי"):
            response = "היי רון, אני שישי"
        else:
            # repeat last command
            pass

        return response

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
    3. שישי כאפה לגיא
    4. שישי מי הוא אבישי
    5. שישי דקירה```
    """

    def guySlap(self):
        return "Slap:wave: <@923925364756078594>"

    def genericSlap(self, username):
        if (username.startswith("ל")):
            username = username[1:]
        return f"Slap:wave: {username}"


    def getYomKippur(self):
        output = "```css"
        try:
            for event in json.loads(requests.get("https://www.hebcal.com/shabbat?cfg=json;geonameid=293397").text)["items"]:
                if "memo" in event.keys() and event["memo"] == "Erev Yom Kippur":
                    startTimeObj = extractTime(event)
                    output += startTimeObj.strftime("\nStart: %H:%M   %d.%m")
                elif "memo" in event.keys() and event["memo"] == "Yom Kippur":
                    endTimeObj = extractTime(event)
                    output += endTimeObj.strftime("\nEnd:   %H:%M   %d.%m")
            return output + prettyPrintTime(startTimeObj, endTimeObj, "Time until the start of the chom", "Time left until you can eat", "you can eat! do eat! now!")
        except Exception as e:
            return "An error has accurred!\nPlease try again at a later date\nMake sure to let <@280034350051885057> know"



    def extractTime(event):
        time = event["date"].split("T")
        time[0] = time[0].split("-")
        time[1] = time[1].split(":")
        return datetime.datetime(int(time[0][0]), int(time[0][1]), int(time[0][2]), int(time[1][0]), int(time[1][1]))

    def prettyPrintTime(start, end, until, happening, happened):
        if (datetime.datetime.now() > end):  # after the event ended
            output = "\n\n" + happened + "```"
        elif (datetime.datetime.now() > start):  # in the event
            diff = end - datetime.datetime.now()
            output = "\n\n" + happening + ":\n"
            tot = diff.total_seconds()
            output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(math.floor(tot / 60/60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games```"
        else:  # before the event
            diff = start - datetime.datetime.now() # get diff
            output = "\n\n" + until + ":\n"
            tot = diff.total_seconds()
            output += str(math.floor(tot)) + " seconds\n" + str(math.floor(tot / 60)) + " minutes\n" + str(math.floor(tot / 60/60)) + " hours\n" + str(math.floor(tot / 60 / 30)) + " average lol games```"
        return output

    def getShabat(self):
        output = "```css"
        startTimeObj = ""
        endTimeObj = ""
        try:
            for event in json.loads(requests.get("https://www.hebcal.com/shabbat?cfg=json;geonameid=293397").text)["items"]:
                if ("title_orig" in event.keys() and event["title_orig"] == "Candle lighting" and startTimeObj == ""):
                    startTimeObj = extractTime(event)
                    output += startTimeObj.strftime("\nStart: %H:%M   %d.%m")
                elif ("title_orig" in event.keys() and event["title_orig"] == "Havdalah" and endTimeObj == ""):
                    endTimeObj = extractTime(event)
                    output += endTimeObj.strftime("\nEnd:   %H:%M   %d.%m")
        
            return output + prettyPrintTime(startTimeObj, endTimeObj, "time left with avishay", "Time until avishay comes back", "Avishay is here!!")
        except Exception as e:
            with open("log.txt", "a") as logFile:
                logFile.write(f"{e}")
            return "An error has accurred!\nPlease try again at a later date\nMake sure to let <@280034350051885057> know"
