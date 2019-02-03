#
#  Project: Offer Search
#
#  Course: CompTech2019
#      Novosibirsk State University
#
#  Created by ameyuuno on 2019-02-03
#
#  GitHub: @ameyuuno
#

import json
import sys
import typing as t
from pathlib import Path

import tqdm
from elasticsearch import Elasticsearch


DEFAULT_INDEX = 'offer_search'
DEFAULT_DOC_TYPE = 'product'


def connect_elasticsearch(es_host: str = 'localhost', es_port: int = 9200) -> Elasticsearch:
    return Elasticsearch([{
        'host': es_host,
        'port': es_port,
    }])


def preset(
    preset: t.List[t.Dict[str, t.Any]],
    index: str = DEFAULT_INDEX,
    doc_type: str = DEFAULT_DOC_TYPE,
) -> t.NoReturn:
    for record in tqdm.tqdm(
        preset,
        desc='[ Indexing.. ]',
        mininterval=1,
        leave=False,
    ):
        self.__elasticsearch.index(index=index, doc_type=doc_type, body=record)


def main(preset_path: Path) -> t.NoReturn:
    es = connect_elasticsearch()

    with preset_path.open('r') as preset_file:
        preset(json.load(preset_file))

if __name__ == '__main__':
    main(Path(sys.argv[1]))
