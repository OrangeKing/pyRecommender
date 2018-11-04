from behave import *

from page_objects.register_page import RegisterPage


@given("app is open")
def check_app_open(context):
    pass


@when("I fill sign up form with credentials of already registered user")
def fill_reg_form(context):
    RegisterPage(context.driver).fill_fields(
        context.username, context.password, context.email)


@when("I do not fill '{what}' input")
def fill_part_reg_form(context, what):
    if what == "username":
        RegisterPage(context.driver).fill_fields(
            " ", context.password, context.email)
    if what == "password":
        RegisterPage(context.driver).fill_fields(
            context.username, " ", context.email)
    if what == "email":
        RegisterPage(context.driver).fill_fields(
            context.username, context.password, " ")


@when("I fill sign up form with generated credentials")
def fill_gen_reg_form(context):
    RegisterPage(context.driver).fill_fields(
        context.timestamp_username, context.timestamp_password, context.timestamp_email)


@when("I stop the music form playing in the background")
def stop_music(context):
    if context.config.userdata['mobile'] != 'default' and context.config.userdata['mobile'] != 'no' and context.config.userdata['mobile'] != 'android':
        RegisterPage(context.driver).stop_mobile_music()
    else:
        RegisterPage(context.driver).stop_music()


@when("I press submit button on sign up form")
def submit_reg(context):
    RegisterPage(context.driver).press_submit()


@then("User with generated credentials should exist in application database")
def check_user_in_database(context):
    assert RegisterPage(context.driver).check_usr_in_db(
        context.timestamp_username)


@then("Registration should fail")
def check_user_not_in_database(context):
    assert RegisterPage(context.driver).check_not_register()
