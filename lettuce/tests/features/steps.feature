Feature: Select a publication date from the list
    In order to view top used words for the selected date
    As a user
    I want to select a publication date

    Scenario: Date "Today"
        Given the select box in the default state
        When I select "Today" option
        Then I see "Today" option selected
	And I see words count section in blank

    Scenario: Date "2017-05-28"
        Given the select box in the default state
        When I select "2017-05-28" option
        Then I see "2017-05-28" option selected
	And I see words count section in blank

