import time
from selenium.webdriver.common.keys import Keys
from lettuce import step
from lettuce import world
from datetime import datetime
from lettuce_webdriver.util import assert_true
from selenium.webdriver.support.color import Color
from lettuce_webdriver.util import assert_false
from lettuce_webdriver.util import AssertContextManager
from lettuce_webdriver.util import find_button
from lettuce_webdriver.util import find_field
from lettuce_webdriver.util import find_option
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

@step('the date "([^"]*)"')
def have_the_date(step, expected):
	world.browser.get("http://127.0.0.1:5000")
	# Make dropdown list visible in order to select one of its option
	world.browser.execute_script("document.getElementById('pub-date-select').setAttribute('style', 'display:block')");
	select = Select(world.browser.find_element_by_id('pub-date-select'))
	select.select_by_value(expected.lower())
	selected_option = select.first_selected_option
	assert True, selected_option.get_attribute('value') == expected.lower()

@step('I press Execute button')
def press_execute_button(step):
	execute_button = world.browser.find_element_by_id("btnExecute")
	execute_button.click()
	assert True, execute_button.get_attribute('value') == True

@step('I see words count section with "([^"]*)"')
def see_words_count_section_with(step, expected):
	WebDriverWait(world.browser, 10)
	elements = world.browser.find_elements(By.NAME, 'result-id')
	current_elements_list = []
	for el in elements:
		current_elements_list.append(el.text)
	expected_elements_list = expected.split("-")
	assert True, expected_elements_list == current_elements_list

@step('I see "([^"]*)" option selected')
def see_default_option_selected(step, expected):
	select = Select(world.browser.find_element_by_id("pub-date-select"))
	selected_option = select.first_selected_option
    	assert True, selected_option.tget_attribute('value') == expected.lower()
