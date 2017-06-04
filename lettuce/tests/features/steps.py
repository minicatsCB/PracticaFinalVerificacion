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

from selenium.webdriver.support.ui import Select

@step('the select box in the default state')
def have_the_select_box_in_the_default_state(step):
	world.browser.get("http://127.0.0.1:5000")
	#world.browser.execute_script("document.getElementById('pub-date-select').setAttribute('style', 'display:block')");
	select = Select(world.browser.find_element_by_id("pub-date-select"))
	selected_option = select.first_selected_option
    	assert True, selected_option.get_attribute('value') == "today"
	

@step('I select "([^"]*)" option')
def select_the_option(step, expected):
	# Make dropdown list visible in order to select one of its option
	world.browser.execute_script("document.getElementById('pub-date-select').setAttribute('style', 'display:block')");
	select = Select(world.browser.find_element_by_id('pub-date-select'))
	select.select_by_value('2017-05-28')

@step('I see "([^"]*)" option selected')
def see_option_selected(step, expected):
	select = Select(world.browser.find_element_by_id("pub-date-select"))
	selected_option = select.first_selected_option
    	assert True, selected_option.tget_attribute('value') == "today"

# Mejora: hacer que por defecto los <p></p> de la plantilla se rellenen con "", en vez de que no existan
@step('I see words count section in blank')
def see_words_count_sectoin_in_blank(step):
	try:
        	result_field_word = world.browser.find_element_by_name("result-id")
   	except NoSuchElementException:
        	return False
    	return True

