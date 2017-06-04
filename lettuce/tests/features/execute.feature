Feature: View top used words for the selected date after selecting it
    In order to view top used words for the selected date after selecting it
    As a user
    I want to press the Execute button

    Scenario: Default date, like "Today"
        Given the date "Today"
        When I press Execute button
        Then I see words count section with ""
        And I see "Today" option selected

    Scenario: Specific date, like "2017-05-28"
        Given the date "2017-05-28"
        When I press Execute button
        Then I see words count section with "28, 28-mayo, 28-no, 26-alonso, 22-este, 22"
        And I see "Today" option selected

