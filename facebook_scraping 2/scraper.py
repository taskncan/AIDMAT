from element_finder import Finder
from helper import HelperFunctions
from driver_initialization import Initializer
from driver_functions import DriverFunctions

from selenium.common.exceptions import NoSuchElementException
import json
import csv
import os
import time

email = "gokhankarahan787@yahoo.com"
password = "kdrhnKRHN787"
# email = "cemetnosce@ymail.com"
# password = "kdrhnKRHN787/(/"

class Facebook_scraper:

	retry = 10
	"""
		todo: GET WHAT TO GET AS PARAMETER
	"""
	def __init__(self,browser="chrome"):
		
		self.URL = "https://www.facebook.com"
		self.browser = browser
		self.driver = ''



	def login(self):
		driver = self.driver
		driver.get(self.URL+"/login")
		DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@id='loginform']")

		email_elem = driver.find_element_by_name("email")
		email_elem.send_keys(email)
		pass_elem = driver.find_element_by_name("pass")
		pass_elem.send_keys(password)
		login_button = driver.find_element_by_name("login")
		login_button.click()
		time.sleep(5)

	def start_driver(self):
		"""changes the class member driver value to driver on call"""
		self.driver = Initializer(self.browser).init()


	def search_posts(self, search_string):
		#call the start_driver and override class member driver to webdriver's instance

		#navigate to URL
		search = "%s/search/posts/?q=/%s/" % (self.URL, search_string)
		self.driver.get(search)
		DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "xpath", "//*[@role='feed']")
		
		result_dict = Finder._Finder__find_all_posts(self.driver)
		

		return result_dict

	def search_hashtag(self, search_hashtag):
		#call the start_driver and override class member driver to webdriver's instance

		#navigate to URL
		search = "%s/hashtag/%s/" % (self.URL, search_hashtag)
		self.driver.get(search)
		DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "xpath", "//*[@role='article']")
		total_post_number = Finder._Finder__find_hashtag_post_number(self.driver)
		result_dict = Finder._Finder__find_posts_clicking_date_in_hashtag(self.driver)
		
		#close the browser window after job is done.

		return result_dict

	def search_user(self, username, get_posts = False, detail = True):
		#call the start_driver and override class member driver to webdriver's instance
		try:
			#navigate to URL
			search = "%s/%s/" % (self.URL, username)
			self.driver.get(search)
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "xpath", "//*[@data-pagelet='ProfileComposer']")
			result_dict = Finder._Finder__find_user_details(self.driver, username, detail)
			
			if get_posts == True:
				#since the getting post layout is same with getting hashtags we can use same function
				try:
					user_posts = Finder._Finder__find_posts_clicking_date_in_hashtag(self.driver, post_number = 2, username=username)
					result_dict["user_posts"] = user_posts
				except:
					result_dict["user_posts"] = []
			#close the browser window after job is done.
			# DriverFunctions._DriverFunctions__close_driver(self.driver)
			return result_dict
		except:
			result_dict = {}
			return result_dict
	
	def search_page(self, username, search_post = False):
		#call the start_driver and override class member driver to webdriver's instance

		#navigate to URL
		search = "%s/%s/" % (self.URL, username)
		self.driver.get(search)
		DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "xpath", "//*[@role='main']")
		result_dict = Finder._Finder__find_page_details(self.driver)
		if search_post == True:
			user_posts = Finder._Finder__find_posts_clicking_date_in_hashtag(self.driver, post_number = 2)
			result_dict["user_posts"] = user_posts


		return result_dict