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
import difflib
from enum import Enum

import aiohttp
import disnake
from disnake.ext import commands

from .finder import search_gelbooru, BooruNotOk
from .popularity import get_sorted_popularity
from ..base import BaseCog
from ..embeds import YoumuEmbed
from ...bot import YoumuBot
from ...cfg import Config
from ...logging import get_logger

logger = get_logger(__name__)


class Rating(str, Enum):
    """
    An that represents different artwork safety ratings
    """
    safe = "safe"  # -rating:explicit -rating:questionable
    not_safe = "not_safe"  # -rating:general -rating:sensitive

    lewd = "lewd"  # -rating:general -rating:explicit

    general = "general"
    sensitive = "sensitive"
    questionable = "questionable"
    explicit = "explicit"
    any = "any"

    def get_tags(self, cfg: Config, nsfw: bool) -> list[str]:
        cfg = cfg.features.art_search
        tags = cfg.boorutags_base.copy()
        match self:
            case Rating.safe:
                tags += ["-rating:explicit", "-rating:questionable"]
            case Rating.not_safe:
                tags += ["-rating:general", "-rating:sensitive"]
            case Rating.lewd:
                tags += ["-rating:general", "-rating:explicit"]
            case Rating.general:
                tags += ["rating:general"]
            case Rating.sensitive:
                tags += ["rating:sensitive"]
            case Rating.questionable:
                tags += ["rating:questionable"]
            case Rating.explicit:
                tags += ["rating:explicit"]
            case Rating.any:
                pass
        if not nsfw:
            tags += cfg.badtags_strict + cfg.bad_artists
        else:
            tags += cfg.very_bad_tags
        return tags


class CharacterCount(str, Enum):
    """
    An enum that represents the number of characters in an artwork
    """
    solo = "solo"
    multi = "multi"
    both = "both"

    def to_tags(self) -> list[str]:
        match self:
            case self.solo:
                return ["solo"]
            case self.multi:
                return ["-1girl", "-1boy", "-solo"]
            case self.both:
                return []


class ClientResetState(int, Enum):
    """
    An enum that represents when the cog's session was last reset and if Gelbooru returned a recent bad status
    """
    ok = 0
    recent_reset = 1
    reset_and_bad_status = 2


