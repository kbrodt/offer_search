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

from offer_search.intent_classification import IntentClassifier
from offer_search.slot_filling import SlotFiller
from offer_search.ranking import Ranker


__all__ = [
    'Searcher',
]


class Searcher:
    def __init__(
        self,
        intent_classifier: IntentClassifier,
        slot_filler: SlotFiller,
        ranker: Ranker,
    ) -> None:
        self.__intent_classifier = intent_classifier
        self.__slot_filler = slot_filler
        self.__ranker = ranker

    def search(self, text: str, n_top: int = 5) -> t.List[t.Dict[str, t.Any]]:
        intent = self.__intent_classifier.predict(text)
        form = self.__slot_filler.fill(text, intent)
        ranking = self.__ranker.rank(form)

        return ranking[:n_top]
