import logging
import random

from .abstract_plugin import AbstractPlugin
from discord.ext import commands
import discord
import ffmpeg
import json
import os
from src.utils.request import Request
from bs4 import BeautifulSoup

class Voice(AbstractPlugin):

    async def _get_message(self, ctx, message):
        self.logger.info(message[:1])
        self.logger.info(message[1:])
        if os.getenv('DISCORD_PREFIX') == message[:1]:
            if " " in message[1:]:
                command, query = message[1:].split(" ", 1)
            else:
                command = message[1:]

            self.logger.info('Found cascade command')
            response = await ctx.invoke(self.bot.get_command(command))
            self.logger.info(response)
            if response:
                return response

        return ctx.message.clean_content.replace(os.getenv('DISCORD_PREFIX') + "say", "")\
            .replace(os.getenv('DISCORD_PREFIX') + "speak", "")\
            .replace(os.getenv('DISCORD_PREFIX') + "play", "")\
            .replace("@", "")

    @commands.command(aliases=['speak'], help="Make me say something, or speak another command")
    async def say(self, ctx, *, message):

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel for this to work")
            return
        channel = ctx.author.voice.channel

        new_message = await self._get_message(ctx, message)

        voice_type = None

        with open('src/data/voice_details.json', 'r') as f:
            voice_details = json.load(f)
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)
            if guild_id in voice_details['data'] and author_id in voice_details['data'][guild_id]:
                voice_type = voice_details['data'][guild_id][author_id]
            # f.close()

        if voice_type and voice_type in voice_details['options']:
            url = voice_details['options'][voice_type]
        else:
            url = voice_details['options'][random.choice(list(voice_details['options']))]

        self.logger.info(url)

        data = {
            'but': "submit",
            'but1': new_message
        }

        response = Request().post(url, data=data, expire_after=1800)
        if not response:
            await ctx.send("Sorry something went wrong. Please try again later.....or not")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.findAll("source")

        if not content:
            self.logger.info("Content Not found")
            return
        self.logger.info(content[0])
        if not content[0]['src']:
            self.logger.info("Src Not found")
            return

        audio_path = content[0]['src']
        self.logger.info(audio_path)

        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)

        audio_source = discord.FFmpegPCMAudio('https://readloud.net' + audio_path, options='-filter:a "atempo=0.85"')

        # maybe better join example
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            voice_client = await channel.connect()

        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)

        await ctx.message.add_reaction('\U0001f44d')

    @commands.group(pass_context=True, help="Commands to control me in voice - including what voice you want me to use")
    async def vc(self, ctx):
        if ctx.invoked_subcommand:
            self.logger.info("inside ferdo love - Sub Command Called")
            return

    @vc.group(name="set-voice", pass_context=True,
              brief="- pass one of the options (m or f (for now)) to choose what voice i use for you",
              description="Pass one of the options (m or f (for now)) to choose what voice i use for you"
              )
    async def set_voice(self, ctx, voice_type):
        self.logger.info("im being asked to set Guild: %s Author: %s: VoiceType: %s" %
             (
                ctx.guild.id,
                ctx.author.id,
                voice_type
             )
         )

        with open('src/data/voice_details.json', 'r') as f:
            voice_details = json.load(f)
            if voice_type not in voice_details['options']:
                await ctx.send("Sorry only the following options are allowed %s" %
                               ', '.join(voice_details['options'].keys())
                               )
                return
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)

            if guild_id not in voice_details['data']:
                voice_details['data'][guild_id] = {}
            voice_details['data'][guild_id][author_id] = voice_type
            f.close()
        with open('src/data/voice_details.json', 'w') as f:
            json.dump(voice_details, f, indent=4)
            f.close()
            await ctx.message.add_reaction('\U0001f44d')


    # @vc.group(pass_context=True)
    # async def leave(self, ctx):
    # @todo: current does not work, no option disconect avalable under voice channel
    #
    #     channel = ctx.author.voice.channel
    #     await channel.disconect()

    @vc.group(pass_context=True,
              brief="- Join a voice channel",
              description="Join a voice channel"
              )
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
