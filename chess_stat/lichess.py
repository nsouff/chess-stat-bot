import aiohttp
import json

async def get_username(username):
        session = aiohttp.ClientSession()
        r = await session.get(f'https://lichess.org/api/user/{username}')
        ret = None
        if r:
            ret =  (await r.json())['username']
        await session.close()
        return ret

async def get_current_games(username):
    session = aiohttp.ClientSession()
    r = await session.get(f'https://lichess.org/api/user/{username}')
    ret = None
    if r:
        player = await r.json()
        if 'playing' in player:
            ret = player['count']['playing'], player['playing']
        else:
            ret = player['count']['playing'], None
    await session.close()
    return ret

async def get_records(u1, u2):
    session = aiohttp.ClientSession()
    params = {'vs': u2}
    headers = {'Accept': 'application/x-ndjson'}
    r = await session.get(f'https://lichess.org/api/games/user/{u1}', headers=headers, params=params)
    ret = None
    if r:
        win = loss = draw = 0
        games = [json.loads(s) for s in (await r.text()).split("\n")[:-1]]
        for game in games:
            if 'winner' in game:
                color_u1 = 'white' if game['players']['white']['user']['name'] == u1 else 'black'
                color_u2 = 'white' if color_u1 == 'black' else 'black'
                if game['winner'] == color_u1:
                    win += 1
                else:
                    loss += 1
            else:
                draw += 1

        ret = (win, loss, draw)
    await session.close()
    return ret
