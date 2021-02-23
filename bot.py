import os

import discord
from dotenv import load_dotenv
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
from discord.utils import find

from chess_stat.player import *
from guild_info import *

guilds_info = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_guild_join(guild):
    for chan in guild.text_channels:
        if chan.permissions_for(guild.me).send_messages:
            await chan.send(f'Hi {guild.name}, events notifications will be wrote here')
            guilds_info[guild.id] = GuildInfo(guild.id, chan.id)
            return

@tasks.loop(seconds=30.0)
async def live_detection():
    await bot.wait_until_ready()
    for guild_id in guilds_info:
        guild = await bot.fetch_guild(guild_id)
        bot_member = await guild.fetch_member(bot.user.id)
        channel_id = guilds_info[guild_id].get_wr_channel()
        channel = await bot.fetch_channel(channel_id)
        for id, player in guilds_info[guild_id].get_players(id=True):
            live = player.update()[0]
            if live and live[1]:
                if channel.permissions_for(bot_member).send_messages:
                    await channel.send(f'<@{id}> is currently plyaing {live[1]}')

@bot.command(name='li_add', help='Link a lichess account to your discord account in this guild')
async def li_add(ctx, li_account):
    guilds_info[ctx.guild.id].add_player(ctx.author.id, li_account=li_account)
    await ctx.send('Success')

@bot.command(name='set_channel', help='Set the channel where I will put events')
@has_permissions(administrator=True)
async def set_channel(ctx):
    if ctx.channel.permissions_for(ctx.guild.me).send_messages:
        await ctx.send('Event message will be sent here')
        guilds_info[ctx.guild.id].set_wr_channel(ctx.channel.id)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        await on_guild_join(guild)
        print(f'{guild}(id: {guild.id})')

    print(f'{bot.user} has connected to Discord!')
    live_detection.start()



bot.run(TOKEN)
