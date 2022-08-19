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


from disnake.ext import commands

from ..bot import YoumuBot
from ..cfg import get_config
from ..logging import get_logger

logger = get_logger(__name__)


class BaseCog(commands.Cog):
    """
    A base class for all the other cogs to inherit from. Adds logging and adds the bot to the cog
    """

    def __init__(self, bot: YoumuBot):
        self.bot: YoumuBot = bot
        super().__init__()
        logger.debug(f"Creating cog {self.__cog_name__}")

    async def cog_load(self) -> None:
        logger.debug(f"Loading cog {self.__cog_name__}")
        await super().cog_load()

    async def cog_unload(self) -> None:
        logger.debug(f"Unloading cog {self.__cog_name__}")
        await super().cog_load()


def get_guild_ids():
    return get_config().bot_info.test_guild_ids
