import datetime
from dataclasses import dataclass, field


@dataclass
class BaseParseResult:
    meta: dict = field(init=False, hash=False, default_factory=dict)


@dataclass(unsafe_hash=True)
class ImageParseResult(BaseParseResult):
    url: str


@dataclass(unsafe_hash=True)
class PageParseResult(BaseParseResult):
    url: str
    title: str


@dataclass(unsafe_hash=True)
class PairParseResult(BaseParseResult):
    image: ImageParseResult
    page: PageParseResult


@dataclass(unsafe_hash=True)
class PageSnapshotParseResult(BaseParseResult):
    page_url: str
    date: datetime.date
    snapshot_url: str

