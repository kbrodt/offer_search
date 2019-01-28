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

import typing as t

from nltk import download
from nltk.data import find


__all__ = [
    'NltkResourceManager',
]


class NltkResourceManager:
    """NLTK Resource Manager

    This manager contains methods to work with NLTK resources: check if resources exist, download
    resources, update NLTK path.
    """

    RESOURCES = {
        'punkt': 'tokenizers/punkt',
        'stopwords': 'corpora/stopwords',
    }

    def check_resources(
        self, 
        resources: t.List[str], 
        download_if_missing: bool = False,
    ) -> t.NoReturn:
        for resource in resources:
            if not (self.exist_resource(resource) or download_if_missing):
                raise LookupError(
                    f"NLTK resource {resource} is missing. Try to fix it with "
                    f"`import nltk; nltk.download('{resource}')`"
                )

            download(resource, quiet=True)

    def exist_resource(self, resource: str) -> bool:
        """Checks NLTK resource exists or not

        :param resource: name of downloading resource ('punkt', 'stopwords', etc.)
        :return: `True` if resource exists else `False`
        """

        nltk_resource = self.RESOURCES.get(resource)

        if nltk_resource is None:
            raise ValueError(
                f"Unknown NLTK resource '{resource}'. Update `NltkResourceManager.RESOURCE`"
            )

        try:
            find(nltk_resource)

        except LookupError:
            return False

        return True
