from lib.api.checkr_api import CheckrAPI
from lib.helpers.constants import STAGING_URL
from lib.helpers.secrets import SECRET_API_KEY
from lib.models.candidate import Candidate
from lib.models.invitation import Invitation


def test_candidate_creation_successful():
    candidate = Candidate(
        checkr_api=CheckrAPI(SECRET_API_KEY, STAGING_URL),
        driver_license_state="CA",
        driver_license_number="O2233344",
        email="murilo.bonetti@pickups.mobi",
        first_name="King",
        last_name="Burguer",
        work_locations=[{"country": "US", "state": "FL", "city": "Miami"}],
    )

    assert candidate.id is None
    creation_successful = candidate.create()
    assert creation_successful is True


def test_candidate_creation_failed():
    candidate = Candidate(
        checkr_api=CheckrAPI("secret not so secret", STAGING_URL),
        driver_license_state="CA",
        driver_license_number="O2233344",
        email="murilo.bonetti@pickups.mobi",
        first_name="King",
        last_name="Burguer",
        work_locations=[{"country": "US", "state": "FL", "city": "Miami"}],
    )

    assert candidate.id is None
    creation_failed = candidate.create(raise_on_failure=False)
    assert creation_failed is False


def test_candidate_creation_and_invitation_successful():
    candidate = Candidate(
        checkr_api=CheckrAPI(SECRET_API_KEY, STAGING_URL),
        driver_license_state="CA",
        driver_license_number="O2233344",
        email="murilo.bonetti@pickups.mobi",
        first_name="King",
        last_name="Burguer",
        work_locations=[{"country": "US", "state": "FL", "city": "Miami"}],
    )

    assert candidate.id is None
    candidate_creation_successful = candidate.create()
    assert candidate_creation_successful is True

    invitation = Invitation(
        checkr_api=CheckrAPI(SECRET_API_KEY, STAGING_URL),
        candidate_id=candidate.id,
        package="basic_crim",
        work_locations=candidate.work_locations,
    )

    assert invitation.id is None
    invitation_created = invitation.create()
    assert invitation_created is True
