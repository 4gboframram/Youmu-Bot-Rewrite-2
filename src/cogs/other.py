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
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import Button

from .base import BaseCog
from .embeds import YoumuEmbed
from ..bot import YoumuBot





class OtherCog(BaseCog):
    """
    The cog containing miscellaneous commands
    """
    def __init__(self, bot: YoumuBot):
        with open("TOS.txt") as f:
            self.tos = f.read()
        super().__init__(bot)

    @commands.slash_command(name="policy", description="The bot's terms of service.")
    async def policy(self, inter):

        embed = YoumuEmbed(title="Policy", description=self.tos, color=0xFFCCAA)
        await inter.send(embed=embed)

    @commands.slash_command(name="help", description="View the documentation for the bot at its GitHub repository")
    async def help(self, inter):
        help_button = Button(url='https://github.com/4gboframram/Youmu-Bot-Rewrite-2', style=ButtonStyle.url, row=1, label="GitHub Repo")
        embed = YoumuEmbed(title="Help?",
                           description="Click the button to go the GitHub repo that contains the documentation: ",
                           colour=0x11ff11)
        await inter.send(embed=embed, components=[help_button])