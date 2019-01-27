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

"""Placeholder Text Generator Module
"""

import itertools as it
import typing as t

from overrides import overrides

from offer_search.utils.dataset.text_generator.base import TextGenerator
from offer_search.utils.dataset.text_generator.variant_text_generator import VariantTextGenerator


__all__ = [
    'PlaceholderTextGenerator',
]


class PlaceholderTextGenerator(VariantTextGenerator):
    """Placeholder Text Generator
    """
    
    def __init__(
        self, 
        components: t.List[t.List[str]], 
        placeholders: t.Dict[str, t.Callable[[], str]],
    ) -> None:
        """Constructor

        :param components: 
        :param placeholders: 
        """

        super().__init__(components)

        self.__placeholders = placeholders

    @overrides
    def generate(
        self,
        joiner: t.Callable[[t.Iterable[str]], str] = ' '.join,
        filter_: t.Callable[[t.Iterable[str]], bool] = lambda combination: True,
    ) -> t.Iterable[str]:
        return (
            text.format(**{
                place: placeholder()
                for place, placeholder in self.__placeholders.items()
            })
            for text in super().generate(joiner, filter_)
        )
