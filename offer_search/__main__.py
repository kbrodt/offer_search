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

from overrides import overrides

from offer_search.intent_classification import IntentClassifier
from offer_search.slot_filling import SlotFiller
from offer_search.ranking import Ranker
from offer_search.searcher import Searcher


class IntentClassifierMock(IntentClassifier):
    @overrides
    def predict(self, text: str) -> str:
        return ''


class SlotFillerMock(SlotFiller):
    @overrides
    def fill(self, text: str, intent: str) -> t.Dict[str, t.Any]:
        return dict()


class RankerMock(Ranker):
    @overrides
    def rank(self, search_form: t.Dict[str, t.Any]) -> t.List[t.Dict[str, t.Any]]:
        return list()


def main() -> t.NoReturn:
    """Entrypoint
    """

    searcher = Searcher(IntentClassifierMock(), SlotFillerMock(), RankerMock())
    
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
