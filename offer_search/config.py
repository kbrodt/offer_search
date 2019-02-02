#
#  Project: Offer Search
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-02-02
#
#  GitHub: @ameyuuno
#

import typing as t
from os import getenv

from dotenv import find_dotenv
from dotenv import load_dotenv


__all__ = [
    'CONFIGURATION',
]


__DEFAULT_LOG_TEMPLATE = '[%(asctime)-23s] %(name)-80s %(filename)35s:%(lineno)-10d ' \
                         '%(levelname)-8s %(message)s'



def __build_configuration() -> t.Dict[str, t.Any]:
    load_dotenv(find_dotenv())

    configuration_core = {
        'RANKER_ELASTICSEARCH_HOST': getenv('RANKER_ELASTICSEARCH_HOST', 'localhost'),
        'RANKER_ELASTICSEARCH_PORT': int(getenv('RANKER_ELASTICSEARCH_PORT', '9200')),
    }

    configuration_logging = {
        'LOGGING_LEVEL': getenv('LOGGING_LEVEL', default='INFO'),
        'LOG_TEMPLATE': getenv('LOG_TEMPLATE', default=__DEFAULT_LOG_TEMPLATE),
    }

    configuration_server = {
        'LISTEN_HOST': getenv('LISTEN_HOST', default='0.0.0.0'),
        'LISTEN_PORT': int(getenv('LISTEN_PORT', default='8080')),

        'TEMPLATES_PATH': getenv('TEMPLATES_PATH', default='./resources/web/templates/'),
        'STATIC_PATH': getenv('STATIC_PATH', default='./resources/web/static/'),
    }

    return {
        **configuration_core,
        **configuration_logging,
        **configuration_server,
    }


CONFIGURATION: t.Dict[str, t.Any] = __build_configuration()
