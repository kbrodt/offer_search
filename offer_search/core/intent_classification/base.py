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

import abc


__all__ = [
    'IntentClassifier',
]


class IntentClassifier(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def predict(self, text: str) -> str:
        pass
