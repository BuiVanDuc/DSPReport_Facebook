import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(PROJECT_ROOT)

EXPORT_CSV_DIR = os.path.join(BASE_DIR, "data", "export")

EXPORT_DOWNLOAD_DIR = os.path.join(BASE_DIR, "data", "downloads")

EXPORT_ACCOUNT_ERROR_DIR = os.path.join(BASE_DIR, "account_error")

CONFIGS_DIR = os.path.join(BASE_DIR, "configs")

