# This example requires the 'message_content' intent.

import discord
import datetime

from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command()
async def history(ctx, member: discord.Member):
    try:
        await ctx.send(f'Scraping messages for {member.name}...')
        print(f"Beginning scraping messages for {member.name}")
        print(f"Date {datetime.datetime.now()}")
        messages = []
        i = 0
        for channel in ctx.guild.channels:
            print(f"- {channel.name} is of type {type(channel)}")
            if isinstance(channel, discord.TextChannel):
                async for message in channel.history(limit = 300_000_000):
                    if message.author == member:
                        messages.append(message)
                        i += 1
                        if i % 100 == 0:
                            print(f"{i} messages...")

        print(f"Finished scraping messages for {member.name}")
        time = datetime.datetime.now()
        print(f"Now = {time}")
        with open(f"messages_{time}.txt", "w") as f:
            for message in messages:
                f.write(f"- $[{message.created_at} in #{message.channel.name} | embeds: {len(message.embeds)} | id: {message.id}] [message]{message.content}[/message]\n")
        await ctx.send(f'Finished scraping messages for {member.name}. {len(messages)} total messages.')
    
    except Exception as e:
        await ctx.send(f'An error occured. Look at console for more info.')
        raise e
        


# @bot.command(description='For when you wanna settle the score some other way')
# async def choose(ctx, *choices: str):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.command()
# async def repeat(ctx, times: int, content='repeating...'):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await ctx.send(content)


# @bot.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


# @bot.group()
# async def cool(ctx):
#     """Says if a user is cool.

#     In reality this just checks if a subcommand is being invoked.
#     """
#     if ctx.invoked_subcommand is None:
#         await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


# @cool.command(name='bot')
# async def _bot(ctx):
#     """Is the bot cool?"""
#     await ctx.send('Yes, the bot is cool.')


with open("token.txt") as f:
    bot.run(f.read())