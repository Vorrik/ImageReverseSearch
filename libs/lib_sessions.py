import os

import requests as r
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def create_request_session_with_http_proxy(proxy_ip, proxy_port, proxy_login, proxy_password):
    requests_session = r.Session()
    auth_str = f"{proxy_login}:{proxy_password}@" if proxy_login and proxy_password else ""
    proxy_url = f'{auth_str}{proxy_ip}:{proxy_port}'
    requests_session.proxies = {
        'http': f'http://{proxy_url}',
        'https': f'http://{proxy_url}',
    }
    return requests_session


def setup_retry_policy(request_session: r.Session):
    retry = Retry(total=4, backoff_factor=1.1, status_forcelist=[
        500, 502, 503, 504,
        401, 403
    ])
    request_session.mount('https://', HTTPAdapter(max_retries=retry))
    request_session.mount('http://', HTTPAdapter(max_retries=retry))


def create_request_session(settings: dict):
    if settings.get('is_use_proxy'):
        request_session = create_request_session_with_http_proxy(
            proxy_ip=settings['proxy_ip'],
            proxy_port=settings['proxy_port'],
            proxy_login=settings.get('proxy_login'),
            proxy_password=settings.get('proxy_password')
        )
    else:
        request_session = r.Session()
    setup_retry_policy(request_session)
    return request_session


def create_parsers_request_session():
    settings = {}
    settings['is_use_proxy'] = os.environ.get('IS_USE_PROXY', '0') == '1'
    if settings['is_use_proxy']:
        settings['proxy_ip'] = os.environ.get('PROXY_IP')
        settings['proxy_port'] = os.environ.get('PROXY_PORT')
        settings['proxy_login'] = os.environ.get('PROXY_LOGIN')
        settings['proxy_password'] = os.environ.get('PROXY_PASSWORD')
    return create_request_session(settings=settings)