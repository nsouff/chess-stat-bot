import aiohttp

async def get_id(username):
    session = aiohttp.ClientSession()
    r = await session.get(f'https://api.chess.com/pub/player/{username}')
    ret = None
    if r:
        ret = (await r.json())['player_id']
    await session.close()
    return ret

async def get_month_games(username, month):
    session = aiohttp.ClientSession()
    r = await session.get(f'https://api.chess.com/pub/player/{username}/games/{month}')
    ret = None
    if r:
        ret = (await r.json())['games']
    await session.close()
    return ret

async def get_current_daily(username):
    session = aiohttp.ClientSession()
    r = await session.get(f'https://api.chess.com/pub/player/{username}/games')
    ret = None
    if r:
        ret = (await r.json())['games']
    await session.close()
    return ret

async def get_month_played(username):
    session = aiohttp.ClientSession()
    r = await session.get(f'https://api.chess.com/pub/player/{username}/games/archives')
    ret = None
    if r:
        months = (await r.json())['archives']
        ret = [month[-7:] for month in months]
    await session.close()
    return ret
async def get_all_games(username):
    months = await get_month_played(username)
    games = []
    for month in months:
        games.extend(await get_month_games(username, month))

    return games

async def get_records(u1, u2):
    games = await get_all_games(u1)
    win = 0
    draw = 0
    loss = 0

    for game in games:
        if game['white']['username'] == u2 or game['black']['username'] == u2:
            color_u1 = 'white' if game['white']['username'] == u1 else 'black'
            color_u2 = 'white' if color_u1 == 'black' else 'black'
            if game[color_u1]['result'] == 'win': win += 1
            elif game[color_u2]['result'] == 'win': loss += 1
            else : draw += 1

    return win, loss, draw

async def get_last_game(username):
    months = await get_month_played(username)
    print("BEF")
    if months == None or len(months) == 0:
        return None
    print("OK")
    month = months[-1]
    games = await get_month_games(username, month)
    print(games[-1]['white']['username'], games[-1]['black']['username'])
    return games[-1]
