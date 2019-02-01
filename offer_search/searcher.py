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

import itertools as it
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

        offers = self.__group_product_ranking_by_offer(ranking)

        return offers[:n_top]

    @staticmethod
    def __group_product_ranking_by_offer(
        ranking: t.List[t.Dict[str, t.Any]],
    ) -> t.List[t.Dict[str, t.Any]]:
        return [
            {
                'offer': offer,
                'products': list(products),  # here we can return shorten information about the 
                                             # products or only links to them
            }
            for offer, products in it.groupby(ranking, key=lambda product: product['Offer'])
        ]
