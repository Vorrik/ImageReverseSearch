import time
from typing import List

import re
import json
# from requests import Session

from curl_cffi import Session
from libs.lib_base import BasePairParser
from libs.lib_types import PairParseResult, ImageParseResult, PageParseResult


class YandexPairParser:
    """
    Searches for image sources by image URL using yandex services
    """

    def __init__(self, settings: dict):
        self.session = None
        self.setup_session()

    def setup_session(self) -> None:
        self.session = Session(impersonate='chrome136', verify=False)

        # self.session.headers.update(
        #     {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        # )

        # self.session.headers.update(
        #     {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'}
        # )

        # self.session.hooks.update(
        #     {'response': lambda r, *args, **kwargs: r.raise_for_status()}
        # )

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

            headers = {
                # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                # 'accept-language': 'en-GB,en;q=0.9',
                # 'cache-control': 'no-cache',
                # 'priority': 'u=0, i',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                # 'sec-fetch-dest': 'document',
                # 'sec-fetch-mode': 'navigate',
                # 'sec-fetch-site': 'none',
                # 'sec-fetch-user': '?1'
            }

            params = {
                'rpt': 'imageview',
                'url': upload_response['url'],
            }

            response = self.session.get(url='https://yandex.ru/images/search', params=params, headers=headers)

            # response = self.session.get(url='https://yandex.ru/images/search?rpt=imageview&url=https%3A%2F%2Favatars.mds.yandex.net%2Fget-images-cbir%2F1006159%2FmnlA1nTz781HM0nFNFwxgg8459%2Forig',
            #                             headers=headers, impersonate='chrome136')

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

    def unsafe_execute(self, image_url: str) -> List[PairParseResult]:
        response = self.request_search_by_image(image_url)
        return self.extract_image_sources(response)

    def execute(self, image_url: str) -> List[PairParseResult]:
        while True:
            try:
                return self.unsafe_execute(image_url)
            except AttributeError:
                self.setup_session()
                print('sleeping')
                time.sleep(60 * 5)
                # return self.unsafe_execute(image_url)
