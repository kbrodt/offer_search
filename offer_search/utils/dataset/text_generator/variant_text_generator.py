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

"""Variant Text Generator Module
"""

import itertools as it
import typing as t

from overrides import overrides

from offer_search.utils.dataset.text_generator.base import TextGenerator
from offer_search.utils.dataset.text_generator.simple_generator import SimpleTextGenerator


__all__ = [
    'VariantTextGenerator',
]


class VariantTextGenerator(TextGenerator):
    """Variant Text Generator

    Variant text generator builds texts just using strings as parts from passed list of possible
    variants. Not support formatting in parts.
    """
    
    def __init__(self, components: t.List[t.List[str]]) -> None:
        """Constructor

        :param components: 
        """

        self.__components = components

    @overrides
    def generate(
        self,
        joiner: t.Callable[[t.Iterable[str]], str] = ' '.join,
        filter_: t.Callable[[t.Iterable[str]], bool] = lambda combination: True,
    ) -> t.Iterable[str]:
        return it.chain.from_iterable((
            SimpleTextGenerator(parts).generate(joiner, filter_)
            for parts in it.product(*self.__components)
        ))
