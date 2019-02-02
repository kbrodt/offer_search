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

from offer_search import core


def main() -> t.NoReturn:
    """Entrypoint
    """

    searcher = core.Searcher(
        core.create_intent_classifier(), 
        core.create_slot_filler(), 
        core.create_ranker(),
    )

    while True:
        search_request = input("search => ")

        if search_request == '\q':
            break

        offers = searcher.search(search_request)

        print("offers =>")
        for i, offer in enumerate(offers):
            print(f"\tOffer #{i + 1}\n\t{json.dumps(offer, ensure_ascii=False, indent=2)}")
 

if __name__ == '__main__':
    main()
