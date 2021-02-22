import lichess
import chesscom

class LichessUser():
    def __init__(self, username):
        if not lichess.get_username(username):
            raise ValueError("User not found on lichess.org")
        self.username = username
        self.nb_games, self.game_link = lichess.get_current_games(username)

    def update(self):
        nb_games, game_link = lichess.get_current_games(self.username)
        ret = None
        if nb_games > 0 and self.nb_games == 0:
            ret = nb_games, game_link
        self.nb_games, self.game_link = nb_games, game_link
        return ret

class ChessComUser():
    def __init__(self, username):
        if not chesscom.get_id(username):
            raise ValueError("User not found on chess.com")
        self.username = username
        self.last_game = chesscom.get_last_game(username)

    def update(self):
        last_game = chesscom.get_last_game(self.username)
        ret = None
        if last_game != self.last_game:
            ret = last_game
        self.last_game = last_game
        return ret


class Player():
    def __init__(self, lichess_name=None, chesscom_name=None):
        if (not lichess_name and not chesscom_name):
            raise ValueError("At least one account must be set")
        if lichess_name:
            self.li_account = LichessUser(lichess_name)
        if chesscom_name:
            self.com_account = ChessComUser(chesscom_name)

    def update(self):
        ret = (None, None)
        if self.li_account:
            ret[0] = self.li_account.update()
        if self.com_account:
            ret[1] = self.com_account.update()
        return ret

    def set_li_account(self, lichess_name):
        self.li_account = LichessUser(lichess_name)

    def set_com_account(self, com_account):
        self.com_account = ChessComUser(com_account)

    
