from typing import List, Tuple
from pathlib import Path

from libs.lib_types import PairParseResult
from utils import resource_path


class PageHTMLExport:

    def __init__(self, template_path: str):
        with open(resource_path(template_path), 'r', encoding='utf-8') as file:
            self.template = file.read()

    def save(self, pages: List[Tuple[str, PairParseResult]], output: str) -> None:
        table_rows = [(f'<tr><td>{i}</td>'
                       f'<td class="img-column"><img src="{image_path}" alt=""/>{Path(image_path).name}</td>'
                       f'<td class="img-column"><img src="{page.image.url}" alt=""/></td>'
                       f'<td>{page.page.title}</td>'
                       f'<td><a href="{page.page.url}">{page.page.url}</a></td></tr>')
                      for i, (image_path, page) in enumerate(pages)]

        with open(output, 'w', encoding='utf-8') as f:
            generated_page = self.template.replace('[ROWS]', ''.join(table_rows))
            f.write(generated_page)
