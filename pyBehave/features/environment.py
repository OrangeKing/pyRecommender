'''
BDD Testing setup.
'''

import json
import os
from time import strftime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


SCRIPT_DIR = os.path.dirname(__file__)
CONFIGURATION_PATH = os.path.join(SCRIPT_DIR, "../configuration/conf.json")


def before_all(context):

    if context.config.userdata['mobile'] == "iphone":
        mobile_emulation = {"deviceName": "iPhone 6"}
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "mobileEmulation", mobile_emulation)
        context.driver = webdriver.Chrome(chrome_options=chrome_options)
    elif context.config.userdata['mobile'] == "default":
        context.driver = webdriver.PhantomJS()
        context.driver.set_window_size(360, 640)
    elif context.config.userdata['mobile'] == "no":
        context.driver = webdriver.PhantomJS()
        context.driver.maximize_window()

    context.driver.get("http://localhost:8000")

    # Read json file
    with open(CONFIGURATION_PATH) as json_file:
        configuration_json = json.load(json_file)

    context.username = str(configuration_json.get("test_username"))
    context.password = str(configuration_json.get("test_password"))
    context.email = str(configuration_json.get("test_email"))

    context.creation_time = strftime("%d%m%y%H%M%S")

    # Credentials generated for creation of new, unique users
    context.timestamp_username = "User_" + context.creation_time
    context.timestamp_password = "Password_" + context.creation_time
    context.timestamp_email = context.creation_time + "@mail.com"
    context.timestamp_messsage = "I have sent this message on" + context.creation_time


def after_all(context):
    context.driver.quit()
    context.driver = None
