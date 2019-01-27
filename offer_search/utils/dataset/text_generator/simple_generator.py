#
#  Project: Offer Search - Experiments
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-01-27
#
#  GitHub: @ameyuuno
#

"""Simple Text Generator Module
"""

import itertools as it
import typing as t

from overrides import overrides

from offer_search.utils.dataset.text_generator.base import TextGenerator


__all__ = [
    'SimpleTextGenerator',
]


class SimpleTextGenerator(TextGenerator):
    """Simple Text Generator

    Simple text generator builds texts just using strings as parts. Not support any formatting or 
    variants.
    """
    
    def __init__(self, parts: t.List[str]) -> None:
        """Constructor

        :param parts: 
        """

        self.__parts = parts

    @overrides
    def generate(
        self,
        joiner: t.Callable[[t.Iterable[str]], str] = ' '.join,
        filter_: t.Callable[[t.Iterable[str]], bool] = lambda combination: True,
    ) -> t.Iterable[str]:
        combinations = it.chain.from_iterable((
            it.combinations(self.__parts, combination_size)
            for combination_size in range(1, len(self.__parts) + 1)
        ))

        combinations_with_permutations = it.chain.from_iterable((
            it.permutations(combination)
            for combination in combinations
        ))

        return (
            joiner(combination) 
            for combination in combinations_with_permutations 
            if filter_(combination)
        )
