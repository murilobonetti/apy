from dataclasses import dataclass
from typing import Optional

from requests import HTTPError

from lib.api.checkr_api import CheckrAPI
from lib.helpers.checkr_api_error import CheckerAPIFailedCreation


@dataclass
class Report:
    checkr_api = CheckrAPI
    candidate_id: str
    package: str
    node: str
    work_locations: list[dict[str, str]]

    id: Optional[str] = None
    self_disclosures: Optional[list[dict[str, str]]] = None
    tags: Optional[list[str]] = None
    object: Optional[str] = None
    uri: Optional[str] = None
    status: Optional[str] = None
    result: Optional[str] = None
    includes_canceled: Optional[bool] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    revised_at: Optional[str] = None
    upgraded_at: Optional[str] = None
    turnaround_time: Optional[int] = None
    adjudication: Optional[str] = None
    assessment: Optional[str] = None
    source: Optional[str] = None
    segment_stamps: Optional[list[str]] = None
    estimated_completion_time: Optional[str] = None
    candidate_story_ids: Optional[list[str]] = None
    drug_screening: Optional[dict[str, any]] = None
    ssn_trace_id: Optional[str] = None
    arrest_search_id: Optional[str] = None
    federal_criminal_search_id: Optional[str] = None
    federal_district_criminal_search_id: Optional[str] = None
    federal_civil_search_id: Optional[str] = None
    federal_district_civil_search_id: Optional[str] = None
    global_watchlist_search_id: Optional[str] = None
    sex_offender_search_id: Optional[str] = None
    national_criminal_search_id: Optional[str] = None
    county_criminal_search_ids: Optional[list[str]] = None
    personal_reference_verification_ids: Optional[list[str]] = None
    professional_reference_verification_ids: Optional[list[str]] = None
    motor_vehicle_report_id: Optional[str] = None
    professional_license_verification_ids: Optional[list[str]] = None
    state_criminal_searches: Optional[list[str]] = None
    international_criminal_searches_v2_ids: Optional[list[str]] = None
    international_adverse_media_search_ids: Optional[list[str]] = None
    international_global_watchlist_search_id: Optional[str] = None
    international_education_verification_id: Optional[str] = None
    international_employment_verification_id: Optional[str] = None
    international_identity_document_validation_id: Optional[str] = None
    documents_ids: Optional[list[str]] = None
    geo_ids: Optional[list[str]] = None
    program_id: Optional[str] = None

    def create(self, raise_on_failure: bool = True) -> bool:

        try:
            response = self.checkr_api.create_report(
                package=self.package,
                candidate_id=self.candidate_id,
                node=self.node,
                work_locations=self.work_locations
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

        return True
