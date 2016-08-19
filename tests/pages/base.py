import re
import requests
from urlparse import urlparse, parse_qs
from braceexpand import braceexpand

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from pypom import Page, Region


class BasePage(Page):

    URL_TEMPLATE = '/{locale}'

    def __init__(self, selenium, base_url, locale='en-US', **url_kwargs):
        super(BasePage, self).__init__(selenium, base_url, locale=locale, **url_kwargs)

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: el.get_attribute('data-ffo-opensanslight'))
        return self

    @property
    def header(self):
        return self.Header(self)

    @property
    def footer(self):
        return self.Footer(self)

    """
    class NavAccess(Region):
        _root_locator(By.ID, 'nav-access')
        _skip_locator(By.ID, 'skip-main')

        # displays on focus

        # skiplink a.href matches ID on page
    """

    class Header(Region):
        report_content_form_url = 'https://bugzilla.mozilla.org/form.doc'
        report_bug_form_url = 'https://bugzilla.mozilla.org/form.mdn'
        # locators
        _root_locator = (By.ID, 'main-header')
        _menu_locator = (By.ID, 'nav-main-menu')
        _platform_submenu_trigger_locator = (By.XPATH,
                                             'id(\'nav-platform-submenu\')/..')
        _platform_submenu_locator = (By.ID, 'nav-platform-submenu')
        _platform_submenu_item_locator = (By.CSS_SELECTOR,
                                          '#nav-platform-submenu a')
        _feedback_link_locator = (By.XPATH, 'id(\'nav-contact-submenu\')/../a')
        _feedback_submenu_trigger_locator = (By.XPATH,
                                             'id(\'nav-contact-submenu\')/..')
        _feedback_submenu_locator = (By.ID, 'nav-contact-submenu')
        _report_content_locator = (By.CSS_SELECTOR,
                                   'a[href^="' + report_content_form_url + '"]')
        _report_bug_locator = (By.CSS_SELECTOR,
                               'a[href^="' + report_bug_form_url + '"]')

        # is displayed?
        @property
        def is_displayed(self):
            return self.root.is_displayed()

        # nav is displayed?
        @property
        def is_menu_displayed(self):
            return self.find_element(*self._menu_locator).is_displayed()

        # platform submenu
        @property
        def is_platform_submenu_trigger_displayed(self):
            submenu_trigger = self.find_element(*self._platform_submenu_trigger_locator)
            return submenu_trigger.is_displayed()

        @property
        def is_platform_submenu_displayed(self):
            submenu = self.find_element(*self._platform_submenu_locator)
            return submenu.is_displayed()

        def show_platform_submenu(self):
            submenu_trigger = self.find_element(*self._platform_submenu_trigger_locator)
            submenu = self.find_element(*self._platform_submenu_locator)
            hover = ActionChains(self.selenium).move_to_element(submenu_trigger)
            hover.perform()
            self.wait.until(lambda s: submenu.is_displayed())

        # feedback submenu
        @property
        def is_feedback_submenu_trigger_displayed(self):
            submenu_trigger = self.find_element(*self._feedback_submenu_trigger_locator)
            return submenu_trigger.is_displayed()

        @property
        def is_feedback_submenu_displayed(self):
            submenu = self.find_element(*self._feedback_submenu_locator)
            return submenu.is_displayed()

        @property
        def is_report_content_link_displayed(self):
            report_content_link = self.find_element(*self._report_content_locator)
            return report_content_link.is_displayed()

        @property
        def is_report_bug_link_displayed(self):
            report_bug_link = self.find_element(*self._report_bug_locator)
            return report_bug_link.is_displayed()

        def show_feedback_submenu(self):
            submenu_trigger = self.find_element(*self._feedback_submenu_trigger_locator)
            submenu = self.find_element(*self._feedback_submenu_locator)
            hover = ActionChains(self.selenium).move_to_element(submenu_trigger)
            hover.perform()
            self.wait.until(lambda s: submenu.is_displayed())

        def open_feedback(self):
            self.find_element(*self._feedback_link_locator).click()
            from pages.feedback import FeedbackPage
            return FeedbackPage(self.selenium, self.page.base_url).wait_for_page_to_load()

        def open_report_content(self):
            self.find_element(*self._report_content_locator).click()
            # TODO - what to return???
            # return FeedbackPage(self.selenium, self.page.base_url).wait_for_page_to_load()

        def is_report_content_url_expected(self, selenium, article_url):
            current_url = selenium.current_url
            report_url = self.report_content_form_url
            # current_url_simplified = re.sub(r'[^a-zA-Z]', '', current_url)
            # article_url_simplified = re.sub(r'[^a-zA-Z]', '', article_url)
            # compare
            url_matches = report_url in current_url
            # url_contains_article = article_url_simplified in current_url_simplified
            return url_matches

        def open_report_bug(self):
            self.find_element(*self._report_bug_locator).click()

        def is_report_bug_url_expected(self, selenium):
            return self.report_bug_form_url in selenium.current_url


    class Footer(Region):
        privacy_url = 'https://www.mozilla.org/privacy/websites/'
        copyright_id = 'Copyrights_and_licenses'
        # locators
        _root_locator = (By.ID, 'main-footer')
        _language_locator = (By.ID, 'language')
        _privacy_locator = (By.CSS_SELECTOR, 'a[href^="' + privacy_url + '"]')
        _license_locator = (By.CSS_SELECTOR,
                            'a[href="/docs/MDN/About#' + copyright_id + '"]')

        # is displayed?
        @property
        def is_displayed(self):
            return self.root.is_displayed()

        # language select is displayed
        @property
        def is_select_language_displayed(self):
            return self.find_element(*self._language_locator).is_displayed()

        # check lanuage selected in drop down matches locale
        @property
        def is_select_language_locale_match(self, locale):
            # get language selected
            language_select = self.find_element(*self._language_locator)
            selected_option = language_select.find_element('option[selected]')
            selected_language = selected_option.get_attribute('value')
            return (selected_language == locale)

        # privacy link is displayed
        @property
        def is_privacy_displayed(self):
            return self.find_element(*self._privacy_locator).is_displayed()

        # license link is displayed
        @property
        def is_license_displayed(self):
            return self.find_element(*self._license_locator).is_displayed()


