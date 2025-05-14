from abc import ABC, abstractmethod
from typing import List

import requests

from libs.lib_types import BaseParseResult, ImageParseResult, PageParseResult, PairParseResult, \
    PageSnapshotParseResult


class AbstractParser(ABC):
    def __init__(self, settings: dict, request_session: requests.Session = None):
        pass

    @abstractmethod
    def execute(self, url: str) -> List[BaseParseResult]:
        pass


class BaseImageParser(AbstractParser, ABC):
    def __init__(self, settings: dict, request_session: requests.Session = None):
        pass

    @abstractmethod
    def execute(self, url: str) -> List[ImageParseResult]:
        pass


class BasePageParser(AbstractParser, ABC):
    def __init__(self, settings: dict, request_session: requests.Session = None):
        pass

    @abstractmethod
    def execute(self, url: str) -> List[PageParseResult]:
        pass


class BasePairParser(AbstractParser, ABC):
    def __init__(self, settings: dict, request_session: requests.Session = None):
        pass

    @abstractmethod
    def execute(self, image_url: str) -> List[PairParseResult]:
        pass


class BasePageSnapshotParser(AbstractParser, ABC):
    def __init__(self, settings: dict, request_session: requests.Session = None):
        pass

    @abstractmethod
    def execute(self, url: str) -> List[PageSnapshotParseResult]:
        pass
