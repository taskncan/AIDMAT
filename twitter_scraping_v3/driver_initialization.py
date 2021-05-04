from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions   
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager



class Initializer:

	def __init__(self, browser_name):
		self.browser_name = browser_name

	def set_properties(self,browser_option):
		"""adds capabilities to the driver"""
		#browser_option.add_argument('--headless')   #runs browser in headless mode

		browser_option.add_argument("--disable-dev-shm-usage")
		browser_option.add_argument('--ignore-certificate-errors')
		browser_option.add_argument('--disable-gpu')
		browser_option.add_argument('--log-level=3')
		browser_option.add_argument('--disable-notifications')
		browser_option.add_argument('--disable-popup-blocking')
		browser_option.add_argument("--lang=en-US")
		return browser_option

	def set_driver_for_browser(self,browser_name):
		"""expects browser name and returns a driver instance"""
		#if browser is suppose to be chrome 
		if browser_name.lower() == "chrome":
			browser_option = ChromeOptions()
			#automatically installs chromedriver and initialize it and returns the instance
			return webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=self.set_properties(browser_option))
		elif browser_name.lower() == "firefox":
			browser_option = FirefoxOptions()
			#automatically installs geckodriver and initialize it and returns the instance
			return webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=self.set_properties(browser_option))
		else:
			#if browser_name is not chrome neither firefox than raise an exception 
			raise Exception("Browser not supported!")

	def init(self):
		"""returns driver instance"""
		driver = self.set_driver_for_browser(self.browser_name)
		return driver

