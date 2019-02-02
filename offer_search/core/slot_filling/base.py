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
    'SlotFiller',
]


class SlotFiller(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fill(self, text: str, intent: str) -> t.Dict[str, t.Any]:
        pass
