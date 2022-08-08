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

import asyncio
from datetime import datetime, timedelta

import aiosqlite
from disnake.abc import GuildChannel
from disnake.ext import commands, tasks

from .db import ReminderDatabase, Reminder
from ..base import BaseCog
from ..embeds import YoumuEmbed
from ...logging import get_logger

logger = get_logger(__name__)


class RemindersCog(BaseCog):
    """
    The cog that deals with the creating and removing reminders and manages the loop that fetches new reminders
    """
    embed_color = 0x42C78D

    def __init__(self, bot):
        super().__init__(bot)
        self.db: ReminderDatabase | None = None

    @commands.slash_command(
        name="reminder",
        description="Remind you of something in a certain amount of time",
    )
    async def reminder(self, inter):
        pass

    @reminder.sub_command(name="new", description="Create a new reminder.")
    async def new(
        self,
        inter,
        reminder: str = commands.Param(description="The message for the reminder"),
        channel: GuildChannel
        | None = commands.Param(
            default=None, description="The channel to send the reminder to"
        ),
        seconds: int = commands.Param(default=0, description="Number of seconds"),
        minutes: int = commands.Param(default=0, description="Number of minutes"),
        hours: int = commands.Param(default=0, description="Number of hours"),
        days: int = commands.Param(default=0, description="Number of days"),
        weeks: int = commands.Param(default=0, description="Number of weeks"),
        months: int = commands.Param(
            default=0, description="Number of months (30 days)"
        ),
    ):
        creation_time = datetime.now()
        delta = timedelta(
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days + 30 * months,
            weeks=weeks,
        )

        """if delta.total_seconds() < 30:
            return await inter.send(f"Cannot process times less than 30 seconds", ephemeral=True)"""

        if delta > timedelta(days=365):
            return await inter.send(
                f"Cannot set a reminder for longer than year in the future",
                ephemeral=True,
            )

        if len(await self.db.get_from_user(inter.author.id)) >= 10:
            return await inter.send(
                "You cannot create more than 10 reminders. "
                "You need to cancel some reminders to create more!",
                ephemeral=True,
            )

        reminder_timestamp = (creation_time + delta).timestamp()
        creation_timestamp = creation_time.timestamp()

        if channel is None:
            channel = inter.channel

        channel_id = channel.id
        author_id = inter.author.id

        reminder = Reminder(
            time=reminder_timestamp,
            created_at=creation_timestamp,
            author=author_id,
            message=reminder,
            channel=channel_id,
            db=self.db,
        )

        await reminder.add_to_db()

        if (
            reminder_timestamp <= self.reminder_loop.next_iteration.timestamp()
        ):  # if it goes off before the next loop
            self.db.tasks.add(
                reminder.task()
            )  # schedule the task because it won't be scheduled before it's too late

        embed = YoumuEmbed(
            title="Reminder scheduled!",
            description=f"Reminder scheduled for <t:{int(reminder_timestamp)}:R>",
            color=0x00FF00,
        )
        await inter.send(embed=embed, ephemeral=True)

    @reminder.sub_command(name="list", description="List all of your current reminders")
    async def list(self, inter):
        reminders = await self.db.get_from_user(inter.author.id)
        embed = YoumuEmbed(title="Reminders", color=self.embed_color)
        if not reminders:
            embed.description = "You do not have any reminders!"
        else:
            embed.description = "Here are your scheduled reminders:"

        for reminder in reminders:
            hash_str = hex(int.from_bytes(reminder.hash(), "little"))[2:]
            embed.add_field(
                name=f"ID: {hash_str}",
                value=f"Message: {reminder.message!r}, Scheduled For: <t:{int(reminder.time)}:F>, "
                f"Created At <t:{int(reminder.created_at)}:F>",
                inline=False,
            )

        await inter.send(embed=embed, ephemeral=True)

    @reminder.sub_command(name="cancel", description="Cancel a reminder")
    async def cancel(
        self,
        inter,
        reminder_id: str = commands.Param(
            name="id", description="The unique id for the reminder."
        ),
    ):
        try:
            reminder = await self.db.get_reminder(reminder_id)

            if reminder is None:
                return await inter.send(
                    f"Could not find a reminder with an id of *{reminder_id}*",
                    ephemeral=True,
                )

            if reminder.author != inter.author.id:
                return await inter.send(
                    "You cannot delete another user's reminder!", ephemeral=True
                )

            await reminder.remove_from_db()

            embed = YoumuEmbed(
                title="Success!",
                description=f"Cancelled reminder **{reminder_id}** successfully!",
                color=self.embed_color,
            )
            await inter.send(embed=embed, ephemeral=True)

        except ValueError | aiosqlite.Error:
            return await inter.send(f"Invalid reminder_id {reminder_id!r}")

    @reminder.sub_command(name="cancel_all", description="Cancel all of your reminders")
    async def cancel_all(self, inter):
        reminders = await self.db.get_from_user(inter.author.id)
        if not reminders:
            return await inter.send("You do not have any reminders to cancel!")

        await asyncio.gather(*[i.remove_from_db() for i in reminders])

        embed = YoumuEmbed(
            title="Success!",
            description="Cancelled all your reminders!",
            color=self.embed_color,
        )

        await inter.send(embed=embed, ephemeral=True)

    @tasks.loop(hours=1)
    async def reminder_loop(self):
        logger.debug("Getting new set of reminders")

        tme = (datetime.now() + timedelta(hours=1)).timestamp()
        reminders = await self.db.get_reminders(tme)
        for task in self.db.tasks:
            assert task.done()

        self.db.tasks = set(r.task() for r in reminders)
        logger.debug(f"Got reminders: {reminders}")

    async def cog_load(self) -> None:
        self.db = ReminderDatabase(self.bot)
        await self.db.init()
        self.reminder_loop.start()

    async def cog_unload(self) -> None:
        self.reminder_loop.cancel()
        await self.db.close()
