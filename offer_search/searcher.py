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
import json
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
        print(f'Intent:\t{intent}')

        form = self.__slot_filler.fill(text, intent)
        print(f'Slots:\t{json.dumps(form, ensure_ascii=False, indent=2)}')

        ranking = self.__ranker.rank(form)

        offers = self.__group_product_ranking_by_offer(ranking, n_top)

        return offers[:n_top]

    @staticmethod
    def __group_product_ranking_by_offer(
        ranking: t.List[t.Dict[str, t.Any]],
        n_top: int = 5,
    ) -> t.List[t.Dict[str, t.Any]]:
        offer_names = set()
        offers = []
        for offer, products in it.groupby(ranking, key=lambda product: product['Offer']):
            if offer in offer_names:
                continue

            new_products = []
            for product in products:
                product.pop('Offer')
                web = product.pop('Web')
                cashback = product.pop('Cashback')
                period = product.pop('Period')
                offer_type = product.pop('Offer_type')
                advert_text = product.pop('Advert_text')
                new_products.append(product)
            products = new_products

            offer_names.add(offer)
            offers.append({
                'offer': {
                    'offer': offer,
                    'web': web,
                    'cashback': cashback,
                    'period': period,
                    'offer_type': offer_type,
                    'advert_text': advert_text,
                },
                'products': list(products)[:n_top],  # here we can return shorten information about the 
                                                     # products or only links to them
            })

        return offers
