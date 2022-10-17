from datetime import date
from dataclasses import dataclass, asdict

import requests
from requests import Session

from requests.adapters import HTTPAdapter, Retry

from lib.candidate import Candidate

# TODO: Proof of concept. Split into multiple files / modules.

session = requests.Session()


def get_default_retries():
    return Retry(total=5,
                 backoff_factor=0.1,
                 status_forcelist=[500, 502, 503, 504])


class CheckrAPI:
    def __init__(self, secret_api_key: str, session: Session = Session(),
                 retries: Retry = get_default_retries()) -> None:
        self.session = session
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.secret_api_key = secret_api_key

    def create_candidate(self, candidate_data: dict) -> Candidate:
        self.session.post("some.checkr.com/path", data=candidate_data)


my_checkr_api = CheckerAPI()
zach = Candidate(checker_api=my_checker_api,
                 first_name="zach",
                 last_name="aysan",
                 etc="etc")

assert zach.id is None

did_it_save = zach.save(raise_on_failure=False)

assert did_it_save is False