class GelbooruCog(BaseCog):
    """
    The cog that deals with searching Gelbooru artworks
    """
    def __init__(self, bot: YoumuBot):
        self.session: aiohttp.ClientSession | None = None
        self.registered_commands: bool = False
        self.bot = bot
        self.reset_state: ClientResetState = ClientResetState.ok
        super().__init__(bot)

    async def register_slash_commands(self):
        """
        Fills the remaining slash command slots based on all character's gelbooru tag popularity
        """
        num_existing_commands = len(self.bot.all_slash_commands)

        num_commands = 100 - num_existing_commands
        logger.info(
            f"{num_existing_commands} commands already registered, so there are {num_commands} "
            f"command slots left for alias commands"
        )

        popularity = await get_sorted_popularity(self.bot.cfg)

        for data in popularity[:num_commands]:
            self.create_character_command(*data)

    async def cog_load(self) -> None:
        self.session = aiohttp.ClientSession()
        await self.register_slash_commands()
        await super().cog_load()

    async def cog_unload(self) -> None:
        await super().cog_unload()
        await self.session.close()

    @property
    def nsfw_in_non_nsfw_embed(self) -> YoumuEmbed:
        return YoumuEmbed(
            title="You Dirty Pervert!",
            description="Nsfw searches can only be done in nsfw channels, you perv!",
            color=0xFF0000,
        )

    @property
    def attempted_filter_bypass_embed(self) -> YoumuEmbed:
        return YoumuEmbed(
            title="Nice Try, Perv!",
            description="Nsfw searches can only be done in nsfw channels, you perv! "
            "You tried to find a loophole, didn't you?",
            color=0xFF0000,
        )

    @property
    def no_results_embed(self) -> YoumuEmbed:
        return YoumuEmbed(
            title="Nothing found :(",
            description="This could be because you tried to search blacklisted tags or because there is no such post",
            color=0xFFFF00,
        )

    @property
    def booru_not_ok_embed(self) -> YoumuEmbed:
        return YoumuEmbed(
            title="Gelbooru doesn't like me :(",
            description="Gelbooru returned a bad response code. "
            "Perhaps I am rate limited, so try again later?",
        )

    @commands.slash_command(
        name="tag", description="Search for artworks with given tags"
    )
    async def tag_command(
        self,
        inter: disnake.ApplicationCommandInteraction,
        tags: str = commands.Param(description="The tags to search for"),
        rating: Rating = commands.Param(
            default=Rating.safe,
            description="The safety rating of the artworks to search for",
        ),
        character_count: CharacterCount = commands.Param(
            default=CharacterCount.both,
            description="Whether results should include other characters",
        ),
    ):
        await self.tag(inter, tags, rating, character_count)

    async def tag(
        self,
        inter,
        tags: str | list[str],
        rating: Rating,
        character_count: CharacterCount,
    ):
        rating = Rating(rating)
        character_count = CharacterCount(character_count)
        logger.debug(f"{rating, character_count}")
        if self.reset_state == ClientResetState.reset_and_bad_status:
            return await inter.send(
                "Gelbooru doesn't like me right now. Try again in a bit.",
                ephemeral=True,
            )

        if isinstance(tags, str):
            tags = tags.split()
        else:
            tags = tags.copy()

        nsfw = inter.channel.is_nsfw()

        if rating not in (Rating.general, Rating.safe) and not nsfw:
            return await inter.send(embed=self.nsfw_in_non_nsfw_embed, ephemeral=True)

        if "rating:explicit" in tags or "rating:questionable" in tags and not nsfw:
            return await inter.send(
                embed=self.attempted_filter_bypass_embed, ephemeral=True
            )

        tags += rating.get_tags(self.bot.cfg, nsfw) + character_count.to_tags()

        try:
            logger.debug(f"Finding post with tags {tags}")
            result = await search_gelbooru(self.bot.cfg, tags, self.session)
            embed = result.to_embed()
            await inter.send(embed=embed)
            msg = None
            async for m in inter.channel.history():
                if not m.embeds:
                    continue

                if (
                    m.embeds[0].image.url == embed.image.url
                    and m.embeds[0].color == embed.color
                ):
                    msg = m
                    break
            else:
                logger.warning("??? Message just sent could not be found. What?")
                return

            def check(reaction, user):
                return (
                    user == inter.author
                    and str(reaction.emoji) == "❌"
                    and reaction.message.id == msg.id
                )

            r = await msg.add_reaction("❌")
            try:
                _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
                await msg.delete()

            except asyncio.TimeoutError:
                await msg.remove_reaction("❌", msg.author)

        except KeyError:
            await inter.send(embed=self.no_results_embed)
        except BooruNotOk:
            await inter.send(embed=self.booru_not_ok_embed)
            print(self.session)
            # Gelbooru probably doesn't like the session or is ratelimiting us
            if self.reset_state == ClientResetState.ok:
                await self.session.close()
                self.session = aiohttp.ClientSession()
                self.reset_state = ClientResetState.recent_reset
                await asyncio.sleep(30)
                self.reset_state = ClientResetState.ok
            elif self.reset_state == ClientResetState.recent_reset:
                self.reset_state = ClientResetState.reset_and_bad_status
                await asyncio.sleep(30)
                self.reset_state = ClientResetState.ok

    @commands.slash_command(
        name="c", description="Search artworks for all 100+ Touhou characters"
    )
    async def char(
        self,
        inter,
        name: str = commands.Param(description="The name of the character"),
        rating: Rating = commands.Param(
            default=Rating.safe,
            description="The safety rating of the artworks to search for",
        ),
        character_count: CharacterCount = commands.Param(
            default=CharacterCount.both,
            description="Whether results should include other characters",
        ),
        tags: str = commands.Param(
            default="", description="Additional tags to add to search"
        ),
    ):
        all_tags = self.bot.cfg.features.art_search.character_tags
        name = name.lower().strip()
        try:
            char_tag = all_tags[name][0]
            tags = [char_tag, *(tags.split())]
            return await self.tag(inter, tags, rating, character_count)
        except KeyError:
            try:
                await inter.send(
                    embed=YoumuEmbed(
                        title="Woops!",
                        description=f"**{name.title()}** is not a character on my list! "
                        + f"Perhaps did you mean "
                        f"**{difflib.get_close_matches(name.lower(), all_tags)[0].title()}**?",
                        color=0xFF0000,
                    )
                )
            except IndexError:
                await inter.send(
                    embed=YoumuEmbed(
                        title="Woops!",
                        description=f"**{name.title()}** is not a character on my list!",
                        color=0xFF0000,
                    )
                )

    def create_character_command(
        self, name: str, char_tag: str, description: str
    ) -> None:
        logger.debug(f"Registering command {name!r} ({char_tag!r}, {description!r})")

        @commands.slash_command(name=name, description=description)
        async def char(
            inter,
            rating: Rating = commands.Param(
                default=Rating.safe,
                description="The safety rating of the artworks to search for",
            ),
            character_count: CharacterCount = commands.Param(
                default=CharacterCount.both,
                description="Whether results should include other characters",
            ),
            tags: str = commands.Param(
                default="", description="Additional tags to add to search"
            ),
        ):
            tags = [char_tag, *tags.split()]
            await self.tag(inter, tags, rating, character_count)

        self.bot.add_slash_command(char)
