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

from pathlib import Path

import joblib
import numpy as np
from overrides import overrides
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from offer_search.intent_classification.standard.intent_classifier import ClassificationModel


__all__ = [
    'LogisticRegressionModel',
]


class LogisticRegressionModel(ClassificationModel):
    def __init__(self, classifier_path: Path, label_encoder_path: Path) -> None:
        if not (classifier_path.exists() and label_encoder_path.exists()):
            raise ValueError("Can not load classifier and/or label encoder")

        with classifier_path.open('rb') as bin_:
            self.__classifier: LogisticRegression = joblib.load(bin_)

        with label_encoder_path.open('rb') as bin_:
            self.__label_encoder: LabelEncoder = joblib.load(bin_)

    @overrides
    def predict(self, vector: np.ndarray) -> str:
        intent = self.__classifier.predict(vector)

        return self.__label_encoder.inverse_transform(intent)[0]
