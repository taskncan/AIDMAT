import argparse
import time
import json
import csv
from element_finder import Finder
from driver_initialization import Initializer
from driver_functions import DriverFunctions
from helper import HelperFunctions


class Twitter_scraper():
	URL = "https://www.twitter.com"
	RETRY_LIMIT = 10

	retry = 10
	"""
		todo: GET WHAT TO GET AS PARAMETER
	"""
	def __init__(self,browser="chrome"):
		

		self.URL = "https://www.twitter.com/"
		self.browser = browser
		self.driver = ''

	def login(self,login_username,password):
		driver = self.driver
		DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "name", "session[username_or_email]")
		DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "name", "session[password]")
		username_element = driver.find_element_by_name("session[username_or_email]")
		username_element.send_keys(login_username)
		pass_elem = driver.find_element_by_name("session[password]")
		pass_elem.send_keys(password)
		login_btn = driver.find_element_by_xpath("//*[@data-testid='LoginForm_Login_Button']")
		login_btn.click()
		time.sleep(5)

	def start_driver(self):
		"""changes the class member driver value to driver on call"""
		self.driver = Initializer(self.browser).init()

	def get_user_profile(self, username, is_detail):
		"""
			To get user profile information such as username, 
			bio, profile picture url, post number, follower number,
			following number with given username.
		"""

		try:
			url = "%s/%s/" % (self.URL, username)
			self.driver.get(url)
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver,"xpath", "//*[@role='main']")
			profile_dict = Finder._Finder__find_user_profile(self.driver,username, is_detail)
			if len(self.driver.window_handles)>2:
				DriverFunctions._DriverFunctions__close_current_tab(self.driver)
			return profile_dict
		except:
			raise

	def get_user_posts(self, username, post_number):
		"""
			To get user posts with given username. If 
			a number also given function will return given 
			number of posts else it will return all posts of the
			user. Another option is detail, it is boolean parameter.
			If it is true function will return posts with all details
			of them.
		"""
		# user_profile = self.get_user_profile(username, True)
		# print(user_profile)
		if post_number is None:
			profile_dict = self.get_user_profile( username, False)
			post_number = profile_dict["post_number"]

		url = "%s/%s/with_replies" % (self.URL, username)
		self.driver.get(url)

		DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver,"xpath", "//*[@role='main']")
		results = Finder._Finder__find_posts(self.driver, username, post_number)
		if len(self.driver.window_handles)>2:
			DriverFunctions._DriverFunctions__close_current_tab(self.driver)
		return results

	def get_user_posts_with_url(self, post_info_list):

		results = Finder._Finder__find_post_details(self.driver, post_info_list)

		return results


	def search_hashtag(self, hashtag, post_number=10):
		"""
			To get user posts with given username. If 
			a number also given function will return given 
			number of posts else it will return all posts of the
			user. Another option is detail, it is boolean parameter.
			If it is true function will return posts with all details
			of them.
		"""
		# user_profile = self.get_user_profile(username, True)
		# print(user_profile)
		# self.start_driver()
		# self.driver.get(Twitter_scraper.URL + "/login")
		# self.login(login_username, password)
		url = self.URL + "/search?q=%23"+hashtag+"&src=typed_query"
		self.driver.get(url)
		DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver,"xpath", "//*[@role='main']")
		results = Finder._Finder__find_hashtag_posts(self.driver, post_number)
		if len(self.driver.window_handles)>2:
			DriverFunctions._DriverFunctions__close_current_tab(self.driver)
		return results





