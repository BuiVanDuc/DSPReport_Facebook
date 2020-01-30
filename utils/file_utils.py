import gzip
import json
import shutil

import yaml
import os
import urllib.request
from os.path import basename
from pathlib import Path
from urllib.parse import urlsplit

from utils.logger_utils import logger


def read_file_account(file_name):
    # Check file_name is existed or not
    list_ids = []
    if is_file_existed(file_name):
        with open(file_name) as f:
            list_ids = f.readlines()
        if list_ids and len(list_ids) > 0:
            # Process id
            list_ids = [id.strip() for id in list_ids]
            return list_ids
    # Logs
    logger.info("{} is not existed".format(file_name))
    return list_ids


def write_data_to_file(data, file_name):
    if data:
        with open(file_name, "a") as file:
            file.write(data)
    else:
        # Logs
        logger.info("Data is not existed, Can not write data to file")


def is_file_existed(file_name):
    if file_name and len(file_name) > 0:
        file = Path(file_name)
        if file.is_file():
            return True
    return False


def unzip_file_gz(file_gz, file_out):
    if is_file_existed(file_gz):
        with gzip.open(file_gz, 'rb') as f_in:
            with open(file_out, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


def get_cfg(file_cfg, type="json"):
    """
    :param file_json:
    :param type: default json
    :return:
    """
    data = {}
    if is_file_existed(file_cfg):
        with open(file_cfg) as f:
            if type == "json":
                data = json.load(f)
            elif type == "yaml":
                data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    # Logs
    logger.info('{} is not existed'.format(file_cfg))
    return data


def download_file(url, out_path):
    file_name = url2name(url)
    response = urllib.request.urlopen(url)
    if 'Content-Disposition' in response.info():
        # If the response has Content-Disposition, we take file name from it
        file_name = response.info()['Content-Disposition'].split('filename=')[1]
        if file_name[0] == '"' or file_name[0] == "'":
            file_name = file_name[1:-1]
    elif response.url != url:
        # if we were redirected, the real file name we take from the final URL
        file_name = url2name(response.url)

    file_name = os.path.join(out_path, file_name)
    urllib.request.urlretrieve(url, file_name)
    return file_name


def url2name(url):
    return basename(urlsplit(url)[2])
