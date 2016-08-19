import pytest

from pages.article import ArticlePage
from pages.feedback import FeedbackPage
from pages.base import assert_valid_url


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_location(base_url, selenium):
    article_page = ArticlePage(selenium, base_url).open()
    page = article_page.header.open_feedback()
    assert page.seed_url in selenium.current_url
    assert page.is_title_expected()
    assert page.is_title_in_title()


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_feedback_layout(base_url, selenium):
    page = FeedbackPage(selenium, base_url).open()
    assert page.is_article_displayed
    assert page.is_article_column_left_present
    assert page.is_article_column_content_present
    assert page.article_column_right_present
    assert page.is_article_columns_expected_layout


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_page_links(base_url, selenium):
    page = FeedbackPage(selenium, base_url).open()
    # get all page links
    article_links = page.article_link_list
    for link in article_links:
        this_link = link.get_attribute('href')
        # exclude IRC, we can't handle that protocol
        if not this_link.startswith('irc'):
            assert_valid_url(this_link, follow_redirects=True)
