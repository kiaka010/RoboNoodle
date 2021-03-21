from src.plugins import AbstractPlugin
from discord.ext import commands
import json
import random
import time

"""

!ferdolove (random ferdo love comment)
!ferdolove submit add some flirty comment here (ways for people to submit there own ferdo love note)
!ferdolove list - lists out all the lines already added
!ferrdolove delete number (delete one of the records, but i'll prevent ferdo from foing it)
"""


class FerdoLove(AbstractPlugin):
    ferdo_love_data = {}

    @commands.group(pass_context=True, hidden=True, description="A random quote direct from our beloved Ferdo")
    async def ferdolove(self, ctx):

        with open('src/data/ferdo_love.json') as f:
            self.ferdo_love_data = json.load(f)

        if ctx.invoked_subcommand:
            self.logger.info("inside ferdo love - Sub Command Called")
            return

        await ctx.send(
            '> %s \n Ferdo %s'
            %
            (
                random.choice(self.ferdo_love_data['data'])['message'],
                2021
            )
        )

    @ferdolove.group(pass_context=True, aliases=['submit'],
                     brief="- Add a quote you have heard from our one and only Ferdo",
                     usage=" <message>",
                     # help="h Add a quote you have heard from our one and only Ferdo",
                     # description="d Add a quote you have heard from our one and only Ferdo"
                     )
    async def add(self, ctx, *, message):
        self.logger.info("inside ferdo love - add - with '%s'" % message)

        for existing_message_data in self.ferdo_love_data['data']:
            if message == existing_message_data['message']:
                await ctx.send("That quote has already been added (must be popular)")
                return

        new_ferdo_quote = {
            'user': {},
            'message': message,
            'date_added': time.time()
        }
        new_ferdo_quote['user']['name'] = ctx.author.name
        new_ferdo_quote['user']['id'] = ctx.author.id

        self.ferdo_love_data['data'].append(new_ferdo_quote)
        with open('src/data/ferdo_love.json', 'w') as f:
            json.dump(self.ferdo_love_data, f, indent=4)
            await ctx.message.add_reaction('\U0001f44d')

            # self.ferdo_love_data = json.load(f)

    # @ferdolove.group(pass_context=True, aliases=['delete'])
    # async def remove(self, ctx, number):
    #     self.logger.info("inside ferdo love - delete - with '%s'" % number)

    @ferdolove.group(pass_context=True, hidden=True,
                     brief="- List out 5 quotes at a time currently added - add a page number to see more",
                     description="List out all the quotes currently added - add page number to see more"
                     # short_doc='See all ferdo quotes (add page number to see more)',
                     )
    async def list(self, ctx, page_num=1):
        self.logger.info("inside ferdo love - list")
        messages = self.ferdo_love_data['data']
        paginated_data = [messages[i:i + 5] for i in range(0, len(messages), 5)]
        self.logger.info(paginated_data)
        #
        response = ''
        if len(paginated_data) < page_num:
            await ctx.send('Page Num %s out of range' % page_num)
            return

        for pag in paginated_data[page_num - 1]:
            response += pag['message'] + '\n'

        await ctx.send(response)
