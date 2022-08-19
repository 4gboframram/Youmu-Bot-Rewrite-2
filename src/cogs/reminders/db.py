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
import struct
from hashlib import md5
from time import time
from typing import Any

import aiosqlite
from attr import define, field

from ..embeds import YoumuEmbed
from ...bot import YoumuBot
from ...logging import get_logger

logger = get_logger(__name__)

float_to_bytes = struct.Struct("d").pack


@define
class Reminder:
    """
    A proxy class that represents a reminder
    """

    time: float
    created_at: float
    author: int
    message: str
    channel: int
    db: "ReminderDatabase"

    def __init__(
        self,
        time: float,
        created_at: float,
        author: int,
        message: str,
        channel: int,
        *,
        db: "ReminderDatabase",
    ):
        self.time = time
        self.created_at = created_at
        self.author = author
        self.message = message
        self.channel = channel
        self.db = db

    def __iter__(self):
        yield self.hash()
        yield self.time
        yield self.created_at
        yield self.author
        yield self.message
        yield self.channel

    def hash(self) -> bytes:
        hasher = md5(float_to_bytes(self.time))
        hasher.update(float_to_bytes(self.created_at))
        hasher.update(self.author.to_bytes(16, "little"))
        hasher.update(self.message.encode())
        hasher.update(self.channel.to_bytes(16, "little"))
        return hasher.digest()

    def __hash__(self):
        return hash(tuple(self))

    async def add_to_db(self):
        await self.db.con.execute(CREATE_REMINDER, tuple(self))
        await self.db.con.commit()

    async def remove_from_db(self):
        await self.db.con.execute(DELETE_REMINDER, (self.hash(),))
        await self.db.con.commit()
        await self.cancel()

    async def respond(self):
        try:
            sleep_time = self.time - time()
            await asyncio.sleep(sleep_time)

            logger.debug(f"Responding to {self}")
            bot = self.db.bot
            channel = await bot.fetch_channel(self.channel)
            create_timestamp = create_relative_timestamp(self.created_at)
            await channel.send(
                f"{self.mention}, here's your reminder from {create_timestamp}",
                embed=self.embed,
            )
            await self.remove_from_db()

        except asyncio.CancelledError:
            logger.debug(f"Cancelled {self}")

    @property
    def embed(self) -> YoumuEmbed:
        return YoumuEmbed(
            title="Reminder!", description=self.message, color=REMINDER_COLOR
        )

    @property
    def mention(self) -> str:
        return f"<@{self.author}>"

    def task(self) -> "ReminderTask":
        task = ReminderTask(self)
        self.db.tasks.add(task)
        return task

    async def cancel(self) -> bool:
        for task in self.db.tasks:
            if task == self:
                return await task.cancel()


@define(auto_attribs=False, weakref_slot=False)
class ReminderTask(asyncio.Task):
    """
    A subclass of asyncio.Task that responds to a reminder
    """

    reminder: Reminder = field()

    def __init__(self, reminder: Reminder, *, loop=None, name=None):
        self.reminder = reminder
        super().__init__(reminder.respond(), loop=loop, name=name)

    def __hash__(self):
        return hash(self.reminder)

    async def cancel(self, msg: Any | None = None) -> bool:
        a = super().cancel(msg)
        await self.reminder.remove_from_db()
        return a


REMINDER_COLOR = 0x02FAFA

CHECK_IF_TABLE_EXISTS = (
    "SELECT name FROM sqlite_master WHERE type='table' AND name='reminders';"
)
CREATE_REMINDER_TABLE = """
CREATE TABLE reminders (
hash     BLOB PRIMARY KEY NOT NULL,
time     REAL NOT NULL,
created_at REAL NOT NULL,
author   INT NOT NULL,
message  TEXT NOT NULL,
channel  INT NOT NULL);"""

GET_REMINDER = "SELECT * FROM reminders WHERE hash == ?"
CREATE_REMINDER = "INSERT INTO reminders VALUES (?, ?, ?, ?, ?, ?)"
GET_ALL_REMINDERS = "SELECT * FROM reminders WHERE time <= ?"
GET_ALL_USER_REMINDERS = "SELECT * FROM reminders WHERE author == ?"
DELETE_ALL_USER_REMINDERS = "DELETE FROM reminders WHERE author == ?"
DELETE_REMINDER = "DELETE FROM reminders WHERE hash = ?"


def create_relative_timestamp(timestamp: float) -> str:
    return f"<t:{int(timestamp)}:R>"


class ReminderDatabase:
    """
    A wrapper around sqlite database used to store reminders
    """

    def __init__(self, bot: YoumuBot):
        self.bot = bot
        self.con: aiosqlite.Connection | None = None
        self.tasks: set[ReminderTask] = set()

    async def init(self):
        db_path = self.bot.cfg.features.reminders.db_path
        logger.debug(f"Connecting to reminders database at {db_path}")
        self.con = await aiosqlite.connect(db_path)

        cur: aiosqlite.Cursor = await self.con.execute(CHECK_IF_TABLE_EXISTS)
        table = await cur.fetchone()
        if not table:
            await self.con.execute(CREATE_REMINDER_TABLE)

        self.con.row_factory = lambda cursor, row: Reminder(*row[1:], db=self)
        logger.debug(f"Connected to reminders database successfully")

    async def get_reminders(self, tme: float) -> list[Reminder, ...]:
        async with self.con.execute(GET_ALL_REMINDERS, (tme,)) as cur:
            return [i async for i in cur]

    async def get_from_user(self, user: int) -> list[Reminder, ...]:
        async with self.con.execute(GET_ALL_USER_REMINDERS, (user,)) as cur:
            return [i async for i in cur]

    async def get_reminder(self, h: str) -> Reminder:
        hsh = int(h, 16).to_bytes(16, "little")

        async with self.con.execute(GET_REMINDER, (hsh,)) as cur:
            return await cur.fetchone()

    async def delete_from_user(self, user: int):
        await self.con.execute(DELETE_ALL_USER_REMINDERS, (user,))
        await self.con.commit()

    async def close(self):
        await self.con.close()
