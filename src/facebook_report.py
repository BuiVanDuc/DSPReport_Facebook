import os

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