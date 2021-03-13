from .abstract_plugin import AbstractPlugin
from discord.ext import commands
from src.utils.request import Request
from src.utils.message_utils import MessageUtils
import random
import os
import aiocron

"""
NONE OF THIS IS READY YET - HENCE COMMENTED OUT - CRON JOBS NOT WORKING
BUT NEED TO CODE A BETTER ONE ANYWAY
"""


# class DankerBeef(AbstractPlugin):

#     def __init__(self, bot, logger):
#         super().__init__(bot, logger)
#         channel = self.bot.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
#         cron = aiocron.crontab('* * * * *', func=self.dankerbeef, args=(channel), start=True)
#
#     @commands.command("dankerbeef", help="Looking for a Danker Beef video, look no further")
#     async def dankerbeef(self, ctx):
#         url = "https://www.googleapis.com/youtube/v3/search"
#         params = {
#             'key': os.getenv('YOUTUBE_API_KEY'),
#             'channelId': 'UCsv2pj6rM1hM5YloMDZdGwA',
#             'order': "date",
#             'maxResults': 200
#         }
#         response = Request().get(url, params=params, expire_after=3600)
#
#         if not response:
#             await ctx.send("Sorry something went wrong. Please try again later.....or not")
#             return
#
#         video_list = []
#         video_list += response.json()['items']
#
#         if 'nextPageToken' in response.json():
#             while 'nextPageToken' in response.json():
#                 self.logger.info("Requesting next page %s" % response.json()['nextPageToken'])
#                 params['pageToken'] = response.json()['nextPageToken']
#                 response = Request().get(url, params=params, expire_after=3600)
#
#                 if not response:
#                     await ctx.send("Sorry something went wrong. Please try again later.....or not")
#                     return
#
#                 video_list += response.json()['items']
#
#         random_video = random.choice(video_list)
#
#         await ctx.send("https://www.youtube.com/watch?v=%s" % random_video['id']['videoId'])
#
# # @aiocron.crontab('* * * * *')  # every min
# # # @aiocron.crontab('1 0 * * *')  # 1 min past midnight
# # async def midnight_process():
# #     channel = bot.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
# #     # await channel.send("Enjoy your daily Danker Beef vid")
# #
# #     await self.dankerbeef(channel)
