from . import lichess
from . import chesscom

class LichessUser():
    @classmethod
    async def create_li_user(cls, username):
        self = LichessUser()
        if not await lichess.get_username(username):
            raise ValueError("User not found on lichess.org")
        self.username = username
        self.nb_games, self.game_link = await lichess.get_current_games(username)
        return self

    async def update(self):
        nb_games, game_link = await lichess.get_current_games(self.username)
        ret = None
        if nb_games > 0 and self.nb_games == 0:
            ret = nb_games, game_link
        self.nb_games, self.game_link = nb_games, game_link
        return ret

class ChessComUser():
    @classmethod
    async def create_com_user(cls, username):
        self = ChessComUser()
        if not await chesscom.get_id(username):
            raise ValueError("User not found on chess.com")
        self.username = username
        self.last_game = await chesscom.get_last_game(username)
        return self

    async def update(self):
        last_game = await chesscom.get_last_game(self.username)
        ret = None
        if last_game != self.last_game:
            ret = last_game
        self.last_game = last_game
        return ret


class Player():
    @classmethod
    async def create_player(cls, lichess_name=None, chesscom_name=None):
        self = Player()
        if (not lichess_name and not chesscom_name):
            raise ValueError("At least one account must be set")
        self.li_account = self.com_account = None
        if lichess_name:
            self.li_account = await LichessUser.create_li_user(lichess_name)
        if chesscom_name:
            self.com_account = await ChessComUser.create_com_user(chesscom_name)
        return self

    async def update_li(self):
        if self.li_account:
            return await self.li_account.update()
    async def update_com(self):
        if self.com_account:
            return await self.com_account.update()

    async def set_li_account(self, lichess_name):
        self.li_account = await LichessUser.create_li_user(lichess_name)

    async def set_com_account(self, com_account):
        self.com_account = await ChessComUser.create_com_user(com_account)
