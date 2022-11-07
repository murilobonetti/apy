from dataclasses import dataclass
from typing import Optional, Any

from requests import HTTPError

from lib.api.checkr_api import CheckrAPI
from lib.helpers.checkr_api_error import CheckerAPIFailedCreation


@dataclass
class Candidate:
    checkr_api: CheckrAPI
    first_name: str
    last_name: str
    email: str
    driver_license_number: str
    driver_license_state: str
    work_locations: list[dict[str, str]]
    id: Optional[str] = None
    adjudication: Optional[str] = None
    copy_requested: Optional[bool] = None
    custom_id: Optional[str] = None
    dob: Optional[str] = None
    geo_ids: Optional[list[str]] = None
    middle_name: Optional[str] = None
    mother_maiden_name: Optional[str] = None
    no_middle_name: Optional[bool] = None
    object: Optional[str] = None
    phone: Optional[str] = None
    previous_driver_license_number: Optional[str] = None
    previous_driver_license_state: Optional[str] = None
    report_ids: Optional[list[str]] = None
    ssn: Optional[str] = None
    uri: Optional[str] = None
    zipcode: Optional[str] = None

    def create(self, raise_on_failure: bool = True) -> bool:
        try:
            candidate = self._create_via_api()
        except HTTPError:
            if raise_on_failure:
                raise
            return False

        if "id" not in candidate:
            if raise_on_failure:
                raise CheckerAPIFailedCreation
            return False

        self.id = candidate["id"]
        self.adjudication = candidate["adjudication"]
        self.copy_requested = candidate["copy_requested"]
        self.custom_id = candidate["custom_id"]
        self.dob = candidate["dob"]
        self.geo_ids = candidate["geo_ids"]
        self.middle_name = candidate["middle_name"]
        self.mother_maiden_name = candidate["mother_maiden_name"]
        self.object = candidate["object"]
        self.phone = candidate["phone"]
        self.previous_driver_license_number = candidate[
            "previous_driver_license_number"
        ]
        self.previous_driver_license_state = candidate[
            "previous_driver_license_state"
        ]
        self.report_ids = candidate["report_ids"]
        self.ssn = candidate["ssn"]
        self.uri = candidate["uri"]
        self.zipcode = candidate["zipcode"]

        return True

    def _create_via_api(self) -> dict[str, Any]:
        candidate_created = self.checkr_api.create_candidate(
            copy_requested=self.copy_requested,
            custom_id=self.custom_id,
            driver_license_number=self.driver_license_number,
            driver_license_state=self.driver_license_state,
            dob=self.dob,
            email=self.email,
            first_name=self.first_name,
            geo_ids=self.geo_ids,
            last_name=self.last_name,
            middle_name=self.middle_name,
            mother_maiden_name=self.mother_maiden_name,
            phone=self.phone,
            previous_driver_license_number=self.previous_driver_license_number,
            previous_driver_license_state=self.previous_driver_license_state,
            ssn=self.ssn,
            work_locations=self.work_locations,
            zipcode=self.zipcode,
        )

        return candidate_created
