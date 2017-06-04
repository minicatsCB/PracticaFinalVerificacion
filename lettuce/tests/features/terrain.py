from lettuce import *
from selenium import webdriver

@before.all
def setup_browser():
	world.browser = webdriver.Chrome()
	world.browser.implicitly_wait(1)

@after.all
def tear_down_feature(feature):
	world.browser.quit

