from behave import *

from page_objects.register_page import RegisterPage


@when("I click register button")
def open_register(context):
    if context.config.userdata['mobile'] != "no":
        RegisterPage(context.driver).open_mobile_navbar()
    RegisterPage(context.driver).open_register()


@when("I click login button")
def open_login(context):
    if context.config.userdata['mobile'] != "no":
        RegisterPage(context.driver).open_mobile_navbar()
    RegisterPage(context.driver).open_login()
