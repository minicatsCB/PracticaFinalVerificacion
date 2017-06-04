from lettuce import *
import lettuce_webdriver.webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

@before.all
def setup_browser():
	world.browser = webdriver.Chrome()
	world.browser.implicitly_wait(1)

@after.all
def tear_down_feature(feature):
	world.browser.quit

