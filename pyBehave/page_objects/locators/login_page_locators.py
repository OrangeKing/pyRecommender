'''
Module representing locators for login page.
'''

from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    '''
    Class contining locators for objects within a page.
    All register screen locators should go here.

    :MODAL_USERNAME: modal-login username form locator (By.CSS_SELECTOR).

    :MODAL_PASSWORD: modal-login pasword form locator (By.CSS_SELECTOR).

    :MODAL_SUBMIT: modal-login submit button locator (By.CSS_SELECTOR).

    :USERNAME_NAVBAR: locator that locates, place on the navbar that displays logged-in user username (By.CSS_SELECTOR).


    '''

    MODAL_USERNAME = (By.CSS_SELECTOR, 'input[id="modal_username"]')
    MODAL_PASSWORD = (By.CSS_SELECTOR, 'input[id="modal_password"]')
    MODAL_SUBMIT = (By.CSS_SELECTOR, 'button[id="login_modal_submit"]')

    USERNAME_NAVBAR = (By.CSS_SELECTOR, 'a[href*="/posts/?q="]')
