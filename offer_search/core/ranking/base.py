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

import abc
import typing as t


__all__ = [
    'Ranker',
]


class Ranker(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def rank(self, search_form: t.Dict[str, t.Any]) -> t.List[t.Dict[str, t.Any]]:
        pass
