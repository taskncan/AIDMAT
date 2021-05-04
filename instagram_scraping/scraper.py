import argparse
import time
import json
import csv
from element_finder import Finder
from driver_initialization import Initializer
from driver_functions import DriverFunctions
from helper import HelperFunctions


class Instagram_scraper():
    URL = "https://www.instagram.com"
    RETRY_LIMIT = 10

    retry = 10
    """
		todo: GET WHAT TO GET AS PARAMETER
	"""

    def __init__(self, browser="chrome"):

        self.URL = "https://www.instagram.com"
        self.browser = browser
        self.driver = ''

    def login(self, login_username, login_password):
        driver = self.driver
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "name", "username")
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "name", "password")
        username_element = driver.find_element_by_name("username")
        username_element.send_keys(login_username)
        pass_elem = driver.find_element_by_name("password")
        pass_elem.send_keys(login_password)
        login_btn = driver.find_element_by_css_selector(".L3NKy")
        login_btn.click()
        time.sleep(5)

    def start_driver(self):
        """changes the class member driver value to driver on call"""
        self.driver = Initializer(self.browser).init()

    def get_user_profile(self, username, is_search_post):
        """
			To get user profile information such as username, 
			bio, profile picture url, post number, follower number,
			following number with given username.
		"""
        # self.start_driver()
        # self.driver.get(self.URL)
        # self.login(login_username, login_password)

        url = "%s/%s/" % (self.URL, username)
        DriverFunctions._DriverFunctions__open_new_tab(self.driver, url)

        DriverFunctions._DriverFunctions__wait_for_element_to_appear(self.driver, "xpath", "//*[@role='main']")

        profile_dict = Finder._Finder__find_user_profile(self.driver, username, is_search_post)

        return profile_dict

    def get_user_posts(self, username: object, number: object = None) -> object:
        """
			To get user posts with given username. If 
			a number also given function will return given 
			number of posts else it will return all posts of the
			user. Another option is detail, it is boolean parameter.
			If it is true function will return posts with all details
			of them.
		"""
        user_profile = self.get_user_profile(username, True)

        if not number:
            number = user_profile["post_num"]
            results = Finder._Finder__get_posts(self.driver, number)
            print(results)
            for i in results: i["username"] = username
            if len(self.driver.window_handles) > 1:
                DriverFunctions._DriverFunctions__close_current_tab(self.driver)
            return results
        else:
            results = Finder._Finder__get_posts(self.driver, number)
            print(results)
            for i in results: i["username"] = username
        if len(self.driver.window_handles) > 1:
            DriverFunctions._DriverFunctions__close_current_tab(self.driver)
            return results

    def get_hashtag_results(self, hashtag, post_number):
        """get elements of search result of given hashtag. """
        # self.start_driver()
        # self.driver.get(self.URL)
        # self.login(login_username, login_password)

        url = "%s/explore/tags/%s/" % (Instagram_scraper.URL, hashtag)
        self.driver.get(url)
        """ **** STRING GET FONKSIYONU ALMIYOR **** """

        result_list = Finder._Finder__get_posts(self.driver, post_number)
        return result_list
