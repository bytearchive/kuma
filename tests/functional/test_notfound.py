import pytest
import requests

from pages.notfound import NotFoundPage
from pages.base import assert_valid_url


# page headers
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_not_found_status(base_url, selenium):
    page = NotFoundPage(selenium, base_url).open()
    assert_valid_url(selenium.current_url, status_code=requests.codes.not_found)


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_expected_content(base_url, selenium):
    page = NotFoundPage(selenium, base_url).open()
    assert page.is_title_expected
    assert page.is_report_link_displayed
