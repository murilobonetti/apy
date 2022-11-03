from dataclasses import dataclass
from typing import Optional

from requests import HTTPError

from lib.api.checkr_api import CheckrAPI
from lib.helpers.checkr_api_error import CheckerAPIFailedCreation


class WorkLocation:
    pass


@dataclass
class Invitation:
    checkr_api: CheckrAPI
    package: str
    candidate_id: str
    work_locations: list[dict[str, str]]

    node: Optional[str] = None
    tags: Optional[list[str]] = None
    communication_types: Optional[list[str]] = None
    uri: Optional[str] = None
    object: Optional[str] = None
    invitation_url: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    deleted_at: Optional[str] = None
    report_id: Optional[str] = None

    id: Optional[int] = None  # From API Creation Response

    def create(self, raise_on_failure: bool = True) -> bool:
        if self.communication_types is None:
            self.communication_types = ["email"]

        try:
            response = self.checkr_api.create_invitation(
                package=self.package,
                candidate_id=self.candidate_id,
                work_locations=self.work_locations,
                node=self.node,
                tags=self.tags,
                communication_types=self.communication_types
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
        self.uri = response["uri"]
        self.object = response["object"]
        self.invitation_url = response["invitation_url"]
        self.status = response["status"]
        self.created_at = response["created_at"]
        self.expires_at = response["expires_at"]
        self.deleted_at = response["deleted_at"]
        self.report_id = response["report_id"]

        return True
