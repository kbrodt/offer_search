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

"""Text Generator Interface Module
"""

import abc
import typing as t

__all__ = [
    'TextGenerator',
]


class TextGenerator(metaclass=abc.ABCMeta):
    """Text Generator Interface
    """

    @abc.abstractmethod
    def generate(
        self,
        joiner: t.Callable[[t.Iterable[str]], str],
        filter_: t.Callable[[t.Iterable[str]], bool],
    ) -> t.Iterable[str]:
        """Returns iterator over generated texts

        :param joiner: function which joins parts into text
        :param filter_: function which filters combinations which will not be used
        """
        pass
