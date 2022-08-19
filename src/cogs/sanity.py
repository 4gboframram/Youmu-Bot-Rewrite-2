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

import disnake
from disnake.ext import commands, tasks

from .base import BaseCog
from ..logging import get_logger

logger = get_logger(__name__)


class SanityCog(BaseCog):
    """
    The cog that handles various things that ensure the bot is working and manages the presence loop
    """

    @commands.slash_command(name="ping", description="Pong?")
    async def ping(self, ctx: disnake.ApplicationCommandInteraction):
        message = random.choice(self.bot.cfg.bot_info.ping_messages)
        await ctx.send(f"{message} ({self.bot.latency * 1000:.0f} ms)")

    def cog_load(self) -> None:
        self.change_presence.start()

    def cog_unload(self) -> None:
        self.change_presence.cancel()

    @tasks.loop(hours=1)
    async def change_presence(self):
        (*available,) = set(self.bot.cfg.bot_info.presences) - {
            self.bot.current_presence
        }
        new_presence = random.choice(available)
        logger.info(f"Changing status to {new_presence!r}")

        await self.bot.change_presence(
            status=disnake.Status.online, activity=disnake.Game(new_presence)
        )

    @change_presence.before_loop
    async def before_change_presence(self):
        logger.info("Waiting until bot is ready to start the presence loop")
        await self.bot.wait_until_ready()
        logger.info("Ready")
