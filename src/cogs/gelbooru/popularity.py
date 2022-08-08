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

import aiohttp

from ...cfg import Config
from ...logging import get_logger

logger = get_logger(__name__)
BOORU_TAGS_URL = "https://gelbooru.com/index.php?page=dapi&s=tag&q=index&json=1&names="


async def get_sorted_popularity(cfg: Config):
    logger.info("Getting popularity of characters.")

    char_tags = cfg.features.art_search.character_tags
    config_by_tags = {d[0]: (name, d[0], d[1]) for name, d in char_tags.items()}

    tags = " ".join(i[0] for i in char_tags.values())
    url = BOORU_TAGS_URL + tags
    logger.debug(f"Getting {url}")
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(verify_ssl=False)
    ) as sess:
        async with sess.get(url) as resp:
            json = await resp.json(content_type=None)
            data = json["tag"]
            tags_sorted = [
                i["name"] for i in sorted(data, key=lambda x: x["count"], reverse=True)
            ]
            return [config_by_tags[tag] for tag in tags_sorted]
