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

from offer_search.core.ranking.base import Ranker


__all__ = [
    'ElasticsearchRanker',
]


class ElasticsearchRanker(Ranker):
    __DEFAULT_INDEX = 'offer_search'
    __DEFAULT_DOC_TYPE = 'product'

    __SEARCH_QUERY_ITEM = {
        'query': {
            'bool': {
                'must': [
                    {
                        'fuzzy': {
                            'Item': {
                                'value': None,
                                'prefix_length': 0,
                            }
                        },
                    },
                ],
                'should': [
                    {
                        'multi_match': {
                                'query': None,
                                'fields': ['Item', 'Attributes', 'Advert_text'],
                                'type': 'best_fields'
                            }
                    },
                ],
                'filter': [
                    {
                        'range': {
                            'Price': {
                                'gte': None,
                                'lte': None,
                            }
                        },
                    },
                    {
                        'range': {
                            'Cashback': {
                                'gte': None,
                            }
                        },
                    },
                    {
                        'range': {
                            'Offer_type': {
                                'gte' : None,
                                'lte' : None,
                            }
                        }
                    },
                ]
            },
        },
        'size': 10000,
    }


    __SEARCH_QUERY_ATTRIBUTES = {
        'query': {
            'bool': {
                'should': [
                    {
                        'multi_match': {
                                'query': None,
                                'fields': ['Item', 'Attributes', 'Advert_text'],
                                'type': 'best_fields'
                            }
                    },
                ],
                'filter': [
                    {
                        'range': {
                            'Price': {
                                'gte': None,
                                'lte': None,
                            }
                        },
                    },
                    {
                        'range': {
                            'Cashback': {
                                'gte': None,
                            }
                        },
                    },
                    {
                        'range': {
                            'Offer_type': {
                                'gte' : None,
                                'lte' : None,
                            }
                        }
                    },
                ]
            },
        },
        'size': 10000,
    }

    __KEYS_TO_SET_ITEM = ('query', 'bool', 'must', 0, 'fuzzy', 'Item', 'value')
    __KEYS_TO_SET_ATTRIBUTES = ('query', 'bool', 'should', 0, 'multi_match', 'query')
    __KEYS_TO_SET_PRICE_FROM = ('query', 'bool', 'filter', 0, 'range', 'Price', 'gte')
    __KEYS_TO_SET_PRICE_TO = ('query', 'bool', 'filter', 0, 'range', 'Price', 'lte')
    __KEYS_TO_SET_CASHBACK = ('query', 'bool', 'filter', 1, 'range', 'Cashback', 'gte')
    __KEYS_TO_SET_OFFER_TYPE_FROM = ('query', 'bool', 'filter', 2, 'range', 'Offer_type', 'gte')
    __KEYS_TO_SET_OFFER_TYPE_TO = ('query', 'bool', 'filter', 2, 'range', 'Offer_type', 'lte')

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
        search_result = self.__elasticsearch.search(
            index=self.__index,
            doc_type=self.__doc_type,
            body=self.__build_search_query(search_form),
        )

        return [record['_source'] for record in search_result['hits']['hits']]

    def __preset(self, preset: t.List[t.Dict[str, t.Any]]) -> t.NoReturn:
        for record in preset:
            self.__elasticsearch.index(
                index=self.__index, 
                doc_type=self.__doc_type, 
                body=record,
            )

    @classmethod
    def __build_search_query(cls, search_form: t.Dict[str, t.Any]) -> t.List[t.Dict[str, t.Any]]:
        if 'Item' in search_form:
            search_query = deepcopy(cls.__SEARCH_QUERY_ITEM)

            for query_keys, query_value in (
                (cls.__KEYS_TO_SET_ITEM, search_form['Item']),
                (cls.__KEYS_TO_SET_ATTRIBUTES, search_form['Attributes']),
                (cls.__KEYS_TO_SET_PRICE_FROM, search_form['Price_from']),
                (cls.__KEYS_TO_SET_PRICE_TO, search_form['Price_to']),
                (cls.__KEYS_TO_SET_CASHBACK, search_form['Cashback']),
                (cls.__KEYS_TO_SET_OFFER_TYPE_FROM, search_form['Offer_type_from']),
                (cls.__KEYS_TO_SET_OFFER_TYPE_TO, search_form['Offer_type_to']),
            ):
                cls.__set_query_value(search_query, query_keys, query_value)
        else:
            search_query = deepcopy(cls.__SEARCH_QUERY_ATTRIBUTES)

            for query_keys, query_value in (
                (cls.__KEYS_TO_SET_ATTRIBUTES, search_form['Attributes']),
                (cls.__KEYS_TO_SET_PRICE_FROM, search_form['Price_from']),
                (cls.__KEYS_TO_SET_PRICE_TO, search_form['Price_to']),
                (cls.__KEYS_TO_SET_CASHBACK, search_form['Cashback']),
                (cls.__KEYS_TO_SET_OFFER_TYPE_FROM, search_form['Offer_type_from']),
                (cls.__KEYS_TO_SET_OFFER_TYPE_TO, search_form['Offer_type_to']),
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
