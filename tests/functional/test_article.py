import pytest

from pages.article import ArticlePage


# page title
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_title_expected(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.is_title_expected()


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_title_in_title(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.is_title_in_title()


# article
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_article_title_expected(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.is_article_title_expected


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_article_layout(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.is_article_displayed
    assert page.is_article_column_left_present
    assert page.is_article_column_content_present
    assert page.article_column_right_present
    assert page.is_article_columns_expected_layout


# page buttons
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_page_buttons_displayed(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.is_language_menu_displayed
    assert page.is_edit_button_displayed
    assert page.is_advanced_menu_displayed


# header tests
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_header_displayed(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.Header.is_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_header_menu_displayed(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.Header.is_menu_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_header_platform_submenu(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.header.is_platform_submenu_trigger_displayed
    assert not page.header.is_platform_submenu_displayed
    page.header.show_platform_submenu()
    assert page.header.is_platform_submenu_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_header_feedback_submenu(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.header.is_feedback_submenu_trigger_displayed
    assert not page.header.is_feedback_submenu_displayed
    page.header.show_feedback_submenu()
    assert page.header.is_feedback_submenu_displayed


# footer tests
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_footer_displayed(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.Footer.is_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_is_footer_links_displayed(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.Footer.is_privacy_displayed
    assert page.Footer.is_license_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_select_language(base_url, selenium):
    page = ArticlePage(selenium, base_url).open()
    assert page.Footer.is_select_language_displayed
    assert page.Footer.is_select_language_locale_match
