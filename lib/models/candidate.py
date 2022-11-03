from dataclasses import dataclass
from typing import Optional

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
    middle_name: Optional[str] = None
    no_middle_name: Optional[bool] = None
    mother_maiden_name: Optional[str] = None
    ssn: Optional[str] = None
    dob: Optional[str] = None
    object: Optional[str] = None
    zipcode: Optional[str] = None
    uri: Optional[str] = None
    phone: Optional[str] = None
    geo_ids: Optional[list[str]] = None
    previous_driver_license_number: Optional[str] = None
    previous_driver_license_state: Optional[str] = None
    copy_requested: Optional[bool] = None
    custom_id: Optional[str] = None
    report_ids: Optional[list[str]] = None
    adjudication: Optional[str] = None

    def create(self, raise_on_failure: bool = True) -> bool:

        try:
            response = self.checkr_api.create_candidate(
                first_name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                driver_license_number=self.driver_license_number,
                driver_license_state=self.driver_license_state,
                work_locations=self.work_locations,
                middle_name=self.middle_name,
                mother_maiden_name=self.mother_maiden_name,
                phone=self.phone,
                zipcode=self.zipcode,
                dob=self.dob,
                ssn=self.ssn,
                previous_driver_license_number=self.previous_driver_license_number,
                previous_driver_license_state=self.previous_driver_license_state,
                copy_requested=self.copy_requested,
                custom_id=self.custom_id,
                geo_ids=self.geo_ids,
            )
        except HTTPError:
            if raise_on_failure:
                raise
            return False

        if "id" not in response:
            if raise_on_failure:
                raise CheckerAPIFailedCreation
            return False

        self.id = response["id"]
        self.middle_name = response["middle_name"]
        self.mother_maiden_name = response["mother_maiden_name"]
        self.ssn = response["ssn"]
        self.dob = response["dob"]
        self.object = response["object"]
        self.zipcode = response["zipcode"]
        self.uri = response["uri"]
        self.phone = response["phone"]
        self.geo_ids = response["geo_ids"]
        self.previous_driver_license_number = response[
            "previous_driver_license_number"
        ]
        self.previous_driver_license_state = response[
            "previous_driver_license_state"
        ]
        self.copy_requested = response["copy_requested"]
        self.custom_id = response["custom_id"]
        self.report_ids = response["report_ids"]
        self.adjudication = response["adjudication"]

        return True
