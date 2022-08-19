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

import hashlib
import random
from typing import Callable

import aiohttp
from disnake.ext import commands

from .base import BaseCog
from .embeds import YoumuEmbed
from ..logging import get_logger

logger = get_logger(__name__)


class RandomFunCog(BaseCog):
    """
    The cog that has random fun games / utilities
    """

    embed_color: int = 0xCC00FF
    bar_len: int = 15
    rating_map: dict[Callable[[int], bool], str] = {
        (lambda x: x in range(0, 30)): "Horrible",
        (lambda x: x in range(30, 40)): "Below Average",
        (lambda x: x in range(40, 50)): "Slightly Below Average",
        (lambda x: x in range(50, 60)): "Average",
        (lambda x: x in range(60, 70)): "Slightly Above Average",
        (lambda x: x in range(70, 80)): "Decent",
        (lambda x: x in range(80, 90)): "Pretty Good",
        (lambda x: x in range(90, 100)): "Almost Perfect",
        (lambda x: x >= 100): "Perfect",
    }

    @staticmethod
    def rng(thing: str, upper: int) -> int:
        digest = hashlib.md5(thing.encode("utf8")).digest()
        gen = random.Random(digest)
        return gen.randint(0, upper)

    @commands.slash_command(
        name="rate", description="What would I rate this thing out of 10?"
    )
    async def rate(
        self, inter, thing: str = commands.Param(description="The thing to rate")
    ):
        h = self.rng(thing, 10)
        embed = YoumuEmbed(
            title="Rate",
            description=f"I would rate *{thing}* {'an' if h == 8 else 'a'} {h} out of 10",
            color=self.embed_color,
        )
        if str(self.bot.user.id) in thing:
            embed = YoumuEmbed(
                title="Rate",
                description=f"I would rate *myself* an 11 out of 10",
                color=self.embed_color,
            )

        await inter.send(embed=embed)

    @commands.slash_command(
        name="percent", description="What percent this thing are you?"
    )
    async def percent(
        self,
        inter,
        thing: str = commands.Param(description="What percent this thing are you?"),
    ) -> None:
        h = self.rng(
            str(inter.author.id) + thing, 100
        )  # keep percent persistent among different servers
        embed = YoumuEmbed(
            title="You are...",
            description=f"{inter.author.mention}, you are {h}% *{thing}*",
            colour=self.embed_color,
        )
        await inter.send(embed=embed)

    @commands.slash_command(name="ship", description="The love boat sets sail...")
    async def ship(
        self,
        inter,
        thing_1: str = commands.Param(description="The love boat sets sail..."),
        thing_2: str
        | None = commands.Param(default=None, description="The love boat sets sail..."),
    ):
        if thing_2 is None:
            thing_2 = inter.author.mention

        ship_percent = (
            int.from_bytes(hashlib.md5(thing_1.encode("utf8")).digest(), "big")
            + int.from_bytes(hashlib.md5(thing_2.encode("utf8")).digest(), "big")
        ) % 101

        if any("692981485975633950" in thing for thing in (thing_1, thing_2)):
            ship_percent = 101

        for check, val in self.rating_map.items():
            if check(ship_percent):
                ship_compatibility = val
                break

        else:
            ship_compatibility = None

        bar = (
            self.bar_len * ship_percent // 100 * "💚"
            + (self.bar_len - self.bar_len * ship_percent // 100) * "🖤"
        )

        embed = YoumuEmbed(
            title="The Love Boat has Sailed!",
            description=f"**{thing_1}** and **{thing_2}** are **{ship_percent}%** compatible!",
            colour=self.embed_color,
        )
        embed.add_field(name=f"**{ship_percent}%**", value=f"{bar}")
        embed.set_footer(text=f"Compatibility: {ship_compatibility}!")
        await inter.send(embed=embed)

    @commands.slash_command(name="inspire", description="Feeling sad? Try this!")
    async def inspire(self, inter):
        logger.debug("Getting inspiration")
        try:
            url = "http://inspirobot.me/api?generate=true"
            params = {"generate": "true"}
            async with aiohttp.ClientSession() as s:
                async with s.get(url, params=params) as response:
                    image = await response.text()
            embed = YoumuEmbed(title="Inspiration", colour=0x53CC74)
            embed.set_image(url=image)

            await inter.send(embed=embed)

        except aiohttp.ClientError:
            await inter.send("Inspirobot is broken, there is no reason to live.")
