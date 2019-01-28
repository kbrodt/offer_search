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

import typing as t
from pathlib import Path
from string import punctuation

import joblib
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
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

        self.__stopwords = stopwords.words('russian')

    def __is_stopword(self, token) -> bool:
        return token in self.__stopwords

    def __is_not_word(self, token) -> bool:
        return not token.isalpha()


class Vectorizer:
    def __init__(self, vectorizer_path: Path) -> None:
        if not vectorizer_path.exists():
            raise ValueError("Can not load vectorizer")

        with vectorizer_path.open('rb') as bin_:
            self.__vectorizer: TfidfVectorizer = joblib.load(bin_)

    def vectorize(self, text: str) -> np.ndarray:
        return self.__vectorizer.transform([text])


class IntentClassificationModel:
    def __init__(self, classifier_path: Path, label_encoder_path: Path) -> None:
        if not (classifier_path.exists() and label_encoder_path.exists()):
            raise ValueError("Can not load classifier and/or label encoder")

        with classifier_path.open('rb') as bin_:
            self.__classifier: LogisticRegression = joblib.load(bin_)

        with label_encoder_path.open('rb') as bin_:
            self.__label_encoder: LabelEncoder = joblib.load(bin_)

    def predict(self, vector: np.ndarray) -> str:
        intent = self.__classifier.predict(vector)

        return self.__label_encoder.inverse_transform(intent)[0]


class LogRegIntentClassifier(IntentClassifier):
    def __init__(
        self, 
        vectorizer_path: Path,
        classifier_path: Path, 
        label_encoder_path: Path,
    ) -> None:
        self.__preprocessor = Preprocessor(download_if_missing=True)
        self.__vectorize = Vectorizer(vectorizer_path)
        self.__model = IntentClassificationModel(classifier_path, label_encoder_path)

    @overrides
    def predict(self, text: str) -> str:
        preprocessed_text = self.__preprocessor.process(text)
        vectorized_text = self.__vectorize.vectorize(preprocessed_text)
        intent = self.__model.predict(vectorized_text)

        return intent
