from datetime import date
from dataclasses import dataclass, asdict
from requests import Session

from requests.adapters import HTTPAdapter, Retry


# TODO: Proof of concept. Split into multiple files / modules.

session = requests.Session()

def get_default_retries():
    return Retry(total=5,
                 backoff_factor=0.1,
                 status_forcelist=[ 500, 502, 503, 504 ])


class CheckerAPIError(RuntimeError):
    pass

class CheckerAPIFailedCreation(CheckerAPIError):
    pass


class CheckrAPI:
    def __init__(self, secret_api_key: str, session: Session = Session(), retries: Retry = get_default_retries()) -> None:
        self.session = session
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.secret_api_key = secret_api_key

    def create_candidate(self, candidate_data: dict) -> Candidate:
        self.session.post("some.checkr.com/path", data=candidate_data)



@dataclass
class Candidate:
    checker_api: CheckerAPI  # Needs this for updating, etc.

    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: str  # TODO: Validate email?
    phone: str
    zipcode: str
    dob: date
    ssn= str
    driver_license_number: str
    driver_license_state: str
    copy_requested: bool
    work_locations: list[dict[str, str]]

    id: Optional[int] = None  # From API Creation Response

    def save(self, raise_on_failure: bool = True) -> bool:
        self_data = asdict(self)
        self_data["no_middle_name"] = bool(self.middle_name)

        try:
            response = self.checker_api.create_candidate(self_data)
        except HttpException:
            if raise_on_failure:
                raise
            return False

        if "id" not in response:
            if raise_on_failure:
                raise CheckerAPIFailedCreation
            return False

        self.id = response["id"]

        return True

my_checkr_api = CheckerAPI()
zach = Candidate(checker_api=my_checker_api, first_name="zach", last_name="aysan", etc="etc")

assert zach.id is None

did_it_save = zach.save(raise_on_failure=False)

assert did_it_save is False
