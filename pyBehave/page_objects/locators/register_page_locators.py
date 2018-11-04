'''
Module representing locators for registration page.
'''

from selenium.webdriver.common.by import By


class RegisterPageLocators(object):
    '''
    Class contining locators for objects within a page.
    All register screen locators should go here.

    :USER_NAME: registration username form locator (By.CSS_SELECTOR).

    :PASSWORD: registration pasword form locator (By.CSS_SELECTOR).

    :EMAIL: registration email form locator (By.CSS_SELECTOR).

    :SUBMIT_BUTTON: registration submit button locator (By.CSS_SELECTOR).

    :MUSIC_BUTTON: button activating the music popup (By.CSS_SELECTOR).

    :STOP_MUSIC_BUTTON: button that stops music (By.CSS_SELECTOR).

    :HIDE_MUSIC_POPUP: button that hides music popup (By.CSS_SELECTOR).

    :REGISTER_ERROR: alert that shows after unsuccessful registration (By.CSS_SELECTOR).

    '''

    USER_NAME = (By.CSS_SELECTOR, 'input[id="register_username"]')
    PASSWORD = (By.CSS_SELECTOR, 'input[id="register_password"]')
    EMAIL = (By.CSS_SELECTOR, 'input[id="register_email"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[id="register_confirm"]')

    # Music popup
    MUSIC_BUTTON = (By.CSS_SELECTOR, 'span[class*="glyphicon-music"]')
    STOP_MUSIC_BUTTON = (By.CSS_SELECTOR, 'div[class*="target"]')
    EXIT_FULLSCREEN_MUSIC = (By.CSS_SELECTOR, 'button[class="fullscreen"]')
    HIDE_MUSIC_POPUP = (By.CSS_SELECTOR, 'button[id="hide_rick"]')

    # delete after making home_page
    REGISTER = (By.CSS_SELECTOR, 'span[class*="glyphicon-user"]')
    # delete after making home_page
    LOGIN = (By.CSS_SELECTOR, 'span[class*="glyphicon-log-in"]')
    # delete after making home_page
    TOOGLE = (By.CSS_SELECTOR, 'button[class*="toggle"]')

    # Register error popup
    REGISTER_ERROR = (By.CSS_SELECTOR, 'div[class*="alert-danger"]')
