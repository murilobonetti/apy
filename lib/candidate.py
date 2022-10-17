from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional

from lib.checkr_api import CheckerAPIFailedCreation


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
    ssn = str
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
