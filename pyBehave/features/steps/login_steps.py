from behave import *

from page_objects.login_page import LoginPage
from page_objects.register_page import RegisterPage


@when("I put valid credentials from configuration file on login form")
def fill_login_modal(context):
    LoginPage(context.driver).fill_fields(context.username, context.password)


@when("I press submit button on login form")
def submit_modal_login(context):
    LoginPage(context.driver).press_submit()


@then("I should be logged in as a user provided in config")
def check_login_navbar(context):
    if context.config.userdata['mobile'] != 'no':
        RegisterPage(context.driver).open_mobile_navbar()
    assert LoginPage(context.driver).check_login(context.username)
