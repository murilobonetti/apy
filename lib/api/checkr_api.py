import json
from datetime import date
from typing import Any, Optional

import requests
from requests import Session
from requests.adapters import HTTPAdapter, Retry
from requests.auth import HTTPBasicAuth

from lib.helpers.utils import get_default_retries


class CheckrAPI:
    def __init__(
        self,
        secret_api_key: str,
        api_url: str,
        session: Optional[Session] = None,
        retries: Optional[Retry] = None,
    ) -> None:
        self.session = session or Session()
        self.retries = session or get_default_retries()
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.secret_api_key = secret_api_key
        self.api_url = api_url

    def create_candidate(
        self,
        driver_license_number: str,
        driver_license_state: str,
        email: str,
        first_name: str,
        last_name: str,
        work_locations: list[dict[str, str]],
        copy_requested: Optional[bool] = None,
        custom_id: Optional[str] = None,
        dob: Optional[date] = None,
        geo_ids: Optional[list[str]] = None,
        middle_name: Optional[str] = None,
        phone: Optional[str] = None,
        previous_driver_license_number: Optional[str] = None,
        previous_driver_license_state: Optional[str] = None,
        mother_maiden_name: Optional[str] = None,
        ssn: Optional[str] = None,
        uri: Optional[str] = None,
        zipcode: Optional[str] = None,
    ) -> dict[str, Any]:
        candidate_data = {
            "copy_requested": copy_requested,
            "custom_id": custom_id,
            "driver_license_number": driver_license_number,
            "driver_license_state": driver_license_state,
            "dob": dob,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "geo_ids": geo_ids,
            "middle_name": middle_name,
            "mother_maiden_name": mother_maiden_name,
            "phone": phone,
            "previous_driver_license_number": previous_driver_license_number,
            "previous_driver_license_state": previous_driver_license_state,
            "ssn": ssn,
            "uri": uri,
            "work_locations": work_locations,
            "zipcode": zipcode,
        }

        candidate_json = json.dumps(candidate_data)
        response = requests.post(
            auth=HTTPBasicAuth(self.secret_api_key, None),
            url=f"{self.api_url}/candidates",
            data=candidate_json,
        )

        candidate = response.json()
        return candidate

    def create_invitation(
        self,
        candidate_id: str,
        package: str,
        communication_types: Optional[list[str]] = None,
        node: Optional[str] = None,
        tags: Optional[str] = None,
        work_locations: list[dict[str, str]] = None,
    ) -> dict[str, Any]:
        invitation_data = {
            "candidate_id": candidate_id,
            "communication_types": communication_types,
            "node": node,
            "package": package,
            "tags": tags,
            "work_locations": work_locations,
        }

        invitation_json = json.dumps(invitation_data)
        response = self.session.post(
            auth=HTTPBasicAuth(self.secret_api_key, None),
            url=f"{self.api_url}/invitations",
            data=invitation_json,
        )

        invitation = response.json()
        return invitation

    def create_report(
        self,
        candidate_id: str,
        package: str,
        work_locations: list[dict[str, str]],
        node: Optional[str] = None,
    ) -> dict[str, Any]:
        report_data = {
            "candidate_id": candidate_id,
            "package": package,
            "node": node,
            "work_locations": work_locations,
        }

        report_json = json.dumps(report_data)
        response = self.session.post(
            auth=HTTPBasicAuth(self.secret_api_key, None),
            url=f"{self.api_url}/reports",
            data=report_json,
        )

        report = response.json()
        return report
