@logged_user_scenarios
@login
Feature: User logging in
As a registered User
I should be able to log in to my account

    Scenario: [SUNNY] Logging with registered user credentials
     Given app is open
     When I click login button
     And I put valid credentials from configuration file on login form
     And I press submit button on login form
     Then I should be logged in as a user provided in config

    