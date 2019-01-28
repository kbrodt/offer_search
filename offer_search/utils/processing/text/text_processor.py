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

import abc
import typing as t

from overrides import overrides

from offer_search.utils.processing.processor import Processor
from offer_search.utils.processing.text import text_processing_stages as stages


__all__ = [
    'TextPreprocessor',
]


class TextPreprocessor(Processor[str, t.List[str]]):
    def __init__(
        self,
        tokenizer: stages.Tokenizer = stages.SimpleTokenizer(),
        filter_: stages.Filter = stages.SimpleFilter(),
        normalizer: stages.Normalizer = stages.SimpleNormalizer(),
    ) -> None:
        def pipeline(text: str) -> t.List[str]:
            return normalizer.normalize(filter_.filter(tokenizer.split(text)))
        
        self.__pipeline = pipeline

    @overrides
    def process(self, source: str) -> t.List[str]:
        return self.__pipeline(source)
