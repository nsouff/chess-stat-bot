import requests
import json
def get_username(username):
        r = requests.get(f'https://api.chess.com/pub/player/{username}')
        if r:
            return r.json()['username']
        else:
            return None

def get_current_games(username):
    r = requests.get(f'https://lichess.org/api/user/{username}')
    if r:
        player = r.json()
        if player['count']['playing'] > 0:
            return player['count']['playing'], player['playing']
        else:
            return player['count']['playing'], None

def get_records(u1, u2):
    params = {'vs': u2}
    headers = {'Accept': 'application/x-ndjson'}
    r = requests.get(f'https://lichess.org/api/games/user/{u1}', headers=headers, params=params)
    if r:
        win = loss = draw = 0
        games = [json.loads(s) for s in r.text.split("\n")[:-1]]
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

        return win, loss, draw
    else:
        return None