def get_abs_url(url, base_url):
    try:
        if url.pattern.startswith('/'):
            # url is a compiled regular expression pattern
            return re.compile(''.join([re.escape(base_url), url.pattern]))
    except AttributeError:
        if url.startswith('/'):
            # urljoin messes with query strings too much
            return ''.join([base_url, url])
    return url


def url_test(url, location=None, status_code=requests.codes.moved_permanently,
             req_headers=None, req_kwargs=None, resp_headers=None, query=None,
             follow_redirects=False, final_status_code=requests.codes.ok):
    """
    Function for producing a config dict for the redirect test.

    You can use simple bash style brace expansion in the `url` and `location`
    values. If you need the `location` to change with the `url` changes you must
    use the same number of expansions or the `location` will be treated as non-expandable.

    If you use brace expansion this function will return a list of dicts instead of a dict.
    You must use the `flatten` function provided to prepare your test fixture if you do this.

    If you combine brace expansion with a compiled regular expression pattern you must
    escape any backslashes as this is the escape character for brace expansion.

    example:

        url_test('/about/drivers{/,.html}', 'https://wiki.mozilla.org/Firefox/Drivers'),
        url_test('/projects/index.{de,fr,hr,sq}.html', '/{de,fr,hr,sq}/firefox/products/'),
        url_test('/firefox/notes/', re.compile(r'\/firefox\/[\d\.]+\/releasenotes\/'),
        url_test('/firefox/android/{,beta/}notes/', re.compile(r'\\/firefox\\/android\\/[\\d\\.]+{,beta}\\/releasenotes\\/'

    :param url: The URL in question (absolute or relative).
    :param location: If a redirect, either the expected value or a compiled regular expression to match the "Location" header.
    :param status_code: Expected status code from the request.
    :param req_headers: Extra headers to send with the request.
    :param req_kwargs: Extra arguments to pass to requests.get()
    :param resp_headers: Dict of headers expected in the response.
    :param query: Dict of expected query params in `location` URL.
    :param follow_redirects: Boolean indicating whether redirects should be followed.
    :param final_status_code: Expected status code after following any redirects.
    :return: dict or list of dicts
    """
    test_data = {
        'url': url,
        'location': location,
        'status_code': status_code,
        'req_headers': req_headers,
        'req_kwargs': req_kwargs,
        'resp_headers': resp_headers,
        'query': query,
        'follow_redirects': follow_redirects,
        'final_status_code': final_status_code,
    }
    expanded_urls = list(braceexpand(url))
    num_urls = len(expanded_urls)
    if num_urls == 1:
        return test_data

    try:
        # location is a compiled regular expression pattern
        location_pattern = location.pattern
        test_data['location'] = location_pattern
    except AttributeError:
        location_pattern = None

    new_urls = []
    if location:
        expanded_locations = list(braceexpand(test_data['location']))
        num_locations = len(expanded_locations)

    for i, url in enumerate(expanded_urls):
        data = test_data.copy()
        data['url'] = url
        if location and num_urls == num_locations:
            if location_pattern is not None:
                # recompile the pattern after expansion
                data['location'] = re.compile(expanded_locations[i])
            else:
                data['location'] = expanded_locations[i]
        new_urls.append(data)

    return new_urls


