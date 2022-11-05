from dataclasses import dataclass
from typing import Optional, Any

from requests import HTTPError

from lib.api.checkr_api import CheckrAPI
from lib.helpers.checkr_api_error import CheckerAPIFailedCreation


@dataclass
class Invitation:
    checkr_api: CheckrAPI
    package: str
    candidate_id: str
    communication_types = ["email"]
    work_locations: list[dict[str, str]]
    id: Optional[int] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    expires_at: Optional[str] = None
    invitation_url: Optional[str] = None
    node: Optional[str] = None
    object: Optional[str] = None
    report_id: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[list[str]] = None
    uri: Optional[str] = None

    def create(self, raise_on_failure: bool = True) -> bool:
        try:
            invitation = self._create_via_api()
        except HTTPError:
            if raise_on_failure:
                raise
            return False

        if "id" not in invitation:
            if raise_on_failure:
                raise CheckerAPIFailedCreation
            return False

        self.id = invitation["id"]
        self.created_at = invitation["created_at"]
        self.deleted_at = invitation["deleted_at"]
        self.expires_at = invitation["expires_at"]
        self.invitation_url = invitation["invitation_url"]
        self.object = invitation["object"]
        self.report_id = invitation["report_id"]
        self.status = invitation["status"]
        self.uri = invitation["uri"]

        return True

    def _create_via_api(self) -> dict[str, Any]:
        invitation_created = self.checkr_api.create_invitation(
            candidate_id=self.candidate_id,
            communication_types=self.communication_types,
            node=self.node,
            package=self.package,
            tags=self.tags,
            work_locations=self.work_locations,
        )

        return invitation_created
