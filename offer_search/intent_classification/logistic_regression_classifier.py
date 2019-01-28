#
#  Project: Offer Search
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-01-27
#
#  GitHub: @ameyuuno
#

from pathlib import Path
from string import punctuation

import joblib
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from overrides import overrides

from offer_search.intent_classification.base import IntentClassifier
from offer_search.utils.nltk_resource_manager import NltkResourceManager
from offer_search.utils.processing.text import TextProcessor
from offer_search.utils.processing.text.stages.filters import CompositeFilter
from offer_search.utils.processing.text.stages.normalizers import Pymorphy2Normalizer
from offer_search.utils.processing.text.stages.tokenizers import NltkTokenizer


__all__ = [
    'LogRegIntentClassifier',
]


class Preprocessor(TextProcessor):
    def __init__(self, download_if_missing: bool = False) -> None:
        NltkResourceManager().check_resources(['stopwords'], download_if_missing)

        super().__init__(
            NltkTokenizer(download_if_missing=True),
            CompositeFilter(filters=[
                self.__is_not_word,
                self.__is_stopword, 
            ]),
            Pymorphy2Normalizer(),
        )

        self.__stopwords = stopwords.get('russian')

    def __is_stopword(self, token) -> bool:
        return token in self.__stopwords

    def __is_not_word(self, token) -> bool:
        return not token.isalpha()


class IntentClassificationModel:
    def __init__(self, classifier_path: Path, label_encoder_path: Path) -> None:
        if not (classifier_path.exists() and label_encoder_path.exists()):
            raise ValueError("Can not load classifier and/or label encoder")

        with classifier_path.open('rb') as bin_:
            self.__classifier: LogisticRegression = joblib.load(bin_)

        with label_encoder_path.open('rb') as bin_:
            self.__label_encoder: LabelEncoder = joblib.load(bin_)


class LogRegIntentClassifier(IntentClassifier):
    def __init__(self, classifier_path: Path, label_encoder_path: Path) -> None:
        self.__preprocessor = Preprocessor(download_if_missing=True)
        self.__vectorizer = None
        self.__model = IntentClassificationModel(classifier_path, label_encoder_path)

    @overrides
    def predict(self, text: str) -> str:
        tokens = self.__preprocessor.process(text)
        vectors = self.__vectorize.transform(tokens)
        
        intent = self.__classifier.predict([])
