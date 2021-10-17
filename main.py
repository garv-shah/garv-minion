import discord
import time
from discord.ext import commands
from discord.errors import Forbidden


class server_vars:
    def __init__(self, dmstate, dmuser, loop, mode, speed, glob_message, age3, age5, age7, prefix):
        self.dmstate = dmstate
        self.dmuser = dmuser
        self.loop = loop
        self.mode = mode
        self.speed = speed
        self.glob_message = glob_message
        self.age3 = age3
        self.age5 = age5
        self.age7 = age7
        self.prefix = prefix


global serverlist
global server_settings
serverlist = []
server_settings = []

bot = commands.Bot(command_prefix='g!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    for guild in bot.guilds:
        serverlist.append(guild.id)

    for x in range(len(serverlist)):
        server_settings.append(server_vars(False, '', 0, 0, 0, '', None, None, None, "g!"))


class Utility(commands.Cog):
    """
  Commands that actually do something kinda useful!
  """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == bot.user:
            return

        try:
            glob = server_settings[serverlist.index(message.guild.id)]
        except:
            user = await bot.fetch_user(int(message.author.id))
            await user.send('ur mom')
            return

        if message.content.lower() == "stop":
            await message.channel.send("okie dokie, stopping")
            glob.mode = 0

        if glob.mode == 1:
            try:
                glob.loop = int(message.content)
                glob.mode = 2
                await message.channel.send("and how fast would u like to spam (it's in milliseconds btw)")
            except:
                await message.channel.send('u need to send an actual number stupid')

        elif glob.mode == 2:
            try:
                glob.speed = int(message.content) / 1000
                glob.mode = 3
                await message.channel.send(
                    'do u wanna dm someone or send it here? if u wanna dm, just @ them, and if not, just say "no"')
            except:
                await message.channel.send("i don't understand what you said, repeat?")

        elif glob.mode == 3:
            if message.content.lower() == 'no' or message.content.lower() == 'nah' or message.content.lower() == 'nup':
                glob.dmstate = False
                glob.mode = 4
                await message.channel.send("cool, what would u like to spam?")
            else:
                glob.dmstate = True
                glob.dmuser = message.content
                glob.dmuser = glob.dmuser.split('>')[0].split('@')[1]
                glob.dmuser = await self.bot.fetch_user(int(glob.dmuser))
                await message.channel.send(f"spamming {glob.dmuser} >:)")
                await message.channel.send("and finally, what message would u like to spam?")
                glob.mode = 4

        elif glob.mode == 4:
            try:
                glob.glob_message = message.content
                await message.channel.send(f"spamming message: {glob.glob_message}")
                print(
                    f'glob.dmstate: {glob.dmstate}, glob.dmuser: {glob.dmuser}, glob.loop: {glob.loop}, glob.mode: {glob.mode}, glob.speed: {glob.speed}, glob.glob_message: {glob.glob_message}')

                for x in range(glob.loop):
                    if (glob.dmstate):
                        await glob.dmuser.send(glob.glob_message)
                        time.sleep(glob.speed)
                    else:
                        await message.channel.send(glob.glob_message)
                        time.sleep(glob.speed)

                glob.mode = 0
            except:
                await message.channel.send("something went very wrong, **fire**?")

    @commands.command()
    async def spam(self, ctx, *args):
        """
      a little function to spam people >:)
      """
        if server_settings[serverlist.index(ctx.message.guild.id)].mode == 0:
            await ctx.send('spammy at ur service! how many times would u like to spam?')
            server_settings[serverlist.index(ctx.message.guild.id)].mode = 1


class Games(commands.Cog):
    """
  a few little games
  """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def age(self, ctx, *args):
        """
      a maths games that guesses ur age
      """
        if server_settings[serverlist.index(ctx.message.guild.id)].mode == 0:
            await ctx.send("let's play an age game! What's the remainder of dividing your age by 3?")
            server_settings[serverlist.index(ctx.message.guild.id)].mode = 5

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == bot.user:
            return

        try:
            glob = server_settings[serverlist.index(message.guild.id)]
        except:
            user = await bot.fetch_user(int(message.author.id))
            await user.send('ur mom')
            return

        if message.content.lower() == "stop":
            await message.channel.send("okie dokie, stopping")
            glob.mode = 0

        elif glob.mode == 5:
            glob.age3 = message.content
            await message.channel.send("What's the remainder of dividing your age by 5?")
            glob.mode = 6

        elif glob.mode == 6:
            glob.age5 = message.content
            await message.channel.send("What's the remainder of dividing your age by 7?")
            glob.mode = 7

        elif glob.mode == 7:
            glob.age7 = message.content
            await message.channel.send(
                f"Are you {(int(glob.age3) * 70 + int(glob.age5) * 21 + int(glob.age7) * 15) % 105} years old?")
            glob.mode = 0

async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """
  Sends this help message
  """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *input):
        """Shows u what I can do!"""

        prefix = server_settings[serverlist.index(ctx.message.guild.id)].prefix
        version = "0.0.1"
        owner = "849839597760413717"
        owner_name = "reyy#2608"

        if not input:
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                description=f'Use `{prefix}help <module>` to gain more information about that module '
                                            f':D\n')

            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            emb.add_field(name="About", value=f"I'm a little minion made to serve all of Garv's needs. My mother is "
                                              f"reyy#2608, so dm them if you need any help.\nHere is a tree :D")
            emb.set_footer(text=f"Bot is running {version}")

        elif len(input) == 1:

            for cog in self.bot.cogs:
                if cog.lower() == input[0].lower():

                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    break

            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                    color=discord.Color.orange())

        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="It's a magical place.",
                                description="I don't know how you got here. But I didn't see this coming at all.\n"
                                            "Would you please be so kind to tell me what you did?\n"
                                            "reyy#2608\n"
                                            "Thank you! ~Garv",
                                color=discord.Color.red())

        await send_embed(ctx, emb)


bot.remove_command("help")
bot.add_cog(Utility(bot))
bot.add_cog(Games(bot))
bot.add_cog(Help(bot))

bot.run('')
