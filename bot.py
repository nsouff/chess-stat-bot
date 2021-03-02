import os

from dotenv import load_dotenv
import pickle

import discord
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
from discord.utils import find

from chess_stat.player import *
from guild_info import *

guilds_info = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
guilds_file = '.guilds.plk'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_guild_join(guild):
    for chan in guild.text_channels:
        if chan.permissions_for(guild.me).send_messages:
            # await chan.send(f'Hi {guild.name}, events notifications will be sent here')
            guilds_info[guild.id] = GuildInfo(guild.id, chan.id)
            return

@tasks.loop(seconds=30.0)
async def live_detection():
    for guild_id in guilds_info:
        guild = await bot.fetch_guild(guild_id)
        bot_member = await guild.fetch_member(bot.user.id)
        channel_id = guilds_info[guild_id].get_wr_channel()
        channel = await bot.fetch_channel(channel_id)
        for id, player in guilds_info[guild_id].get_players(id=True):
            live = await player.update_li()
            if live and live[1]:
                if channel.permissions_for(bot_member).send_messages:
                    await channel.send(f'<@{id}> is currently playing {live[1]}')

@tasks.loop(minutes=1)
async def end_game_detection():
    for guild_id in guilds_info:
        guild = await bot.fetch_guild(guild_id)
        bot_member = await guild.fetch_member(bot.user.id)
        channel_id = guilds_info[guild_id].get_wr_channel()
        channel = await bot.fetch_channel(channel_id)
        for id, player in guilds_info[guild_id].get_players(id=True):
            last_game = await player.update_com()
            if last_game:
                if channel.permissions_for(bot_member).send_messages:
                    user = await bot.fetch_user(id)
                    embed = discord.Embed(title=f'Chess.com {player.com_account.username} ({user})  game result', url=last_game['url'], color=0x6c9d41)
                    embed.set_author(name='chess-stat', icon_url="https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/SamCopeland/phpmeXx6V.png")
                    winner = 'Draw'
                    if last_game['white']['result'] == 'win':
                        winner = 'White'
                    elif last_game['black']['result'] == 'win':
                        winner = 'Black'
                    embed.add_field(name='White', value=f'> Username: {last_game["white"]["username"]}\n> Rating: {last_game["white"]["rating"]}', inline=False)
                    embed.add_field(name='Black', value=f'> Username: {last_game["black"]["username"]}\n> Rating: {last_game["white"]["rating"]}', inline=False)
                    embed.add_field(name='Time class', value=last_game['time_class'], inline=True)
                    embed.add_field(name='Rules', value=last_game['rules'], inline=True)
                    await channel.send(embed=embed)

@tasks.loop(minutes=2)
async def save():
    await bot.wait_until_ready()
    with open(guilds_file, 'wb') as f:
        pickle.dump(guilds_info, f, pickle.HIGHEST_PROTOCOL)

@bot.command(name='com_add', help='Link a chess.com account to your discord account in this guild')
async def com_add(ctx, com_account):
    players = guilds_info[ctx.guild.id]

    if players.exists(ctx.author.id):
        await players.set_com_account(ctx.author.id, com_account)
    else:
        await players.add_player(ctx.author.id, com_account=com_account)
    await ctx.send('Success')

@bot.command(name='li_add', help='Link a lichess account to your discord account in this guild')
async def li_add(ctx, li_account):
    players = guilds_info[ctx.guild.id]

    if players.exists(ctx.author.id):
        await players.set_li_account(ctx.author.id, li_account)
    else:
        await players.add_player(ctx.author.id, li_account=li_account)
    await ctx.send('Success')

@bot.command(name='set_channel', help='Set the channel where I will put events')
@has_permissions(administrator=True)
async def set_channel(ctx):
    if ctx.channel.permissions_for(ctx.guild.me).send_messages:
        await ctx.send('Event message will be sent here')
        guilds_info[ctx.guild.id].set_wr_channel(ctx.channel.id)

@bot.command(name='stat', help='Display statistics about a user')
async def stat(ctx, member: discord.Member, *args):
    players = guilds_info[ctx.guild.id]
    if not players.exists(ctx.author.id):
        await ctx.send('You must register your lichess or chess.com account first')
        return
    if not players.exists(member.id):
        await ctx.send(f'<@{member.id}> must register his lichess or chess.com account first')
        return
    lichess = chesscom = False
    if 'lichess' in args:
        lichess = True
    elif 'chesscom' in args:
        chesscom = True
    else:
        lichess = chesscom = True
    win, loss, draw = await players.get_records(ctx.author.id, member.id, lichess=lichess, chesscom=chesscom)
    await ctx.send(f'{win} **W** | {loss} **L** | {draw} **D**')

def load_guilds():
    with open(guilds_file, 'rb') as f:
        return pickle.load(f)

@bot.event
async def on_ready():
    global guilds_info
    try:
        guilds_info = load_guilds()
    except (FileNotFoundError, pickle.PickleError):
        print("erorr")
        guilds_info = {}
    for guild in bot.guilds:
        if guild.id not in guilds_info:
            await on_guild_join(guild)
        print(f'{guild}(id: {guild.id})')
    print(f'{bot.user} has connected to Discord!')
    live_detection.start()
    end_game_detection.start()
    save.start()



bot.run(TOKEN)
