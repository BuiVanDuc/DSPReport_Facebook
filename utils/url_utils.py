# -*- coding: utf-8 -*-
import json
import re
import requests
from utils.logger_utils import logger
from utils.file_utils import get_cfg


def request_gateway_api(url, payload=None):
    r"""Sends a GET request.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    if is_url_validated(url):
        response = requests.get(url, params=payload)
        return response
    # Logs
    logger.info('{} is not validated'.format(url))
    return None


def is_url_validated(url):
    if url and len(url) > 0:
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or ftp://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url)
    return False


def initialize_url(file_cfg):
    data = get_cfg(file_cfg)
    if data:
        protocol = data.get("protocol")
        domain = data.get("domain")
        port = data.get("port")
        path = data.get("path")

        url = '{}://{}:{}{}'.format(protocol, domain, port, path)
        return url
