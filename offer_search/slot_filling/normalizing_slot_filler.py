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

import abc
import typing as t

from .base import SlotFiller


__all__ = [
    'NormalizingSlotFiller',
]


class NormalizingSlotFiller(SlotFiller, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def normalize(self, form: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """Takes form and returns new form with its normalized values
        """
        pass
