from urllib3 import Retry


def get_default_retries():
    return Retry(
        total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
    )
