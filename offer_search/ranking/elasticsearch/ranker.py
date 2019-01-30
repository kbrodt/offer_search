#
#  Project: Offer Search
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-01-29
#
#  GitHub: @ameyuuno
#

import typing as t
from copy import deepcopy
from operator import itemgetter

from elasticsearch import Elasticsearch
from overrides import overrides

from offer_search.ranking.base import Ranker


__all__ = [
    'ElasticsearchRanker',
]


class ElasticsearchRanker(Ranker):
    __DEFAULT_INDEX = 'offer_search'
    __DEFAULT_DOC_TYPE = 'offer'

    __SEARCH_QUERY = {
        'query': {
            'bool': {
                'must': [
                    {
                        'match': {
                            'Item': None,
                        },
                    },
                ],
                'filter': [
                    {
                        'range': {
                            'Price_from': {
                                'gte': None,
                            },
                            'Price_to': {
                                'lte': None,
                            },
                        },
                    },
                ],
            },
        },
    }
    __KEYS_TO_SET_ITEM = ('query', 'bool', 'must', 0, 'match', 'Item')
    __KEYS_TO_SET_PRICE_FROM = ('query', 'bool', 'filter', 0, 'range', 'Price_from', 'gte')
    __KEYS_TO_SET_PRICE_TO = ('query', 'bool', 'filter', 0, 'range', 'Price_to', 'lte')

    def __init__(
        self, 
        es_host: str = 'localhost', 
        es_port: int = 9200,
        index: str = __DEFAULT_INDEX,
        doc_type: str = __DEFAULT_DOC_TYPE,
        preset: t.Optional[t.List[t.Dict[str, t.Any]]] = None,
    ) -> None:
        self.__elasticsearch = Elasticsearch([{
            'host': es_host,
            'port': es_port,
        }])

        if not self.__elasticsearch.ping():
            raise ValueError(f"Can not connect to Elasticsearch: {es_host}:{es_port}")

        self.__index = index
        self.__doc_type = doc_type

        if preset is not None:
            self.__preset(preset)

    @overrides
    def rank(self, search_form: t.Dict[str, t.Any]) -> t.List[t.Dict[str, t.Any]]:
        search_response = self.__elasticsearch.search(
            index=self.__index,
            doc_type=self.__doc_type,
            body=self.__build_search_query(search_form),
        )

    def __preset(self, preset: t.List[t.Dict[str, t.Any]]) -> None:
        for record in preset:
            self.__elasticsearch.index(
                index=self.__index, 
                doc_type=self.__doc_type, 
                body=record,
            )

    @classmethod
    def __build_search_query(cls, search_form: t.Dict[str, t.Any]) -> t.List[t.Dict[str, t.Any]]:
        search_query = deepcopy(cls.__SEARCH_QUERY)

        for query_keys, query_value in (
            (cls.__KEYS_TO_SET_ITEM, search_form['Item']),
            (cls.__KEYS_TO_SET_PRICE_FROM, search_form['Price_from']),
            (cls.__KEYS_TO_SET_PRICE_TO, search_form['Price_to']),
        ):
            cls.__set_query_value(search_query, query_keys, query_value)

        return search_query

    @staticmethod
    def __set_query_value(query: t.Dict[str, t.Any], keys: t.Tuple[str], value: t.Any) -> t.NoReturn:
        container = query

        # try to come to penultimate ("last but one") contrainer, so use keys without its tail
        # it is nessaccary because otherwise we will lose reference to last container and will
        # not be able to set new value
        keys_to_penultimate_container = keys[:-1]
        last_key = keys[-1]

        for key in keys_to_penultimate_container:
            container = itemgetter(key)(container)

        container[last_key] = value
