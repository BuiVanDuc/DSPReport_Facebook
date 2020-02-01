import os
import re

from utils.file_utils import get_cfg, unzip_file_gz
from settings import EXPORT_CSV_DIR


def build_params(file_cfg, start_date, end_date):
    data = get_cfg(file_cfg, type="yaml")
    params = {
        "during": "{},{}".format(start_date, end_date),
        "fields": "",
        "breakdows": data["breakdows"],
        "level": data["level"]
    }
    fields = ','.join(str(item) for item in data["fields"])

    params["fields"] = fields

    return params


def create_csv_report(file_gz):
    file_name = "something"
    file_out = os.path.join(EXPORT_CSV_DIR, file_name)
    unzip_file_gz(file_gz, file_out)
    # Process data


def search_data_by_regex(regex, str_data):
    if str:
        match = re.search(regex, str_data)
        return match


def process_data(list_data):
    list_rows = []
    for line in list_data:
        list_value = line.split("\t")

        # Field likes and total_action
        actions_type = list_value[-3]
        value_like = ''
        value_total_action = 0
        regex_value = r'/d+'
        if actions_type:
            # Field likes
            regex = r'{"action_type":"like","value":"\d+"}'
            match = search_data_by_regex(regex, actions_type)
            if match:
                str_temp = match.group()
                # Search value of like in string of type_like
                match = search_data_by_regex(regex_value, str_temp)
                if match:
                    value_like = match.group()
            # Field total_action
            regex = r'{"action_type":"offsite_conversion.fb_pixel_purchase","value":"\d+"}'
            match = search_data_by_regex(regex, actions_type)
            if match:
                str_temp = match.group()
                # Search value of like in string of type_like
                match = search_data_by_regex(regex_value, str_temp)
                if match:
                    value_total_action = match.group()
        list_value[-3] = value_like

        # Field currency
        currency = list_value[-1].replace('"','')
        list_value[-1] = currency

        # Append total_action
        data = '\t'.join(str(item) for item in list_value)
        list_value.append(value_total_action)

        # Append data to list_row []
        list_rows.append(list_value)


def get_header(file_cfg):
    data = get_cfg(file_cfg, type="yaml")
    list_fields = data["fields"]
    return '\t'.join(str(item) for item in list_fields)
