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

import itertools as it
import typing as t

from nltk import download
from nltk.data import find
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from overrides import overrides

from offer_search.utils.processing.text.text_processing_stages import Filter


__all__ = [
    'NltkTokenizer',
]


class CompositeFilter(Filter):
    def __init__(self, filters: t.List[t.Callable[[str], bool]]) -> None:
        self.__filters = filters

    @overrides
    def filter(self, tokens: t.List[str]) -> t.List[str]:
        return [
            token 
            for token in tokens 
            if any((filter_(token) for filter_ in self.__filters))
        ]
