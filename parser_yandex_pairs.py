from typing import List

import re
import json
from requests import Session

from libs.lib_base import BasePairParser
from libs.lib_types import PairParseResult, ImageParseResult, PageParseResult


class YandexPairParser(BasePairParser):
    """
    Searches for image sources by image URL using yandex services
    """

    def __init__(self, settings: dict, request_session: Session = None):
        super().__init__(settings)
        self.session = request_session

        self.session.headers.update(
            {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        )

        self.session.hooks.update(
            {'response': lambda r, *args, **kwargs: r.raise_for_status()}
        )

    def request_search_by_image(self, image_url: str) -> str:
        #  Дебажить запросы нужно с самого начала https://yandex.ru/images/
        #  'request': '{"blocks":[{"block":"content_type_search-by-image"}]}'

        with open(image_url, "rb") as image:
            image_data = image.read()
            upload_response = self.session.post(url='https://yandex.ru/images-apphost/image-download',
                                                headers={'content-type': 'image/jpeg'},
                                                params={'images_avatars_size': 'orig',
                                                        'images_avatars_namespace': 'images-cbir'},
                                                data=image_data).json()

            params = {
                'rpt': 'imageview',
                'url': upload_response['url'],
            }

            response = self.session.get(url='https://yandex.ru/images/search', params=params)
            return response.text.replace('&quot;', '"').replace('&amp;', '&')

    @staticmethod
    def extract_image_sources(html_block: str) -> List[PairParseResult]:
        # div id 'ImagesApp-PQj4ZjZ' -> attr 'data-state'
        json_str = re.search(r'(?<="cbirSites":).*?(?=])', html_block).group(0) + ']}'
        raw_image_sources = json.loads(json_str)['sites']

        return [PairParseResult(
            image=ImageParseResult(url=source['originalImage']['url']),
            page=PageParseResult(url=source['url'], title=source['title'])
        ) for source in raw_image_sources]

    def execute(self, image_url: str) -> List[PairParseResult]:
        response = self.request_search_by_image(image_url)
        return self.extract_image_sources(response)
