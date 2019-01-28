#
#  Project: Offer Search
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-01-28
#
#  GitHub: @ameyuuno
#

import typing as t

from overrides import overrides

from offer_search.utils.processing.text.text_processing_stages import Filter


__all__ = [
    'CompositeFilter',
]


class CompositeFilter(Filter):
    def __init__(self, filters: t.Optional[t.List[t.Callable[[str], bool]]] = None) -> None:
        self.__filters = filters or list()

    @overrides
    def filter(self, tokens: t.List[str]) -> t.List[str]:
        return [
            token 
            for token in tokens 
            if not any((filter_(token) for filter_ in self.__filters))
        ]
