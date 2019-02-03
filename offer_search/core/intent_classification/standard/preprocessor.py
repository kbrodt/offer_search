#
#  Project: Offer Search
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-01-29
#
#  GitHub: @ameyuuno
#

from nltk.corpus import stopwords

from offer_search.utils.nltk_resource_manager import NltkResourceManager
from offer_search.utils.processing.text import TextProcessor
from offer_search.utils.processing.text.stages.filters import CompositeFilter
from offer_search.utils.processing.text.stages.normalizers import Pymorphy2Normalizer
from offer_search.utils.processing.text.stages.tokenizers import NltkTokenizer


__all__ = [
    'Preprocessor',
]


class Preprocessor(TextProcessor):
    def __init__(self, download_if_missing: bool = False) -> None:
        NltkResourceManager().check_resources(['punkt', 'stopwords'], download_if_missing)

        super().__init__(
            NltkTokenizer(),
            CompositeFilter(filters=[
                self.__is_not_word,
                self.__is_stopword, 
            ]),
            Pymorphy2Normalizer(),
        )

        self.__stopwords = stopwords.words('russian')

    def __is_stopword(self, token: str) -> bool:
        return token in self.__stopwords

    def __is_not_word(self, token: str) -> bool:
        return not token.isalpha()
