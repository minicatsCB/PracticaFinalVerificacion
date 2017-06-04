from lettuce import step
from lettuce import world
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


@step('the select box in the default state')
def have_the_select_box_in_the_default_state(step):
	world.browser.get("http://127.0.0.1:5000")
	# Make dropdown list visible in order to select one of its option
	world.browser.execute_script("document.getElementById('pub-date-select').setAttribute('style', 'display:block')")
	select = Select(world.browser.find_element_by_id("pub-date-select"))
	selected_option = select.first_selected_option
    	assert True, selected_option.get_attribute('value') == "today"
	

@step('I select "([^"]*)" option')
def select_the_option(step, expected):
	select = Select(world.browser.find_element_by_id('pub-date-select'))
	select.select_by_value('2017-05-28')


@step('I see "([^"]*)" option selected')
def see_option_selected(step, expected):
	select = Select(world.browser.find_element_by_id("pub-date-select"))
	selected_option = select.first_selected_option
    	assert True, selected_option.tget_attribute('value') == expected.lower()


@step('I see words count section in blank')
def see_words_count_sectoin_in_blank(step):
	try:
        	world.browser.find_element_by_name("result-id")
   	except NoSuchElementException:
        	return False
    	return True

