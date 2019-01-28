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

from offer_search.utils.dataset.text_generator.base import TextGenerator
from offer_search.utils.dataset.text_generator.simple_generator import SimpleTextGenerator
from offer_search.utils.dataset.text_generator.variant_text_generator import VariantTextGenerator
from offer_search.utils.dataset.text_generator.placeholder_generator import PlaceholderTextGenerator


__all__ = [
    'TextGenerator',
    'SimpleTextGenerator',
    'VariantTextGenerator',
    'PlaceholderTextGenerator',
]
