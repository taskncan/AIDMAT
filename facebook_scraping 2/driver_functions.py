from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class DriverFunctions:

	@staticmethod
	def __close_driver(driver):
		"""expects driver's instance, closes the driver"""
		try:
			driver.close()
			driver.quit()
		except Exception as e:
			print("error at close_driver method : {}".format(e))

	@staticmethod
	def __scroll_down(driver, SCROLL_PAUSE_TIME = 0.5, SCROLL_NUMBER = 2):
		"""expects driver's instance as a argument, and it scrolls down page to the most bottom till the height"""
		# Get scroll height
		last_height = driver.execute_script("return document.body.scrollHeight")
		count = 0
		while True:		
			try:
				if SCROLL_NUMBER != None and count == SCROLL_NUMBER:
					break

				# Scroll down to bottom
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				
				# Wait to load page
				time.sleep(SCROLL_PAUSE_TIME)

				# Calculate new scroll height and compare with last scroll height
				new_height = driver.execute_script("return document.body.scrollHeight")
				if new_height == last_height:
					break
				last_height = new_height
				count += 1
			except Exception as e:
				#if any error occured than close the driver and exit
				print("error at scroll_down method : {}".format(e))
	
	@staticmethod
	def __scroll_down_with_space(driver, SCROLL_PAUSE_TIME = 0.5, SCROLL_NUMBER = 1):
		"""expects driver's instance as a argument, and it scrolls down page to the most bottom till the height"""
		# Get scroll height

		actions = ActionChains(driver)
		for _ in range(SCROLL_NUMBER):
			actions.send_keys(Keys.SPACE).perform()
			time.sleep(SCROLL_PAUSE_TIME)

	@staticmethod
	def __check_exists_by_class_name(driver, class_name):
		try:
			driver.find_element_by_class_name(class_name)
		except NoSuchElementException:
			return False
		return True

	@staticmethod
	def __check_exists_by_tag_name(driver, tag_name):
	    try:
	        driver.find_element_by_tag_name(tag_name)
	    except NoSuchElementException:
	        return False
	    return True

	@staticmethod
	def __check_exists_by_xpath(driver, xpath):
		try:
			driver.find_element_by_xpath(xpath)
		except NoSuchElementException:
			return False
		return True
	@staticmethod
	def __wait_for_element_to_appear(driver, locator, element):
		"""
			Find an element given a locator
		"""
		if locator == "xpath":
			try:
				#wait for page to load so posts are visible
				WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,element)))
			except WebDriverException:
				#if it was not found,it means either page is not loading or it does not exists
				print("Nothing found!")
				raise Exception


			except Exception as e:
				print("error at wait_for_element_to_appear method : {}".format(e))
		
		elif locator == "css_selector":
			try:
				#wait for page to load so posts are visible
				WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,element)))
			except WebDriverException:
				#if it was not found,it means either page is not loading or it does not exists
				print("No posts were found!")
	

			except Exception as e:
				print("error at wait_for_element_to_appear method : {}".format(e))


		elif locator == "class":
			try:
				#wait for page to load so posts are visible
				WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,element)))
			except WebDriverException:
				#if it was not found,it means either page is not loading or it does not exists
				print("No posts were found!")
		

			except Exception as e:
				print("error at wait_for_element_to_appear method : {}".format(e))
	

		elif locator == "name":
			try:
				#wait for page to load so posts are visible
				WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME,element)))
			except WebDriverException:
				#if it was not found,it means either page is not loading or it does not exists
				print("No posts were found!")
		

			except Exception as e:
				print("error at wait_for_element_to_appear method : {}".format(e))

	
	@staticmethod
	def __open_new_tab_ctrl(driver,post):
		action = ActionChains(driver)
		action.move_to_element(post).key_down(Keys.CONTROL).click(post).key_up(Keys.CONTROL).perform()
		driver.switch_to.window(driver.window_handles[-1])

	@staticmethod
	def __open_new_tab(driver, url):
		driver.execute_script("window.open('%s');" %url)
		driver.switch_to.window(driver.window_handles[-1])
	@staticmethod
	def __close_current_tab(driver):
		driver.close()
		driver.switch_to.window(driver.window_handles[0])
		time.sleep(3)







