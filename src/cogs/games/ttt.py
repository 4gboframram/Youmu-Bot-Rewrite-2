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

import numpy as np
from disnake import ButtonStyle, MessageInteraction
from disnake.ui import Button, View

from ...logging import get_logger

logger = get_logger(__name__)


class InvalidBoardSize(Exception):  # unused, will be removed
    def __init__(self, n):
        self.message = (
            f"Invalid size for tictactoe board, {n}. Must be size 1-5 inclusive."
        )
        super().__init__(self.message)


class TTT(View):
    """
    A View that represents the state of a TTT game
    """

    def __init__(self, n: int, players: tuple[int, int]):
        # x is 0, o is 1, not taken is -1
        if n not in range(1, 6):  # unneeded
            raise InvalidBoardSize(n)

        self.players = players
        self.labels = ("o", "x")
        self.turn = 1
        self.board: np.ndarray = np.zeros((n, n), dtype=int) - 1
        super().__init__(timeout=600.0)

        for x in range(n):
            for y in range(n):
                self.add_item(TTTButton(x, y))

    def update_turn_order(self) -> None:
        self.turn += 1
        self.turn %= 2

    @property
    def current_turn_mention(self) -> str:
        return f"<@{self.players[self.turn]}>"

    @staticmethod
    def check_rows(arr: np.ndarray) -> int | None:
        for row in arr:
            if len(set(row)) == 1:
                result = row[0]
                if result != -1:
                    return result
        return None

    def check_diags(self) -> int | None:
        diag = self.board.diagonal()
        if len(set(diag)) == 1 and diag[0] and -1 not in diag:
            return diag[0]

        other_diag = np.rot90(self.board).diagonal()

        if len(set(other_diag)) == 1 and -1 not in diag:
            return other_diag[0]

        return None

    def winner(self) -> int | None:
        """
        Returns 0 for red, 1 for blue, and None for no winner
        """
        results = (
            self.check_rows(self.board),
            self.check_rows(np.rot90(self.board)),
            self.check_diags(),
        )

        (*results,) = set(filter(lambda x: x is not None, results))

        assert len(results) in (0, 1), "Houston, we have a problem"

        return results[0] if results else None

    def end_game(self) -> None:
        for item in self.children:
            item.disabled = True
        self.stop()

    async def on_timeout(self) -> None:
        self.end_game()
        await super().on_timeout()


class TTTButton(Button["TTT"]):
    """
    A button that changes the state of a TTT game
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        super().__init__(row=y, label="\u200b")

    @property
    def state(self):
        return self.view.board[self.x][self.y]

    @state.setter
    def state(self, value: int):
        self.view.board[self.x][self.y] = value

    def get_new_style(self) -> ButtonStyle:
        match self.state:
            case 0:
                return ButtonStyle.red
            case 1:
                return ButtonStyle.blurple
            case _:
                return ButtonStyle.gray

    async def callback(self, interaction: MessageInteraction, /):
        assert self.state == -1
        if interaction.author.id != self.view.players[self.view.turn]:
            interaction.response.send_message(
                f"{interaction.author.mention}, you cannot do this!", ephemeral=True
            )
            return

        self.state = self.view.turn
        self.label = self.view.labels[self.state]
        self.style = self.get_new_style()
        self.disabled = True

        if winner := self.view.winner() is not None:
            self.view.end_game()
            await interaction.response.edit_message(
                f"{self.view.current_turn_mention} won!", view=self.view
            )
        elif -1 not in self.view.board.flat:
            self.view.end_game()
            await interaction.response.edit_message(f"Nobody Won!", view=self.view)
        else:
            self.view.update_turn_order()
            await interaction.response.edit_message(
                f"{self.view.current_turn_mention}'s turn!", view=self.view
            )
