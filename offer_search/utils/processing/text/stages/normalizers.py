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

from pymorphy2 import MorphAnalyzer
from overrides import overrides

from offer_search.utils.processing.text.text_processing_stages import Normalizer


__all__ = [
    'Pymorphy2Normalizer',
]


class Pymorphy2Normalizer(Normalizer):
    def __init__(self) -> None:
        self.__morph_analyzer = MorphAnalyzer()

    @overrides
    def normalize(self, tokens: t.List[str]) -> t.List[str]:
        return [self.__normalize(token) for token in tokens]

    def __normalize(self, word: str) -> str:
        return self.__morph_analyzer.parse(word)[0].normal_form
