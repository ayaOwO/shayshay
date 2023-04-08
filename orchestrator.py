import logging
from logging.handlers import RotatingFileHandler
from discord.ext import commands

import discord

from commandInterpreter import CommandInterpreter


class Orchestrator():
    def create_logger(self):
        logger = logging.Logger("shayshay")
        formatter = logging.Formatter(fmt="%(asctime)s :: %(levelname)s :: %(message)s")
        handler = RotatingFileHandler("./logs/shayshay.log", backupCount=10)
        handler.formatter = formatter
        logger.addHandler(handler)
        logging.Formatter = formatter

        return logger

    def create_token(self):
        with open("bot.token") as token_file:
            token = token_file.read()
        print(f'token is {token}')
        return token

    def create_command_interpreter(self, logger, help_file_name):
        return CommandInterpreter(logger, help_file_name)

    def create_intents(self):
        intents = discord.Intents.default()
        intents.message_content = True

        return intents

    def create_bot(self, pre):
        intents = self.create_intents()
        bot = commands.Bot(command_prefix=pre, intents=intents)

        return bot

    def create_client(self):
        intents = self.create_intents()
        return discord.Client(intents=intents)
