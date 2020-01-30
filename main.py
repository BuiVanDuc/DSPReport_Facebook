# -*- coding: utf-8 -*-
import os
from random import randint
from time import sleep

from src.facebook_report import create_csv_report
from utils.file_utils import download_file, write_data_to_file, read_file_account
from utils.logger_utils import logger
from utils.req_utils import request_gateway_api, initialize_url
from settings import EXPORT_DOWNLOAD_DIR, EXPORT_ACCOUNT_ERROR_DIR, CONFIGS_DIR

'''
-----STATUS----
1: SUBMIT
2: COMPLETED
3: ERROR
'''

# initialization
# file_account = 'account_manager.txt'
# file_account_error = "account_error.txt"
# list_accounts = read_file(file_account)

# file_config_url = {"{}/{}".format(BASE_DIR, 'url.json')}
# url = initialize_url(file_account)


def get_facebook_custom_report(list_accounts, url, params):
    list_req_error_accounts = []
    list_res_error_accounts = []
    if list_accounts and len(list_accounts) > 0:
        for account_id in list_accounts:
            url = url + str(account_id)
            # Step 1. Request to gateway api
            response = request_gateway_api(url, params=params)
            # Step 2. Get new resource
            if response.status_code == 201 or response.status_code == 200:
                data = response.headers()
                # The new resource is effectively created
                url = data.get('Location')
                # This response is sent back and the new resource is returned in the body of the message
                count = 0
                while True:
                    response = request_gateway_api(url)
                    if response and response.status_code == 201:
                        data = response.json()
                        if data.get("status") == "SUBMIT":
                            sleep(30)
                        elif data.get("status") == "COMPLETED":
                            # Download Facebook_CUSTOM_REPORT
                            file_gz = download_file(url, EXPORT_DOWNLOAD_DIR)
                            if file_gz and len(file_gz) > 0:
                                create_csv_report(file_gz)
                                break
                        elif data.get("status") == "ERROR":
                            sleep(5)
                            count += 1
                            if count > 3:
                                list_res_error_accounts.append(account_id)
                                break
                    else:
                        logger.info("[STATUS CODE] {} : {}".format(response.status_code, url))
                        list_req_error_accounts.append(account_id)
                        break
    else:
        logger.info("Account id is not existed".format())
    # Write res error account to file:
    if len(list_res_error_accounts) > 0:
        file_name = "res_error_account.txt"
        file_name = os.path.join(EXPORT_ACCOUNT_ERROR_DIR, file_name)
        for account_id in list_res_error_accounts:
            write_data_to_file(account_id, file_name)
    # Write req error account to file:
    if len(list_req_error_accounts) > 0:
        file_name = "req_error_account.txt"
        file_name = os.path.join(EXPORT_ACCOUNT_ERROR_DIR, file_name)
        for account_id in list_req_error_accounts:
            write_data_to_file(account_id, file_name)


# 2. Request gateway api
if __name__ == '__main__':
    file_account = "accounts.txt"
    list_accounts = read_file_account(file_account)
    file_cfg_url = os.path.join(CONFIGS_DIR, "json", "url.json")
    url = initialize_url(file_cfg_url)
    get_facebook_custom_report(list_accounts, url)
