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
from disnake import MessageInteraction, ButtonStyle
from disnake.ext import commands
from disnake.ui import Button, View

from .ttt import TTT
from ..base import BaseCog
from ..embeds import YoumuEmbed


class TTTInviteView(View):
    """
    A view that represents an invitation to a TTT game
    """

    def __init__(self, players: tuple[int, int], n: int, inter):
        super().__init__(timeout=60.0)
        self.button = TTTInviteButton(players, n)
        self.inter = inter
        self.add_item(self.button)

    async def on_timeout(self) -> None:
        self.button.label = "Expired Invite :("
        self.button.emoji = "❎"
        self.button.disabled = True
        self.button.style = ButtonStyle.red
        await self.inter.edit_original_message(view=self)

        self.stop()


class TTTInviteButton(Button[TTTInviteView]):
    """
    A class that represents the button that starts a TTT game
    """

    def __init__(self, players: tuple[int, int], n: int):

        if random.randint(0, 1):
            self.players = tuple(reversed(players))
        else:
            self.players = players

        self.n = n
        super().__init__(
            label="Accept Tic Tac Toe Invite",
            style=disnake.ButtonStyle.green,
            emoji="☑️",
        )

    async def callback(self, inter: MessageInteraction):
        if inter.author.id != self.players[1]:
            return
        game = TTT(players=self.players, n=self.n)
        await inter.send(f"{game.current_turn_mention}'s turn!", view=game)


class GameCog(BaseCog):
    """
    A cog that handles various major games within the bot
    """

    @commands.slash_command(
        name="ttt", description="Play a game of Tic Tac Toe with someone."
    )
    async def ttt(
        self,
        inter,
        player: disnake.Member = commands.Param(
            name="player", description="Who to play the game with"
        ),
        n: int = commands.Param(
            name="n", description="The dimension of the board", default=3, ge=1, le=5
        ),
    ):
        if player.id == inter.author.id:
            await inter.send("You can't challenge yourself!", ephemeral=True)
            return

        embed = YoumuEmbed(
            title="✉️Invitation!✉️",
            description=f"{player.mention}, {inter.author.mention} has challenged you to a game of "
            + f"**Tic Tac Toe**.\n\nPress the button within the next minute to start the game."
            + f"\n\n*Remember that if you don't accept, you might lose a friend~*",
            color=0x53CC74,
        )
        view = TTTInviteView((inter.author.id, player.id), n, inter)
        await inter.send(embed=embed, view=view)
