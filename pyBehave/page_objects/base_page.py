'''
Module representing abstract Base page for the application.
This page contains all parameters and methods called from all children-pages.
'''


class BasePage(object):
    '''
    Base class to initialize the base page that will be called from all pages.
    Provides all methods and parameters for further inheritance.

    '''

    def __init__(self, driver):
        self.driver = driver

    def go_back(self):
        '''
        Used to peform "back" function on the back.
        Returns to the previous view in app.
        '''

        self.driver.back()
