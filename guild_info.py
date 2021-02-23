from chess_stat.player import *

class GuildInfo():
    def __init__(self, guild_id, wr_channel_id):
        self.guild_id = guild_id
        self.wr_channel_id = wr_channel_id
        self.players = {}
    async def add_player(self, discord_id, li_account=None, com_account=None):
        self.players[discord_id] = await Player.create_player(li_account, com_account)

    async def set_li_account(self, discord_id, li_account):
        if discord_id not in self.players:
            raise ValueError(f'{discord_id} is not a saved player')
        else:
            await self.players[discord_id].set_li_account(li_account)

    async def set_com_account(self, discord_id, com_account):
        if discord_id not in self.players:
            raise ValueError(f'{discord_id} is not a saved player')
        else:
            await self.players[discord_id].set_com_account(com_account)

    def set_wr_channel(self, wr_channel_id):
        self.wr_channel_id = wr_channel_id

    def get_players(self, id=False):
        if id:
            return self.players.items()
        else:
            return self.players.keys()

    def get_wr_channel(self):
        return self.wr_channel_id

    def exists(self, discord_id):
        return discord_id in self.players
