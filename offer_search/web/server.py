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

import aiohttp_jinja2
import jinja2
from aiohttp import web

from offer_search.web import views


__all__ = [
    'HttpServer',
]


logger = logging.getLogger(__name__)


class HttpServer:
    def __init__(
        self, 
        listen_host: str, 
        listen_port: int,
        template_path: t.Optional[str] = '',
        static_path: t.Optional[str] = '',
    ) -> None:
        self.__host = listen_host
        self.__port = listen_port

        self.__application = web.Application()

        aiohttp_jinja2.setup(self.__application, loader=jinja2.FileSystemLoader(template_path))

        self.__application.router.add_view('/', views.IndexView, name='index')
        self.__application.router.add_view('/offer_search', views.OfferSearchView, name='offer_search')
        self.__application.router.add_static('/static', path=static_path, name='static')

    def start(self) -> t.NoReturn:
        logger.info(f"start the server: http://{self.__host}:{self.__port}")

        web.run_app(self.__application, host=self.__host, port=self.__port)
