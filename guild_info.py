from chess_stat.player import *

class GuildInfo():
    def __init__(self, guild_id, wr_channel_id):
        self.guild_id = guild_id
        self.wr_channel_id = wr_channel_id
        self.players = {}
    def add_player(self, discord_id, li_account=None, com_account=None):
        self.players[discord_id] = Player(li_account, com_account)

    def set_li_account(self, discord_id, li_account):
        if discord_id not in self.players:
            raise ValueError(f'{discord_id} is not a saved player')
        else:
            self.players[discord_id].set_li_account(li_account)

    def set_com_account(self, discord_id, com_account):
        if discord_id not in self.players:
            raise ValueError(f'{discord_id} is not a saved player')
        else:
            self.players[discord_id].set_com_account(com_account)

    def set_wr_channel(self, wr_channel_id):
        self.wr_channel_id = wr_channel_id
