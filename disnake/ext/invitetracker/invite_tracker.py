import logging
from typing import TypeVar, Dict, Optional, Union

from disnake import Invite, Guild, Member, errors
from disnake.ext.commands import InteractionBot, Bot

__all__ = ("InviteTracker",)
logger = logging.getLogger(__name__)
T = TypeVar("T", bound=Dict[int, Dict[str, Invite]])


class InviteTracker:
    cache = None

    def __init__(
        self,
        bot: Union[InteractionBot, Bot],
        auto_work: bool = True
    ) -> None:
        """ Initialize the InviteTracker class. """
        self.bot: Union[InteractionBot, Bot] = bot
        self.auto_work: bool = auto_work
        self.cache: T = {}

        if self.auto_work:
            self.bot.add_listener(self._load_invites, "on_ready")
            self.bot.add_listener(self._add_guild, "on_guild_join")
            self.bot.add_listener(self._remove_guild, "on_guild_remove")
            self.bot.add_listener(self._create_invite, "on_invite_create")
            self.bot.add_listener(self._delete_invite, "on_invite_delete")

    async def _load_invites(self) -> T:
        """ Load all invites from a guild. """
        for guild in self.bot.guilds:
            try:
                self.cache[guild.id] = {}

                for invite in await guild.invites():
                    self.cache[guild.id][invite.code] = invite
                    logger.debug(f"Loaded invite {invite.code} from guild {guild.id}")

            except Exception as error:
                logger.error(f"Error while loading invites from guild {guild.id}: {error}")

        logger.info("Loaded all invites from guilds.")

        return self.cache

    async def _add_guild(self, guild: Guild) -> T:
        """
        Add a guild to the cache.

        :param guild: disnake.Guild: New guild to add to the cache.
        :return: T: The updated cache.
        """
        self.cache[guild.id] = {}

        try:
            for invite in await guild.invites():
                self.cache[guild.id][invite.code] = invite
                logger.debug(f"Added invite {invite.code} from guild {guild.id}")

        except (errors.HTTPException, errors.Forbidden):
            logger.error(f"[x] Failed to add invites from guild {guild.id}")

        logger.info(f"[+] Added guild {guild.id} to the cache.")

        return self.cache

    async def _remove_guild(self, guild: Guild) -> T:
        """
        Remove a guild from the cache.

        :param guild: disnake.Guild: The guild to remove from the cache.
        :return: T: The updated cache.
        """
        try:
            self.cache.pop(guild.id)
        except KeyError:
            logger.error(f"[x] Failed to remove guild {guild.id} from the cache.")

        logger.debug(f"[+] Removed guild {guild.id} from the cache.")

        return self.cache

    async def _create_invite(self, invite: Invite) -> T:
        """
        Create an invitation and add it to the cache.

        :param invite: disnake.Invite: The invite to create.
        :return: T: The updated cache.
        """
        if invite.guild.id not in self.cache.keys():
            self.cache[invite.guild.id] = {}

        self.cache[invite.guild.id][invite.code] = invite

        logger.info(f"[+] Created invite {invite.code} from guild {invite.guild.id}")

        return self.cache

    async def _delete_invite(self, invite: Invite) -> T:
        """
        Delete an invitation from the cache.

        :param invite: disnake.Invite: The invite to delete.
        :return: T: The updated cache.
        """
        if invite.guild.id not in self.cache:
            return self.cache

        if invite.code in self.cache[invite.guild.id]:
            self.cache[invite.guild.id].pop(invite.code)
            logger.info(f"[+] Deleted invite {invite.code} from guild {invite.guild.id}")

        return self.cache

    async def get_invite(self, member: Member) -> Optional[Invite]:
        """
        Get an invitation author from a member.

        :param member: disnake.Member: The member to get the invite from.
        :return: Optional[disnake.Invite]: The invite or None if not found.
        """
        guild_cache = self.cache.get(member.guild.id)
        invite = None

        if not guild_cache:
            logger.error(f"[x] Guild {member.guild.id} not found in the cache.")
            return None

        for invite_raw in await member.guild.invites():
            cached_invite = guild_cache.get(invite_raw.code)

            if cached_invite and invite_raw.uses > cached_invite.uses:
                cached_invite.uses = invite_raw.uses
                invite = invite_raw

                logger.info(f"[+] Found invite {invite.code} from guild {member.guild.id}")
                break

        return invite
