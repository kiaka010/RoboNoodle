import os

import requests
from discord.ext import commands
import logging
from src.plugins.compliment import *

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')
logger = logging.getLogger("discord")
bot = commands.Bot(command_prefix=PREFIX)


async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')


@bot.command("compliment", pass_context=True)
async def compliment(ctx):
    await givelove.invoke(ctx)


@bot.command("give-love")
async def give_love(ctx):
    await givelove.invoke(ctx)


@bot.command("givelove")
async def givelove(ctx):
    url = "https://complimentr.com/api"
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers)
    logger.info(response)

    if response.status_code != 200:
        logger.error("A compliment Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    compliment = ""
    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            logger.info(mention)
            compliment += "<@%s> " % mention.id
    compliment += response.json()['compliment']

    await ctx.send(compliment)


@bot.command("roast")
async def roast(ctx):

    url = "https://www.rappad.co/api/battles/random_insult"
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers)
    logger.info(response)

    if response.status_code != 200:
        logger.error("A Roast Battle Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    insult = ""
    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            logger.info(mention)
            insult += "<@%s> " % mention.id
    insult += response.json()['insult']

    await ctx.send(insult)


def main():
    logger.setLevel(logging.DEBUG)
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', filename='')
    logging.getLogger('discord').setLevel(logging.DEBUG)

    logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(filename="logs.txt")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    logger.info("Starting")
    logger.info(TOKEN)
    bot.run(TOKEN)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Exiting System")