import discord
from discord.ext import commands
import time

# Used for DNS lookup
import socket
# Used for regexp
import re
# Used for ping
import os
from random import randint
import random
# General stuff for discord
import asyncio
import aiohttp
import urllib.request, json

import datetime
import requests

client = discord.Client()


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
        game = discord.Game(name='Justified Loyalty')
        await self.bot.change_status(game)

    @commands.command(pass_context=True)
    async def beleidige(self, ctx, name):
        """Second Test, Variablenverarbeitung"""
        msg = await self.bot.say(name + ' ist ein Behindi!')
        await self.bot.add_reaction(msg, '😲')

    @commands.command(pass_context=True)
    async def pizza(self, ctx):
        """Pizza!"""
        pizza_list = [
            'https://media1.giphy.com/media/iThaM3NlpjH0Y/200w.gif',
            'https://media1.giphy.com/media/POmeDOmoTg9CU/200w.gif',
            'https://i.imgur.com/BrXB1VU.gifv',
            'https://media0.giphy.com/media/3o7aDdeZzsZyx4qkqk/200w.gif',
            'https://media0.giphy.com/media/sTUWqCKtxd01W/200w.gif',
            'https://media0.giphy.com/media/YfLdTsfMIfHX2/200w.gif',
            'https://media0.giphy.com/media/AeWntMyxGFXXi/200w.gif',
            'https://media0.giphy.com/media/10kxE34bJPaUO4/giphy.gif',
            'https://media0.giphy.com/media/RRRSdQ6tuUXBu/200w.gif'
        ]

        rng = random.randint(0, len(pizza_list))
        await self.bot.say(pizza_list[rng])

    @commands.command(pass_context=True)
    async def emojis(self, ctx):
        """Returns a list of all Server Emojis"""
        server = ctx.message.server
        await self.bot.say('This may take some time, generating list...')
        data = discord.Embed(description="Emojilist")
        for ej in server.emojis:
            data.add_field(
                name=ej.name, value=str(ej) + " " + ej.id, inline=False)
        await self.bot.say(embed=data)

    @commands.command(pass_context=True)
    async def create(self, ctx):
        """Create custom emojis Currently not working"""
        server = ctx.message.server
        with open('/opt/Red-DiscordBot/cogs/icon.png', 'rb') as imageFile:
            f = imageFile.read()
        await self.bot.create_custom_emoji(server=server, name='temp', image=f)

    @commands.command(pass_context=True)
    async def just(self, ctx):
        """Displays general help information for my guild"""
        user = ctx.message.author
        color = self.getColor(user)

        data = discord.Embed(
            description='Erklärung zu den Befehlen', color=color)
        data.set_author(name='Justified Loyalty')
        data.add_field(
            name='Schlüssel hinzufügen',
            value=
            '*!key add <schlüssel>*  Fügt euren Schlüssel hinzu, wird benötigt, um Daten auszulesen.',
            inline=False)
        data.add_field(
            name='Informationen zur Gilde',
            value='*!guild info Justified Loyalty* (nur für Gildenleader)',
            inline=False)
        data.add_field(
            name='Gildenmitglieder anzeigen',
            value='*!guild members Justified Loyalty* (nur für Gildenleader)',
            inline=False)
        data.add_field(
            name='Inhalt der Schatzkammer anzeigen',
            value='*!guild treasury Justified Loyalty* (nur für Gildenleader)',
            inline=False)
        data.add_field(
            name='Informationen zum Charakter',
            value='*!character info <name>*',
            inline=False)
        data.add_field(
            name='Informationen zum Account', value='*!account*', inline=False)
        data.add_field(
            name='PvP Statistiken', value='*!pvp stats*', inline=False)
        data.add_field(
            name='Auktionen im Handelsposten einsehen',
            value='*!tp current buys/sells*',
            inline=False)
        data.add_field(
            name='Lieferungen im Handelsposten einsehen',
            value='*!tp delivery*',
            inline=False)
        data.add_field(
            name='WvW Punktestand',
            value=
            '*!wvw info*  Kann auch mit anderen Servern aufgerufen werden.',
            inline=False)
        data.add_field(
            name='Geldbeutelinhalt (Geld oder Dungeonmarken) anzeigen',
            value='*!wallet show/tokens*',
            inline=False)
        data.add_field(
            name='Dailies anzeigen',
            value='*!daily pvp/pve/wvw/fractals*',
            inline=False)
        data.set_footer(text='Bei Fragen an Fabi wenden')
        data.set_thumbnail(
            url='https://cdn.discordapp.com/emojis/294742647069868032.png')

        await self.bot.say(embed=data)

    @commands.command(pass_context=True)
    async def ping(self, ctx, ip):
        """Check if Server is online"""

        # Check for valid IP else do DNS lookup
        valid_ip = re.compile("[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}")
        valid_hostname = re.compile(".*\.[a-zA-Z]{2,}")
        valid = False

        if valid_ip.match(ip):
            valid = True
        elif valid_hostname.match(ip):
            valid = True
            try:
                await self.bot.say('Doing DNS lookup...')
                ip = socket.gethostbyname(ip)

                if valid == True:
                    start = time.time()
                    response = os.system("sudo ping -c 1 -w3 " + ip)
                    duration = time.time() - start
                    duration = round(duration * 1000, 0)
                    if response == 0:
                        await self.bot.say(ip + ' is up and responding in ' +
                                           str(duration) + 'ms.')
                    else:
                        await self.bot.say(ip + ' is not reachable.')
                else:
                    await self.bot.say(ip + ' is not a valid IP or Domain.')

            except socket.gaierror:
                await self.bot.say('Whoops! That Address cant be resolved!')

    @commands.command(pass_context=True)
    async def pr0(self, ctx):
        """Outputs a random image from pr0gramm.com (sfw)"""

        # Generate random number, check if header responds with 200 (OK)
        # If not generate new number
        # Hardcoded img src from webpage in line 63
        # Extract path to image from webpage
        # Clean up
        user = ctx.message.author
        color = self.getColor(user)

        with urllib.request.urlopen(
                "https://pr0gramm.com/api/items/get") as url:
            data = json.loads(url.read().decode())

        items = data["items"]
        item = random.choice(items)["image"]
        upvotes = random.choice(items)["up"]
        downvotes = random.choice(items)["down"]
        uploader = random.choice(items)["user"]
        embed = discord.Embed(
            description='Uploaded by **{}**'.format(uploader), color=color)
        embed.add_field(
            name="Score",
            value="{0} :arrow_up: {1} :arrow_down:".format(upvotes, downvotes))

        await self.bot.say(embed=embed)
        await self.bot.say("https://img.pr0gramm.com/{}".format(item))

    @commands.command(pass_context=True)
    async def coinflip(self, ctx, player1=None, *, player2=None):
        """Coinflip, defaults to Kopf/Zahl if no players are given"""
        rng = randint(1, 10)

        if player1 is None and player2 is None:
            if rng < 5:
                return await self.bot.say("Kopf gewinnt!")
            else:
                return await self.bot.say("Zahl gewinnt!")
        else:
            if rng < 5:
                return await self.bot.say("{} hat gewonnen!".format(player1))
            else:
                return await self.bot.say("{} hat gewonnen!".format(player2))

    def getColor(self, user):
        try:
            color = user.colour
        except:
            color = discord.Embed.Empty
        return color

   #mensa
    @commands.command(pass_context=True)
    async def mensa(self, ctx):
        user = ctx.message.author
        color = self.getColor(user)

        # Get current calendarweek
        today = datetime.datetime.now()
        cal_week = today.strftime("%W")
        weekday = datetime.datetime.today().weekday()
        week_start = today - datetime.timedelta(days=weekday)
        week_end = today + datetime.timedelta(days=4 - weekday)

        url_mensa = "https://www.my-stuwe.de/mensa/mensa-morgenstelle-tuebingen/?woche={}".format(cal_week)

        r = requests.get(url_mensa)
        html_mensa = re.sub('\n', ' ', r.content.decode('utf8'))
        tagesmenu = re.findall(r"(<td>Tagesmenü</td>.*?)(</td>)", html_mensa)
        tagesmenu_veg = re.findall(r"(<td>Tagesmenü vegetarisch</td>.*?)(</td>)", html_mensa)
        # Probably should make an regex OR
        mensa_vital = re.findall(r"(<td>mensaVital.*?</td>.*?)(</td>)", html_mensa)

        def cleanUp(menu):
            daily_menu = []
            for m in menu:
                t_menu = re.sub("(<.*?>)", "", m[0])
                t_menu = re.sub("  |, ", "\n- ", t_menu)
                t_menu = re.sub("Tagessuppe ", "Tagessuppe\n- ", t_menu)
                t_menu = re.sub("Tagesmenü vegetarisch|Tagesmenü|mensaVital vegan|mensaVital vegetarisch|mensaVital", "", t_menu)
                daily_menu.append((t_menu))
            return daily_menu

        menu1 = cleanUp(tagesmenu)
        menu2 = cleanUp(tagesmenu_veg)
        menu3 = cleanUp(mensa_vital)
        embed = discord.Embed(
            description="Mensa Morgenstelle, KW {} vom {} bis {}".format(cal_week, week_start.strftime("%d.%m."),
                                                                         week_end.strftime("%d.%m.")), color=color)

        if weekday > 0:
            counter = 0 + weekday
        else:
            counter = 0
        wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        for speise in menu1:
            try:
                vegetarisch = menu2[counter - weekday]
            except IndexError:
                vegetarisch = ""
            try:
                vegan = menu3[counter - weekday]
            except IndexError:
                vegan = ""
            embed.add_field(name="{}".format(wochentage[counter]),
                            value="*Tagesmenü:*\n- {}\n\n*Tagesmenü vegetarisch:*\n- {}\n\n*MensaVital:*\n- {}\n".format(
                                speise, vegetarisch, vegan), inline=False)
            counter += 1

        embed.set_thumbnail(
            url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Studentenwerk_T%C3%BCbingen-Hohenheim_logo.svg/220px-Studentenwerk_T%C3%BCbingen-Hohenheim_logo.svg.png')
        embed.set_footer(text='(c) Fabian Ihle')
        await self.bot.say(embed=embed)
        
        #mensa with options
        #Options: -a for full menu, -nw for next week 
        @commands.command(pass_context=True)
    async def mensa(self, ctx, options=None):
        user = ctx.message.author
        color = self.getColor(user)
        
        #set flags
        sall = true if "a" in options else false
        nweek = true if "nw" in options else false

        # Get current calendarweek
        today = datetime.datetime.now()
        cal_week = today.strftime("%W")
        weekday = datetime.datetime.today().weekday()
        week_start = today - datetime.timedelta(days=weekday)
        week_end = today + datetime.timedelta(days=4 - weekday)

        url_mensa = "https://www.my-stuwe.de/mensa/mensa-morgenstelle-tuebingen/?woche={}".format(cal_week)

        r = requests.get(url_mensa)
        html_mensa = re.sub('\n', ' ', r.content.decode('utf8'))
        tagesmenu = re.findall(r"(<td>Tagesmenü</td>.*?)(</td>)", html_mensa)
        tagesmenu_veg = re.findall(r"(<td>Tagesmenü vegetarisch</td>.*?)(</td>)", html_mensa)
        # Probably should make an regex OR
        mensa_vital = re.findall(r"(<td>mensaVital.*?</td>.*?)(</td>)", html_mensa)

        def cleanUp(menu):
            daily_menu = []
            for m in menu:
                t_menu = re.sub("(<.*?>)", "", m[0])
                t_menu = re.sub("  |, ", "\n- ", t_menu)
                t_menu = re.sub("Tagessuppe ", "Tagessuppe\n- ", t_menu)
                t_menu = re.sub("Tagesmenü vegetarisch|Tagesmenü|mensaVital vegan|mensaVital vegetarisch|mensaVital", "", t_menu)
                daily_menu.append((t_menu))
            return daily_menu

        menu1 = cleanUp(tagesmenu)
        menu2 = cleanUp(tagesmenu_veg)
        menu3 = cleanUp(mensa_vital)
        embed = discord.Embed(
            description="Mensa Morgenstelle, KW {} vom {} bis {}".format(cal_week, week_start.strftime("%d.%m."),
                                                                         week_end.strftime("%d.%m.")), color=color)

        if weekday > 0:
            counter = 0 + weekday
        else:
            counter = 0
        wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        for speise in menu1:
            try:
                vegetarisch = menu2[counter - weekday]
            except IndexError:
                vegetarisch = ""
            try:
                vegan = menu3[counter - weekday]
            except IndexError:
                vegan = ""
            embed.add_field(name="{}".format(wochentage[counter]),
                            value="*Tagesmenü:*\n- {}\n\n*Tagesmenü vegetarisch:*\n- {}\n\n*MensaVital:*\n- {}\n".format(
                                speise, vegetarisch, vegan), inline=False)
            counter += 1

        embed.set_thumbnail(
            url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Studentenwerk_T%C3%BCbingen-Hohenheim_logo.svg/220px-Studentenwerk_T%C3%BCbingen-Hohenheim_logo.svg.png')
        embed.set_footer(text='(c) Fabian Ihle')
        await self.bot.say(embed=embed)


def setup(bot):
    n = Ihlebot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)
