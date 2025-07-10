from typing import List, Optional, Dict
from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    exclude_sites: List[str]
    include_only_domains: List[str]
    include_only_sites: List[str]


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        exclude_sites=env.list('EXCLUDE_SITES'),
        include_only_domains=env.list('INCLUDE_ONLY_DOMAINS'),
        include_only_sites=env.list('INCLUDE_ONLY_SITES')
    )
