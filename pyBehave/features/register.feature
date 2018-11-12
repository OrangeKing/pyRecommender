@register

Feature: New user registration
As a User
I should be able to create new account

    @generated_user
   Scenario: [SUNNY] Create a new user with unique name and valid credentials
    Given app is open
    When I click register button
    And I fill sign up form with generated credentials
    And I press submit button on sign up form
    Then User with generated credentials should exist in application database

    @rainy_scenarios
  Scenario: [RAINY] Logging with previously registered user's credentials
    Given app is open
    When I click register button
    And I fill sign up form with credentials of already registered user
    And I press submit button on sign up form
    Then Registration should fail
    
    @rainy_scenarios
   Scenario: [RAINY] Create a new user with empty login
    Given app is open
    When I click register button
    And I do not fill 'username' input 
    And I press submit button on sign up form
    Then Registration should fail

    @rainy_scenarios
   Scenario: [RAINY] Create a new user with empty password
    Given app is open
    When I click register button
    And I do not fill 'password' input 
    And I press submit button on sign up form
    Then Registration should fail

    @rainy_scenarios
   Scenario: [RAINY] Create a new user with with empty email
    Given app is open
    When I click register button
    And I do not fill 'email' input 
    And I press submit button on sign up form
    Then Registration should fail