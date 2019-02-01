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
from offer_search.intent_classification.standard import CompositeVectorizer
from offer_search.intent_classification.standard import LogisticRegressionModel
from offer_search.intent_classification.standard import Preprocessor
from offer_search.intent_classification.standard import StandardIntentClassifier
from offer_search.intent_classification.standard import TfidfVectorizer
from offer_search.searcher import Searcher
from offer_search.slot_filling import SlotFiller
from offer_search.slot_filling.slot_filling import SlotFillerWithRules
from offer_search.ranking import Ranker
from offer_search.ranking.elasticsearch import ElasticsearchRanker


def create_intent_classifier() -> IntentClassifier:
    resource_directory = Path('./resources/intent_classification')

    return StandardIntentClassifier(
        Preprocessor(download_if_missing=True),
        CompositeVectorizer([
            TfidfVectorizer(resource_directory / 'over_words_vectorizer.joblib'),
            TfidfVectorizer(resource_directory / 'over_trigrams_vectorizer.joblib'),
        ]),
        LogisticRegressionModel(
            resource_directory / 'classifier.joblib',
            resource_directory / 'label_encoder.joblib',
        ),
    )


def create_slot_filler() -> SlotFiller:
    return SlotFillerWithRules()


def create_ranker() -> Ranker:
    with Path('./resources/ranking/preset_small.json').open('r') as preset_file:
        preset: t.List[t.Dict[str, t.Any]] = json.load(preset_file)

    return ElasticsearchRanker(
        es_host='localhost',
        es_port=9200,
        preset=preset,
    )


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
            print(f"\tOffer #{i + 1}\n\t{json.dumps(offer, ensure_ascii=False, indent=2)}")
 

if __name__ == '__main__':
    main()
