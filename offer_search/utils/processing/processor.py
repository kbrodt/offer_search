#
#  Project: Offer Search
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-01-28
#
#  GitHub: @ameyuuno
#

import abc
import typing as t


__all__ = [
    'Processor',
]


S = t.TypeVar('S')  # type of preprocessing source
T = t.TypeVar('T')  # type of preprocessing target


class Processor(t.Generic[S, T], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def process(self, source: S) -> T:
        pass
