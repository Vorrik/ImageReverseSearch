import os
import sys
import time
import glob
from pathlib import Path
from urllib.parse import urlparse

from libs.lib_sessions import create_request_session
from parser_yandex_pairs import YandexPairParser
from page_html_export import PageHTMLExport


def main():
    html_export = PageHTMLExport(template_path='template.html')
    parser = YandexPairParser(settings={}, request_session=create_request_session({}))

    t1 = time.time()

    image_folder = sys.argv[1] if len(sys.argv) > 1 else r'Images\Compressed'
    images = glob.glob(image_folder + r'\**\*.*', recursive=True)
    print('Loaded', len(images), 'files from', image_folder)

    found_pages = []
    failed_images = []
    for i, img_path in enumerate(images):
        try:
            print(f'[{i + 1}/{len(images)}] Parsing {img_path}')
            results = parser.execute(img_path)
            relative_img_path = os.path.relpath(img_path, Path().absolute())
            found_pages.extend([(relative_img_path, page) for page in results])

            # print(results)
            print('Size:', len(results))
        except Exception as e:
            print('Failed to parse:', e)
            failed_images.append(img_path)

    found_pages.sort(key=lambda p: urlparse(p[1].page.url).netloc)
    html_export.save(pages=found_pages, output=f'{int(time.time())}_output.html')

    if failed_images:
        print('Failed images:', '\n'.join(failed_images))

    t2 = time.time()
    print('Time:', t2 - t1)
    os.system('PAUSE')


if __name__ == '__main__':
    main()
