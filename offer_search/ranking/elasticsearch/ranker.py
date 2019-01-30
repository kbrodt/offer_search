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

from elasticsearch import Elasticsearch
from overrides import overrides

from offer_search.ranking.base import Ranker


__all__ = [
    'ElasticsearchRanker',
]


class ElasticsearchRanker(Ranker):
    __DEFAULT_INDEX = 'offer_search'
    __DEFAULT_DOC_TYPE = 'offer'

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
        raise NotImplementedError

    def __preset(self, preset: t.List[t.Dict[str, t.Any]]) -> None:
        for record in preset:
            self.__elasticsearch.index(
                index=self.__index, 
                doc_type=self.__doc_type, 
                body=record,
            )
