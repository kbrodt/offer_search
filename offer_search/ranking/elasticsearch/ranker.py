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

from overrides import overrides

from offer_search.ranking.base import Ranker


__all__ = [
    'ElasticsearchRanker',
]


class ElasticsearchRanker(Ranker):
    @overrides
    def rank(self, search_form: t.Dict[str, t.Any]) -> t.List[t.Dict[str, t.Any]]:
        pass
