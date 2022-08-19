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

"""
Contains a class for creating Markov Chain Generators.
"""

import random
import typing


class NotTrainedError(Exception):
    """
    An Exception raised when the Markov chain is not trained.
    """

    def __init__(self, *args):
        super().__init__(*args)


class Markov:
    """
    A class that represents a markov chain generator.
    """

    def __init__(self, words: typing.Iterable[typing.Hashable]):
        """
            :param words: An iterable that represents words for the dataset of the Markov chain generator.
        All elements must be hashable
        """
        self.words = tuple(words)
        self.chain = dict()

    def train(self) -> None:
        """
        Trains the model by generating the chain.
        :return: None
        """
        for i in range(len(self.words)):
            word = self.words[i]
            if word not in self.chain:
                self.chain[word] = []
            self.chain[word].append(self.words[i + 1]) if i < len(
                self.words
            ) - 1 else None

    def generate(self, seed: str | None = None, *, word_count: int) -> tuple:
        """
        Generates a Markov chain from the training data
        :param seed: The starting seed of the chain generator. Should be either None or an element in the dataset.
         If None, uses a random element in the dataset.
        :param word_count: The number of words to generate
        :return: A list of words with a length of word_count
        :raises: ValueError, NotTrainedError
        """

        if word_count <= 0:
            raise ValueError("Number of words to generate must be greater than zero")

        if not self.chain:
            raise NotTrainedError(
                "Before generating anything, the Markov chain must be trained"
            )

        if seed is None:
            seed = random.choice(tuple(self.chain.keys()))

        result = []
        for _ in range(word_count):
            result += [seed]
            seed = random.choice(self.chain[seed])
        return tuple(result)

    def new_generator(self, seed: str | None = None):
        """
        :param seed: The starting seed of the chain generator. Should be either None or an element in the dataset.
         If None, uses a random element in the dataset.
        :return: A generator that
        """
        if not self.chain:
            raise NotTrainedError(
                "Before generating anything, the Markov chain must be trained"
            )

        if seed is None:
            seed = random.choice(tuple(self.chain.keys()))

        def _generator():
            nonlocal self
            nonlocal seed
            while True:
                seed = random.choice(self.chain[seed])
                yield seed

        return _generator()
