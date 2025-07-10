import os
import sys
import time
import glob
from pathlib import Path
from urllib.parse import urlparse
from typing import List, Tuple

from config import load_config, Config
from parser_yandex_pairs import YandexPairParser, PairParseResult
from page_html_export import PageHTMLExport


def does_site_belong_to_domains(site_netloc: str, domains: List[str]) -> bool:
    for include_domain in domains:
        if site_netloc.endswith(include_domain):
            return True

    return False


def apply_filters(app_config: Config, pairs: List[Tuple[str, PairParseResult]]) -> List[Tuple[str, PairParseResult]]:
    filtered_pairs = []

    for img_path, site_pair in pairs:
        site_netloc = urlparse(site_pair.page.url).netloc

        if site_netloc in app_config.exclude_sites:
            continue

        if (app_config.include_only_domains
                and not does_site_belong_to_domains(site_netloc, app_config.include_only_domains)):
            continue

        if app_config.include_only_sites and site_netloc not in app_config.include_only_sites:
            continue

        filtered_pairs.append((img_path, site_pair))

    return filtered_pairs


def main():
    app_config = load_config()
    html_export = PageHTMLExport(template_path='template.html')
    parser = YandexPairParser(settings={})

    t1 = time.time()

    image_folder = sys.argv[1] if len(sys.argv) > 1 else r'Images\Big'
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

    found_pages = apply_filters(app_config, found_pages)
    found_pages.sort(key=lambda p: urlparse(p[1].page.url).netloc)
    html_export.save(pages=found_pages, output=f'{int(time.time())}_output.html')

    if failed_images:
        print('Failed images:', '\n'.join(failed_images))

    t2 = time.time()
    print('Time:', t2 - t1)
    os.system('PAUSE')


if __name__ == '__main__':
    main()
