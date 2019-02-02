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

import abc

import numpy as np
from overrides import overrides

from offer_search.core.intent_classification.base import IntentClassifier
from offer_search.utils.processing.text import TextProcessor


__all__ = [
    'ClassificationModel',
    'StandardIntentClassifier',
    'Vectorizer',
]


class Vectorizer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def vectorize(self, text: str) -> np.ndarray:
        pass


class ClassificationModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def predict(self, vector: np.ndarray) -> str:
        pass


class StandardIntentClassifier(IntentClassifier):
    def __init__(
        self, 
        preprocessor: TextProcessor,
        vectorizer: Vectorizer,
        model: ClassificationModel,
    ) -> None:
        self.__preprocessor = preprocessor
        self.__vectorizer = vectorizer
        self.__model = model

    @overrides
    def predict(self, text: str) -> str:
        preprocessed_text = self.__preprocessor.process(text)
        vectorized_text = self.__vectorizer.vectorize(preprocessed_text)
        predicted_intent = self.__model.predict(vectorized_text)

        return predicted_intent
