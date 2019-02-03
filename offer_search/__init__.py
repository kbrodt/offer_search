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

import asyncio
import logging
import typing as t

from offer_search.config import CONFIGURATION
from offer_search import core
from offer_search.utils.logger import setup_logging
from offer_search.web import HttpServer


__all__ = [
    'start_service',
]


logger = logging.getLogger(__name__)


def __create_searcher() -> core.Searcher:
    return core.Searcher(
        core.create_intent_classifier(),
        core.create_slot_filler(),
        core.create_ranker(
            CONFIGURATION['RANKER_ELASTICSEARCH_HOST'],
            CONFIGURATION['RANKER_ELASTICSEARCH_PORT'],
        ),
    )


def start_service() -> t.NoReturn:
    setup_logging(CONFIGURATION)

    server = HttpServer(
        CONFIGURATION['LISTEN_HOST'],
        CONFIGURATION['LISTEN_PORT'],
        CONFIGURATION['TEMPLATES_PATH'],
        CONFIGURATION['STATIC_PATH'],
    )
    server.add_property('searcher', __create_searcher())

    try:
        server.start()

    except KeyboardInterrupt:
        pass

    except Exception as err:
        logger.exception("Critical error occured in the service!")

    finally:
        loop = asyncio.get_event_loop()

        if not loop.is_closed():
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

