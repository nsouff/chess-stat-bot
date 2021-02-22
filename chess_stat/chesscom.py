import requests

def get_id(username):
    r = requests.get(f'https://api.chess.com/pub/player/{username}')
    if r:
        return r.json()['player_id']
    else:
        return None

def get_month_games(username, month):
    r = requests.get(f'https://api.chess.com/pub/player/{username}/games/{month}')
    if r:
        return r.json()['games']
    else:
        return None

def get_current_daily(username):
    r = requests.get(f'https://api.chess.com/pub/player/{username}/games')
    if r:
        return r.json()['games']
    else:
        return None

def get_month_played(username):
    r = requests.get(f'https://api.chess.com/pub/player/{username}/games/archives')
    if r:
        months = r.json()['archives']
        return [month[-7:] for month in months]
    else:
        None

def get_all_games(username):
    months = get_month_played(username)
    games = []
    for month in months:
        games.extend(get_month_games(username, month))

    return games

def get_records(u1, u2):
    games = get_all_games(u1)
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
