import disnake

class InviteLogger():
    def __init__(self, bot):
        self.bot = bot
        self.cache = {}

        self.bot.add_listener(self.update_guild_cache, "on_ready")
        self.bot.add_listener(self.add_guild_cache, "on_guild_join")
        self.bot.add_listener(self.remove_guild_cache, "on_guild_remove")
        self.bot.add_listener(self.update_invite_cache, "on_invite_create")
        self.bot.add_listener(self.remove_invite_cache, "on_invite_delete")

    async def update_guild_cache(self):
        for guild in self.bot.guilds:
            try:
                self.cache[guild.id] = {}
                for invite in await guild.invites():
                    self.cache[guild.id][invite.code] = invite
            except:
                continue

    async def add_guild_cache(self, guild: disnake.Guild):
        self.cache[guild.id] = {}
        for invite in await guild.invites():
            self.cache[guild.id][invite.code] = invite

    async def remove_guild_cache(self, guild: disnake.Guild):
        try:
            self.cache.pop(guild.id)
        except:
            return

    async def update_invite_cache(self, invite: disnake.Invite):
        if not invite.guild.id in self.cache.keys():
            self.cache[invite.guild.id] = {}
        self.cache[invite.guild.id][invite.code] = invite

    async def remove_invite_cache(self, invite: disnake.Invite):
        if not invite.guild.id in self.cache.keys():
            return
        for cach_invite in self.cache[invite.guild.id].values():
            if invite.code == cach_invite.code:
                self.cache[invite.guild.id].pop(invite.code)

    async def get_invite(self, member: disnake.Member):
        for join_invite in await member.guild.invites():
            for cach_invite in self.cache[member.guild.id].values():
                if join_invite.uses > cach_invite.uses:
                    if join_invite.code == cach_invite.code:
                        cach_invite.uses += 1
                        return join_invite