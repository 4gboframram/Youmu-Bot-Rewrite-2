#    Copyright (C) 2022  4gboframram

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by

#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random
from typing import cast

from disnake.ext import commands

from .cfg import get_config, Config
from .logging import get_logger

logger = get_logger(__name__)

BotBase: type[commands.InteractionBot] = commands.InteractionBot

if get_config().bot_info.shard:
    BotBase = cast(
        type[commands.InteractionBot], commands.AutoShardedInteractionBot
    )  # damn you type checker

logger.debug(f"Bot base class is {BotBase.__name__}")


class YoumuBot(BotBase):
    """
    The base class representing the Bot itself
    """

    def __init__(self):
        cfg = get_config()
        self.cfg: Config = cfg
        self.current_presence = random.choice(cfg.bot_info.presences)
        test_guild_ids = cfg.bot_info.test_guild_ids
        super().__init__(test_guilds=test_guild_ids if test_guild_ids else None)

    def reload_config(self) -> None:
        self.cfg = get_config(force_reload=True)

    async def start_bot(self):
        from .cogs.sanity import SanityCog
        from .cogs.gelbooru.cog import GelbooruCog
        from .cogs.random_fun import RandomFunCog
        from .cogs.other import OtherCog
        from .cogs.reminders.cog import RemindersCog
        from .cogs.games.cog import GameCog
        from .cogs.markov.cog import SpellcardCog

        self.add_cog(SanityCog(self))
        self.add_cog(RandomFunCog(self))
        self.add_cog(OtherCog(self))
        self.add_cog(RemindersCog(self))
        self.add_cog(GameCog(self))
        self.add_cog(SpellcardCog(self))
        self.add_cog(GelbooruCog(self))

        await self.start(self.cfg.bot_info.token)
