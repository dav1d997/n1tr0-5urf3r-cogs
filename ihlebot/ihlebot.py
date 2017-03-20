import discord
from discord.ext import commands
import os
import time
from .utils import checks
from cogs import * #dataIO, fileIO
from __main__ import send_cmd_help

# Used for DNS lookup
import socket
# Used for regexp
import re
# Used for ping
import os
# General stuff for discord
import asyncio
import aiohttp
import datetime


class Ihlebot:
    """ Command definitions"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def __unload(self):
        self.session.close()

    @commands.group(pass_context=True)
    async def ihle(self, ctx):
        """First Test, Commandcall"""
        await self.bot.say('Ihle ist der beste!')

    @commands.command(pass_context=True)
    async def beleidige(self, ctx, name):
        """Second Test, Variablenverarbeitung"""
        msg = await self.bot.say(name + ' ist ein Behindi!')
        await self.bot.add_reaction(msg,'😲')

    @commands.command(pass_context=True)
    async def emojis(self, ctx):
        """Returns a list of all Server Emojis"""
        server = ctx.message.server
        await self.bot.say('This may take some time, generating list...')
        data = discord.Embed(description="Emojilist")
        for ej in server.emojis:
            data.add_field(name=ej.name, value=str(ej) + " " + ej.id, inline=False)
        await self.bot.say(embed=data)

#    @commands.command(pass_context=True)
#    async def create(self, ctx):
#        """Create custom emojis"""
#        server = ctx.message.server
#        with open('/opt/Red-DiscordBot/cogs/icon.png', 'rb') as imageFile:
#            f = imageFile.read()
#        await self.bot.create_custom_emoji(server, 'temp', f)

    @commands.command(pass_context=True)
    async def ping(self, ctx, ip):
        """Check if Server is online"""

        # Check for valid IP
        valid_ip = re.compile("[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}")
        valid_hostname = re.compile(".*\.[a-zA-Z]{2,}")
        valid = False

        if valid_ip.match(ip):
            valid = True
        elif valid_hostname.match(ip):
            valid = True
            await self.bot.say('Doing DNS lookup...')
            ip = socket.gethostbyname('ip')
            await self.bot.say('DEBUG: looked up ip is '+ip)
        if valid == True:
            start = time.time()
            response = os.system("sudo ping -c 1 -w3 " + ip)
            duration = time.time() - start
            duration = round(duration * 1000, 0)
            if response == 0:
                await self.bot.say(ip + ' is up and responding in ' + str(duration) + 'ms.')
            else:
                await self.bot.say(ip + ' is not reachable.')
        else:
            await self.bot.say(ip + ' is not valid.')


def setup(bot):
    n = Ihlebot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)