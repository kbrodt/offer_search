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

from overrides import overrides


__all__ = [
    'Tokenizer',
    'Filter',
    'Normalizer',
    'SimpleTokenizer',
    'SimpleFilter',
    'SimpleNormalizer',
]


class Tokenizer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def split(self, text: str) -> t.List[str]:
        pass


class SimpleTokenizer(metaclass=abc.ABCMeta):
    @overrides
    def split(self, text: str) -> t.List[str]:
        return text.split()


class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def filter(self, tokens: t.List[str]) -> t.List[str]:
        pass
        return text.split()


class SimpleFilter(metaclass=abc.ABCMeta):
    @overrides
    def filter(self, tokens: t.List[str]) -> t.List[str]:
        return tokens


class Normalizer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def normalize(self, tokens: t.List[str]) -> t.List[str]:
        pass
        return tokens


class SimpleNormalizer(metaclass=abc.ABCMeta):
    @overrides
    def normalize(self, tokens: t.List[str]) -> t.List[str]:
        return tokens
