#
#  Project: Offer Search
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-02-03
#
#  GitHub: @ameyuuno
#

import json
import typing as t
from pathlib import Path

from offer_search.core.intent_classification import IntentClassifier
from offer_search.core.intent_classification.standard import CompositeVectorizer
from offer_search.core.intent_classification.standard import LogisticRegressionModel
from offer_search.core.intent_classification.standard import Preprocessor
from offer_search.core.intent_classification.standard import StandardIntentClassifier
from offer_search.core.intent_classification.standard import TfidfVectorizer
from offer_search.core.slot_filling import SlotFiller
from offer_search.core.slot_filling.slot_filling import SlotFillerWithRules
from offer_search.core.ranking import Ranker
from offer_search.core.ranking.elasticsearch import ElasticsearchRanker


__all__ = [
    'create_intent_classifier',
    'create_slot_filler',
    'create_ranker',
]


def create_intent_classifier(
    resource_directory: Path = Path('./resources/intent_classification'),
    over_words_vectorizer_name: str = 'over_words_vectorizer.joblib',
    over_trigrams_vectorizer_name: str = 'over_trigrams_vectorizer.joblib',
    classifier_name: str = 'classifier.joblib',
    label_encoder_name: str = 'label_encoder.joblib',
) -> IntentClassifier:
    return StandardIntentClassifier(
        Preprocessor(download_if_missing=True),
        CompositeVectorizer([
            TfidfVectorizer(resource_directory / over_words_vectorizer_name),
            TfidfVectorizer(resource_directory / over_trigrams_vectorizer_name),
        ]),
        LogisticRegressionModel(
            resource_directory / classifier_name,
            resource_directory / label_encoder_name,
        ),
    )


def create_slot_filler() -> SlotFiller:
    return SlotFillerWithRules()


def create_ranker(
    elasticsearch_host: str = 'localhost',
    elasticsearch_port: int = 9200,
    preset_path: t.Optional[Path] = None,
) -> Ranker:
    preset = None

    if preset_path is not None:
        with preset_path.open('r') as preset_file:
            preset: t.List[t.Dict[str, t.Any]] = json.load(preset_file)

    return ElasticsearchRanker(
        elasticsearch_host,
        elasticsearch_port,
        preset=preset,
    )
