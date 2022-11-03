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
        session: Session = Session(),
        retries: Retry = get_default_retries(),
    ) -> None:
        self.session = session
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.secret_api_key = secret_api_key
        self.api_url = api_url

    def create_candidate(
        self,
        first_name: str,
        last_name: str,
        email: str,
        driver_license_number: str,
        driver_license_state: str,
        work_locations: list[dict[str, str]],
        middle_name: Optional[str] = None,
        mother_maiden_name: Optional[str] = None,
        ssn: Optional[str] = None,
        dob: Optional[date] = None,
        zipcode: Optional[str] = None,
        uri: Optional[str] = None,
        phone: Optional[str] = None,
        geo_ids: Optional[list[str]] = None,
        previous_driver_license_number: Optional[str] = None,
        previous_driver_license_state: Optional[str] = None,
        copy_requested: Optional[bool] = None,
        custom_id: Optional[str] = None,
    ) -> str:
        candidate_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "driver_license_number": driver_license_number,
            "driver_license_state": driver_license_state,
            "work_locations": work_locations,
            "middle_name": middle_name,
            "mother_maiden_name": mother_maiden_name,
            "ssn": ssn,
            "dob": dob,
            "zipcode": zipcode,
            "uri": uri,
            "phone": phone,
            "geo_ids": geo_ids,
            "previous_driver_license_number": previous_driver_license_number,
            "previous_driver_license_state": previous_driver_license_state,
            "copy_requested": copy_requested,
            "custom_id": custom_id
        }

        candidate_json = json.dumps(candidate_data)
        response = requests.post(
            auth=HTTPBasicAuth(self.secret_api_key, None),
            url=f"{self.api_url}/candidates",
            data=candidate_json
        )

        candidate = response.json()
        return candidate

    def create_invitation(
        self,
        candidate_id: str,
        package: str,
        work_locations: list[dict[str, str]] = None,
        node: Optional[str] = None,
        tags: Optional[str] = None,
        communication_types=None,
    ) -> dict[str, Any]:
        invitation_data = {
            "package": package,
            "candidate_id": candidate_id,
            "work_locations": work_locations,
            "node": node,
            "tags": tags,
            "communication_types": communication_types
        }

        invitation_json = json.dumps(invitation_data)
        response = self.session.post(
            auth=HTTPBasicAuth(self.secret_api_key, None),
            url=f"{self.api_url}/invitations",
            data=invitation_json
        )

        invitation = response.json()
        return invitation

    def create_report(
        self,
        candidate_id: str,
        package: str,
        work_locations: list[dict[str, str]],
        node: Optional[str] = None
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
            data=report_json
        )

        report = response.json()
        return report
