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

import typing as t

import numpy as np
from overrides import overrides
from scipy.sparse import hstack

from offer_search.intent_classification.standard.intent_classifier import Vectorizer


__all__ = [
    'TfidfVectorizer',
]


class TfidfVectorizer(Vectorizer):
    def __init__(self, vectorizer_path: Path) -> None:
        if not vectorizer_path.exists():
            raise ValueError("Can not load vectorizer")

        with vectorizer_path.open('rb') as bin_:
            self.__vectorizer: TfidfVectorizer = joblib.load(bin_)

    @overrides
    def vectorize(self, text: str) -> np.ndarray:
        return self.__vectorizer.transform([text])


class CompositeVectorizer(Vectorizer):
    def __init__(self, vectorizers: t.List[Vectorizer]) -> None:
        if len(vectorizers) == 0:
            raise ValueError("Pass at least one vectorizer")

        self.__vectorizers = vectorizers

    @overrides
    def vectorize(self, text: str) -> np.ndarray:
        return hstack((vectorizer.transform([text]) for vectorizer in self.__vectorizers))