def assert_valid_url(url, location=None, status_code=requests.codes.moved_permanently,
                     req_headers=None, req_kwargs=None, resp_headers=None,
                     query=None, base_url=None, follow_redirects=False,
                     final_status_code=requests.codes.ok):
    """
    Define a test of a URL's response.
    :param url: The URL in question (absolute or relative).
    :param location: If a redirect, either the expected value or a compiled regular expression to match the "Location" header.
    :param status_code: Expected status code from the request.
    :param req_headers: Extra headers to send with the request.
    :param req_kwargs: Extra arguments to pass to requests.get()
    :param resp_headers: Dict of headers expected in the response.
    :param base_url: Base URL for the site to test.
    :param query: Dict of expected query params in `location` URL.
    :param follow_redirects: Boolean indicating whether redirects should be followed.
    :param final_status_code: Expected status code after following any redirects.
    """
    kwargs = {'allow_redirects': follow_redirects}
    if req_headers:
        kwargs['headers'] = req_headers
    if req_kwargs:
        kwargs.update(req_kwargs)

    abs_url = get_abs_url(url, base_url)
    resp = requests.get(abs_url, **kwargs)
    # so that the value will appear in locals in test output
    resp_location = resp.headers.get('location')
    if follow_redirects:
        assert resp.status_code == final_status_code
    else:
        assert resp.status_code == status_code
    if location and not follow_redirects:
        if query:
            # all query values must be lists
            for k, v in query.items():
                if isinstance(v, basestring):
                    query[k] = [v]
            # parse the QS from resp location header and compare to query arg
            # since order doesn't matter.
            resp_parsed = urlparse(resp_location)
            assert query == parse_qs(resp_parsed.query)
            # strip off query for further comparison
            resp_location = resp_location.split('?')[0]

        abs_location = get_abs_url(location, base_url)
        try:
            # location is a compiled regular expression pattern
            assert abs_location.match(resp_location) is not None
        except AttributeError:
            assert abs_location == resp_location

    if resp_headers and not follow_redirects:
        for name, value in resp_headers.items():
            print name, value
            assert name in resp.headers
            assert resp.headers[name].lower() == value.lower()


def flatten(urls_list):
    """Take a list of dicts which may itself contain some lists of dicts, and
       return a generator that will return just the dicts in sequence.

       Example:

       list(flatten([{'dude': 'jeff'}, [{'walter': 'walter'}, {'donny': 'dead'}]]))
       > [{'dude': 'jeff'}, {'walter': 'walter'}, {'donny': 'dead'}]
    """
    for url in urls_list:
        if isinstance(url, dict):
            yield url
        else:
            for sub_url in url:
                yield sub_url
