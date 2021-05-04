from driver_initialization import Initializer
from driver_functions import DriverFunctions
import re
from selenium.webdriver.common.action_chains import ActionChains
import locale
import datetime

class HelperFunctions():


	@staticmethod
	def __check_number(string):
		"""check if the string is number. if it number return 
		number, otherwise raise exception"""
		string = string.replace(",","")
		string = string.replace(".","")
		try:
			number = int(string)
			return number
		except:
			raise
	@staticmethod
	def __format_number(string):
		"""example format is: 27.5 K. function will return 27500"""
		number = string.split()[0]

		if "K" in number:
			number = int(float(number[:-1])*1000)
			return number
		elif "M" in number:
			number = int(float(number[:-1])*100000)
			return number
		else:
			number = number.replace(",","")
			number = number.replace(".","")
			return int(number)



	@staticmethod
	def __extract_number(string):
		"""extract number from strings"""
		number = int(re.findall('\d+', string )[0])
		return number

	@staticmethod
	def __extract_username(string):
		"""extract username from strings"""
		username = string.split("@")[1].split()[0]
		
		return username

	@staticmethod
	def __hover_element(driver, element_to_hover_over):
		"""hover the given element"""
		
		hov = ActionChains(driver).move_to_element(element_to_hover_over)
		hov.perform()


	@staticmethod
	def __convertTo24HourFormat(inputTime):
		inputTime_time  = re.findall("[0-9]{2}[:][0-9]{2}", inputTime)[0]
		# Check if last two elements of time is AM and first two elements are 12
		if inputTime[:2] == "ÖÖ"  and inputTime_time[:2] == "12":
			return "00" + inputTime[2:-2][2:-2]
		 
		# remove the AM from input   
		elif inputTime[-2:] == "ÖÖ":
			return inputTime_time[:-2]

		# Check if last two elements of time is PM and first two elements are 12   
		elif inputTime[-2:] == "ÖS" and inputTime_time[:2] == "12":
			return inputTime_time[:-2]
		 
		else:
		# Add 12 to hours and remove PM
			return str(int(inputTime_time[:2]) + 12) + inputTime[2:-2]

	@staticmethod
	def __format_datetime(datetime_str):
		"""make datetime string python datetime object"""
		locale.setlocale(locale.LC_TIME, "tr_TR") 
		time = datetime_str.split("·")[0]
		date = datetime_str.split(" · ")[1]
		return date
		#time = HelperFunctions._HelperFunctions__convertTo24HourFormat(time)
	
	@staticmethod
	def __find_hashtags(post_content):
		pat = re.compile(r"#(\w+)")
		hashtags = pat.findall(post_content)
		return hashtags

	@staticmethod
	def __find_user_mentions(post_content):
		pat = re.compile(r"@([a-zA-Z0-9]{1,24})")
		mentions = pat.findall(post_content)
		return mentions

	@staticmethod
	def __find_urls(post_content):
		pat = re.compile(r'http\S+')
		urls = pat.findall(post_content)
		return urls
