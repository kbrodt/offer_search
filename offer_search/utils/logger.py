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


__all__ = [
    'setup_logging',
]


def setup_logging(configuration: t.Dict[str, t.Any], logger_name: t.Optional[str] = None) -> None:
    logger_name = logger_name or __package__.split('.', maxsplit=1)[0]
    logging_level = logging.getLevelName(configuration['LOGGING_LEVEL'])

    formatter = logging.Formatter(configuration['LOG_TEMPLATE'])

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    logger.addHandler(stream_handler)
