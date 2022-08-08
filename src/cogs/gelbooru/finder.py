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
from typing import Iterable, Any

from aiohttp import ClientSession
from attrs import define, fields
from disnake import Embed

from ...cfg import Config
from ...logging import get_logger

logger = get_logger(__name__)


class BooruNotOk(Exception):
    pass


BOORU_BASE_URL: str = (
    "https://www.gelbooru.com/index.php?page=dapi&s=post&q=index&json=1"
)


@define(frozen=True)
class SearchResult:
    """
    A class that represents the necessary information from a Gelbooru post
    """
    source: str
    file_url: str
    id: int
    width: int
    height: int

    def to_embed(self) -> Embed:
        if not self.source:
            booru_sauce = "No source listed"
        elif "pixiv" in self.source:
            booru_sauce = f"[Pixiv]({self.source})"
        elif "twitter" in self.source:
            booru_sauce = f"[Twitter]({self.source})"
        elif "nicovideo" in self.source:
            booru_sauce = f"[NicoNico]({self.source})"
        elif "deviantart" in self.source:
            booru_sauce = f"[DeviantArt]({self.source})"
        else:
            booru_sauce = self.source
        logger.debug(f"Converting {self} to embed")
        embed = Embed(color=random.randint(0, 0xFFFFFF))
        embed.set_author(name="Character!")
        embed.set_image(url=self.file_url)
        embed.add_field(name="Image source", value=booru_sauce, inline=False)
        embed.add_field(name="Gelbooru ID", value=self.id, inline=True)
        embed.add_field(
            name="Dimensions", value=f"{self.width}x{self.height}", inline=True
        )
        return embed


def join_tags(tags: Iterable[str]) -> str:
    return "+".join(tags)


async def search_gelbooru(
    cfg: Config, tags: Iterable[str], session: ClientSession
) -> SearchResult | None:
    url = (
        BOORU_BASE_URL + cfg.bot_info.gelbooru_credentials + "&tags=" + join_tags(tags)
    )
    logger.debug(url)
    async with session.get(url) as resp:
        logger.debug(resp.status)
        logger.debug(resp.headers)
        if resp.status != 200:
            logger.debug(await resp.content.read())
            raise BooruNotOk("Booru did not respond with an ok response code.")

        data: dict[str, Any] = await resp.json(content_type=None)
        post: dict[str, Any] = random.choice(data["post"])

        return SearchResult(
            **{field.name: post[field.name] for field in fields(SearchResult)}
        )
