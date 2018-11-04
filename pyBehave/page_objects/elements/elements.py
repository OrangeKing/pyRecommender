'''
Element class. It contains methods that perform actions on elements.
'''

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class BasePageElement(object):
    '''
    Base page class that is initialized on every page object class.
    '''

    MAX_DELAY = 10

    def __init__(self, driver):
        self.driver = driver

    def get_element(self, locator):
        '''
        Used to find element by locator object.

        :param locator: locator object, e.g. LOGIN_FORM = (By.ID, "username").

        :return: WebDriver element or None.
        '''

        return WebDriverWait(self.driver, self.MAX_DELAY).until(
            EC.visibility_of_element_located(locator))

    def get_elements(self, locator):
        '''
        Used to find many elements by locator object.

        :param locator: locator object, e.g. LOGIN_FORM = (By.ID, "username").

        :return: List of element or empty list.
        '''

        return WebDriverWait(self.driver, self.MAX_DELAY).until(
            EC.visibility_of_any_elements_located(locator))

    def get_unstable_element(self, locator):
        '''
        Used to find element by locator object, when element may disappear
        and appear in various intervals

        :param locator: locator object, e.g. LOGIN_FORM = (By.ID, "username").

        :return: WebDriver element or None.
        '''

        wait = WebDriverWait(self.driver, 10, poll_frequency=1,
                             ignored_exceptions=NoSuchElementException)
        element = wait.until(EC.visibility_of_element_located(locator))
        return element

    def click_element_and_wait(self, locator):
        '''
        Used to click element by locator object and wait afterwards.

        :param element: WebDriver element.
        '''

        self.get_element(locator).click()
        self.driver.implicitly_wait(2)

    def click_element(self, locator):
        '''
        Used to click element by locator object.

        :param locator: locator object, e.g. LOGIN_FORM = (By.ID, "username").
        '''

        self.get_element(locator).click()

    def input_text(self, locator, text):
        '''
        Used to send keys to the element by locator.

        :param locator: locator object, e.g. LOGIN_FORM = (By.ID, "username").

        :param text: text string to be sent.
        '''
        self.get_element(locator).send_keys(text)
