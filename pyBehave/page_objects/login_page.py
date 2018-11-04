'''
Module representing login page.
All user input is validated on the app-side.
'''

from page_objects.locators.login_page_locators import LoginPageLocators
from page_objects.base_page import BasePage
from page_objects.elements.elements import BasePageElement


class LoginPage(BasePage):
    '''
    Class contining methods for actions within login page.
    All user signing up methods should go here.
    '''

    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)

    def fill_fields(self, username, password):
        '''
        Fills registration forms with given user credentials.

        :param username: string value of registered user username to be put into
                         login form.

        :param password: string value of registered user password to be put into
                         login form.

        :param email: string value of registered user password to be put into
                         login form.
        '''

        self.driver.switch_to_active_element()
        if username != " ":
            BasePageElement(self.driver).input_text(
                LoginPageLocators.MODAL_USERNAME, username)
        if password != " ":
            BasePageElement(self.driver).input_text(
                LoginPageLocators.MODAL_PASSWORD, password)

    def press_submit(self):
        '''
        Clicks at the "submit" button to confirm login process with given
        credentials.
        '''
        self.driver.switch_to_default_content()

        BasePageElement(self.driver).click_element_and_wait(
            LoginPageLocators.MODAL_SUBMIT)

    def check_login(self, username):
        '''
        Checks if username name is being displayed on navbar.
        '''
        current_username = BasePageElement(self.driver).get_element(
            LoginPageLocators.USERNAME_NAVBAR)
        if current_username.text == username:
            return True
