from behave import *

from page_objects.register_page import RegisterPage


@when("I fill sign up form with generated credentials")
def fill_reg_form(context):
    RegisterPage(context.driver).fill_fields(
        context.timestamp_username, context.timestamp_password, context.timestamp_email)


@when("I stop the music form playing in the background")
def stop_music(context):
    RegisterPage(context.driver).stop_music()


@then("I press submit button on sign up form")
def submit_reg(context):
    RegisterPage(context.driver).press_submit()
