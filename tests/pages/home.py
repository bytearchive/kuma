from selenium.webdriver.common.by import By

from pages.base import BasePage


class HomePage(BasePage):

    _masthead_locator = (By.CSS_SELECTOR, '.home-masthead')

    @property
    def is_masthead_displayed(self):
        return self.find_element(*self._masthead_locator).is_displayed()
