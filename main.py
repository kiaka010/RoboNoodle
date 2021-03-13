import os
import random
import discord
import requests
from discord.ext import commands
import logging
import aiocron
from bs4 import BeautifulSoup

import requests_cache
requests_cache.install_cache('system_cache', backend='sqlite', expire_after=1)


from src.plugins.compliment import *

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')
logger = logging.getLogger("discord")
bot = commands.Bot(command_prefix=PREFIX)


async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')


@bot.command("dankerbeef")
async def dankerbeef(ctx):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': os.getenv('YOUTUBE_API_KEY'),
        'channelId': 'UCsv2pj6rM1hM5YloMDZdGwA',
        'order': "date",
        'maxResults': 200
    }
    response = requests.get(url, params=params, expire_after=3600)
    logger.info("Is request cached: %s" % response.from_cache)
    logger.info(response)

    if response.status_code != 200:
        logger.error("A compliment Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return
    video_list = []
    video_list += response.json()['items']
    # logger.info(video_list)
    if 'nextPageToken' in response.json():
        while 'nextPageToken' in response.json():
            logger.info("Requesting next page %s" % response.json()['nextPageToken'])
            params['pageToken'] = response.json()['nextPageToken']
            response = requests.get(url, params=params, expire_after=3600)
            logger.info("Is request cached: %s" % response.from_cache)

            logger.info(response)

            if response.status_code != 200:
                logger.error("A compliment Request Failed")
                await ctx.send("Sorry something went wrong. Please try again later.....or not")
                return

            video_list += response.json()['items']
    # logger.info(video_list)
    random_video = random.choice(video_list)
    await ctx.send("https://www.youtube.com/watch?v=%s" % random_video['id']['videoId'])


# @aiocron.crontab('* * * * *')  # every min
@aiocron.crontab('1 0 * * *')  # 1 min past midnight
async def midnight_process():
    channel = bot.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
    await channel.send("Enjoy your daily Danker Beef vid")

    await dankerbeef(channel)
#
@bot.command("idea")
async def idea(ctx):
    idea = ctx.message.clean_content.replace(PREFIX + "idea", "")

    author_name = ctx.author.name
    url = "https://api.trello.com/1/cards"
    params = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN'),
        'idList': '604ab9e2028f1f3c06e42389',
        'name': "(%s) %s" % (author_name, idea),
    }
    logger.info(params)
    response = requests.request('POST', url, params=params)
    logger.info("Is request cached: %s" % response.from_cache)

    logger.info(response)

    if response.status_code != 200:
        logger.error("A compliment Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    # thumbs up message

    await ctx.message.add_reaction('\U0001f44d')


@bot.command("compliment")
async def compliment(ctx):
    await givelove.invoke(ctx)


@bot.command("give-love")
async def give_love(ctx):
    await givelove.invoke(ctx)


@bot.command("givelove")
async def givelove(ctx):
    # logger.info(ctx.channel.members)
    url = "https://complimentr.com/api"
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers)
    logger.info("Is request cached: %s" % response.from_cache)

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
    logger.info("Is request cached: %s" % response.from_cache)
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


@bot.command("dadjoke")
async def dadjoke(ctx):

    url = "https://icanhazdadjoke.com/"
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers)
    logger.info("Is request cached: %s" % response.from_cache)
    logger.info(response)

    if response.status_code != 200:
        logger.error("A Dad Joke Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    joke = ""
    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            logger.info(mention)
            joke += "<@%s> " % mention.id
    joke += response.json()['joke']

    await ctx.send(joke)

@bot.command("pickup")
async def pickup(ctx):

    url = "http://www.pickuplinegen.com/"

    response = requests.get(url)

    response = requests.request('GET', url)
    logger.info("Is request cached: %s" % response.from_cache)
    logger.info(response)

    if response.status_code != 200:
        logger.error("A Pickup Line Request Failed")
        await ctx.send("Sorry something went wrong. Please try again later.....or not")
        return

    pickup = ""
    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            logger.info(mention)
            pickup += "<@%s> " % mention.id

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.select("#content")[0]
    pickup += content.text

    await ctx.send(pickup)


def main():
    # logging.basicConfig(level=logging.DEBUG)

    logger.setLevel(logging.DEBUG)
    # logger.info(TOKEN)
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
    
    # logger.info(TOKEN)
    bot.run(TOKEN)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Exiting System")