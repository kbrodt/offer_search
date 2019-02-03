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

import logging
import typing as t
from json import JSONDecodeError

import aiohttp_jinja2
from aiohttp import web

from offer_search.core import Searcher

__all__ = [
    'IndexView',
    'OfferSearchView',
]


logger = logging.getLogger(__name__)


class IndexView(web.View):
    @aiohttp_jinja2.template('index.jinja2')
    async def get(self) -> t.Dict[str, t.Any]:
        logger.info("http :: index page handler")

        return dict()


class OfferSearchView(web.View):
    async def post(self) -> t.List[t.Dict[str, t.Any]]:
        logger.info("http :: search offer handler")

        try:
            request_body = await self.request.json()
            query = request_body['query']
            logger.info(f"Query: {query}")

            searcher: Searcher = self.request.app['searcher']

            offers = searcher.search(query)
            logger.info(f"Found offers: {offers}")

            return web.json_response(offers, status=200)
        
        except (KeyError, JSONDecodeError) as err:
            logger.error(str(err))

            return web.json_response(
                {'error': str(err)},
                status=400,
            )
