'''
Module representing registration page.
All user input is validated on the app-side.
'''

from page_objects.locators.register_page_locators import RegisterPageLocators
from page_objects.base_page import BasePage
from page_objects.elements.elements import BasePageElement

import psycopg2
from time import sleep


class RegisterPage(BasePage):
    '''
    Class contining methods for actions within register page.
    All user signing up methods should go here.
    '''

    def __init__(self, driver):
        super(RegisterPage, self).__init__(driver)

    def fill_fields(self, username, password, email):
        '''
        Fills registration forms with given user credentials.

        :param username: string value of registered user username to be put into
                         login form.

        :param password: string value of registered user password to be put into
                         login form.

        :param email: string value of registered user password to be put into
                         login form.
        '''

        if username != " ":
            BasePageElement(self.driver).input_text(
                RegisterPageLocators.USER_NAME, username)
        if password != " ":
            BasePageElement(self.driver).input_text(
                RegisterPageLocators.PASSWORD, password)
        if email != " ":
            BasePageElement(self.driver).input_text(
                RegisterPageLocators.EMAIL, email)

    def press_submit(self):
        '''
        Clicks at the "submit" button to confirm register process with given
        credentials and sign up.
        '''
        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.SUBMIT_BUTTON)

    def stop_music(self):
        '''
        Stops the music video.
        '''

        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.MUSIC_BUTTON)

        frame = self.driver.find_element_by_css_selector("iframe[src]")
        self.driver.switch_to_frame(frame)

        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.STOP_MUSIC_BUTTON)

        self.driver.switch_to_default_content()

        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.HIDE_MUSIC_POPUP)

    def stop_mobile_music(self):
        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.MUSIC_BUTTON)

        frame = self.driver.find_element_by_css_selector("iframe[src]")
        self.driver.switch_to_frame(frame)
        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.STOP_MUSIC_BUTTON)

        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.EXIT_FULLSCREEN_MUSIC)
        self.driver.switch_to_default_content()

    # delete after making home_page
    def open_register(self):
        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.REGISTER)

    def open_mobile_navbar(self):
        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.TOOGLE)

    # delete after making home_page
    def open_login(self):
        BasePageElement(self.driver).click_element_and_wait(
            RegisterPageLocators.LOGIN)

    def check_not_register(self):
        if BasePageElement(self.driver).get_element(RegisterPageLocators.REGISTER_ERROR):
            return True

    def check_usr_in_db(self, username):
        sleep(2)
        '''
        Verify whether user was properly registered by looking up user database.

        :param username: string object used for assertion with list of registered
                         users.

        :return: boolean value.
        '''

        try:
            conn = psycopg2.connect(
                "dbname='django_maps' user='django_admin' host='localhost' password='password'")
        except:
            print("DB error")

        cur = conn.cursor()
        cur.execute("""SELECT * FROM auth_user """)
        rows = cur.fetchall()
        for row in rows:
            if username in row:
                return True
