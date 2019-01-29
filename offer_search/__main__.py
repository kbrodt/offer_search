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

import json
import typing as t
from pathlib import Path

from overrides import overrides

from offer_search.intent_classification import IntentClassifier
from offer_search.intent_classification import LogRegIntentClassifier
from offer_search.searcher import Searcher
from offer_search.slot_filling import SlotFiller
from offer_search.ranking import Ranker


def create_intent_classifier() -> IntentClassifier:
    resource_directory = Path('./resources/intent_classification')

    return LogRegIntentClassifier(
        resource_directory / 'over_words_vectorizer.joblib',
        resource_directory / 'over_trigrams_vectorizer.joblib',
        resource_directory / 'classifier.joblib',
        resource_directory / 'label_encoder.joblib',
    )


def create_slot_filler() -> SlotFiller:
    class SlotFillerMock(SlotFiller):
        @overrides
        def fill(self, text: str, intent: str) -> t.Dict[str, t.Any]:
            return dict()

    return SlotFillerMock()


def create_ranker() -> Ranker:
    class RankerMock(Ranker):
        @overrides
        def rank(self, search_form: t.Dict[str, t.Any]) -> t.List[t.Dict[str, t.Any]]:
            return list()

    return RankerMock()


def main() -> t.NoReturn:
    """Entrypoint
    """

    searcher = Searcher(create_intent_classifier(), create_slot_filler(), create_ranker())

    while True:
        search_request = input("search => ")

        if search_request == '\q':
            break

        offers = searcher.search(search_request)

        print("offers =>")
        for i, offer in enumerate(offers):
            print(f"\tOffer #{i + 1}\n\t{json.dumps(offer)}")
 

if __name__ == '__main__':
    main()
