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

from offer_search.utils.processing.text.text_processing_stages import Tokenizer


__all__ = [
    'NltkTokenizer',
]


class NltkTokenizer(Tokenizer):
    __PUNKT = 'punkt'

    __PUNKT_RESOURCE = f'tokenizers/{__PUNKT}'

    def __init__(self, download_if_missing: bool = False) -> None:
        # TODO: check existence of serialized tokenizers
        pass

    @overrides
    def split(self, text: str) -> t.List[str]:
        tokenized_sentences = (word_tokenize(sentence) for sentence in sent_tokenize(text))

        return list(it.chain.from_iterable(tokenized_sentences))
