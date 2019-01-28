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

from offer_search.intent_classification.base import IntentClassifier
from offer_search.intent_classification.logistic_regression_classifier import LogRegIntentClassifier


__all__ = [
    'IntentClassifier',
    'LogRegIntentClassifier',
]
