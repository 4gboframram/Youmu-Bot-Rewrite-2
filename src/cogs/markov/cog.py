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

import os
import string
from pathlib import Path
from random import randint

from disnake.ext import commands

from .markov import Markov
from ..base import BaseCog


class SpellcardCog(BaseCog):
    async def cog_load(self) -> None:
        with open(Path(os.getcwd(), "assets", "spellcards.txt")) as f:
            data = f.read().lower().replace("-", " ").replace('"', " ")
            data = filter(
                lambda x: x in string.ascii_lowercase + string.digits + " %", data
            )
            data = "".join(data)
            self.markov = Markov(data.split(" "))
            self.markov.train()

    def generate_spellcard(self):
        while True:
            (*result,) = self.markov.generate(word_count=randint(4, 8))
            if "sign" in result:
                i = result.index("sign")
                if i < (len(result) - 2) and i != 0 and result.count("sign") == 1:
                    result[i + 1] = "｢" + result[i + 1]
                    result[-1] += "｣"
                    break

        return " ".join(result).title().replace("｢ ", "｢")

    @commands.slash_command(name="spellcard", description="Generate a spellcard name.")
    async def spellcard(self, inter):
        await inter.send(self.generate_spellcard())
