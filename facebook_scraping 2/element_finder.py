from selenium.common.exceptions import NoSuchElementException
from driver_functions import DriverFunctions    
from helper import HelperFunctions
import time
from find_reactions import FindReactions

class Finder():
	"""
	Holds the collections of methods that finds element of the facebook's posts using selenium's
	webdriver's methods  
	"""

		
	@staticmethod
	def __find_post_links(driver, post_number):
		"""finds all posts of the facebook search result using selenium's webdriver's method"""
		#xpath = "//*[@class='rq0escxv l9j0dhe7 du4w35lb hybvsw6c ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi ni8dbmo4 stjgntxs k4urcfbm sbcfpzgs']"
		xpath = "//*[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']"
		post_link_list = []
		while True:
			DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME = 1, SCROLL_NUMBER = 2)
			post_elements = driver.find_elements_by_xpath(xpath)
		
			for item in post_elements:
				post_link = item.get_attribute("href")
				post_link_list.append(post_link)
			post_link_list = list(set(post_link_list))
			if len(post_link_list) >= post_number:
				break
		return post_link_list



	@staticmethod
	def __find_post_date(driver):
		try:
			posted_date_element = driver.find_element_by_xpath("//b[@class='b6zbclly myohyog2 l9j0dhe7 aenfhxwr l94mrbxd ihxqhq3m nc684nl6 t5a262vz sdhka5h4']")
			posted_date = posted_date_element.text
			posted_date = HelperFunctions._HelperFunctions__format_date(posted_date)
			return posted_date
		except:
			posted_date_element = driver.find_element_by_xpath("//*[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']")
			posted_date = posted_date_element.text
			posted_date = HelperFunctions._HelperFunctions__format_date(posted_date)
			return posted_date
		
	
	@staticmethod
	def __find_post_shared_url(driver):
		xpath_1 = "//*[@class='oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 a8c37x1j mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l tm8avpzi']"
		xpath_2 = "//*[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 a8c37x1j p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 p8dawk7l']"
		check = DriverFunctions._DriverFunctions__check_exists_by_xpath(driver, xpath_1)
		if check == True:
			shared_element = driver.find_element_by_xpath(xpath_1)
			shared_url = shared_element.get_attribute("href")		
			return shared_url
		else:
			check = DriverFunctions._DriverFunctions__check_exists_by_xpath(driver, xpath_2)
			if check == True:
				shared_element = driver.find_element_by_xpath(xpath_2)
				shared_url = shared_element.get_attribute("href")		
				return shared_url
			else:
				shared_url = ""
				return shared_url



	@staticmethod
	def __find_post_content(driver):
		
		try:
			post_element = driver.find_element_by_xpath("//*[@role='article']/div/div/div/div/div/div/div/div/div[@dir='auto']")
			content_text = post_element.find_element_by_xpath(".//*[@data-ad-comet-preview='message']")
			content_text = content_text.text
			hashtags_in_content = HelperFunctions._HelperFunctions__get_parsed_hashtags(content_text)
			mentions_in_content = HelperFunctions._HelperFunctions__get_parsed_mentions(content_text)
			#shared_urls_in_content
			return content_text, hashtags_in_content, mentions_in_content
		except:
			content_text = ""
			hashtags_in_content = []
			mentions_in_content = []
			#shared_urls_in_content = ""
			return content_text, hashtags_in_content, mentions_in_content

	@staticmethod
	def __find_img_url_list(driver):
		try:
			img_url_list = []
			img_elements = driver.find_elements_by_xpath("//*[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm']")
			if img_elements != []:
				for element in img_elements:
					img_url = element.get_attribute("src")
					if img_url == None:
						raise Exception
					img_url_list.append(img_url)
			
			return img_url_list
		except:
			img_url_list = []
			return img_url_list

	@staticmethod
	def __find_video_url(driver):
		try:
		
			video_url = driver.find_element_by_tag_name("video").get_attribute("src")	
			return video_url
		except:
			video_url = ""
			return video_url

	@staticmethod
	def __find_comments_number(driver):
		"""finds comments count of the facebook post using selenium's webdriver's method"""
		xpath = "//*[contains(text(), 'Yorum')]"
		try:
			comments_num = driver.find_element_by_xpath(xpath).text
			#extract numbers from text
			comments_num =HelperFunctions._HelperFunctions__extract_number(comments_num)
		except NoSuchElementException:
			comments_num = 0
		except Exception as e:
			print("error at find_comments_number method : {}".format(e))
			comments_num = 0

		return comments_num

	@staticmethod
	def __uncollapse_comments(driver):
		
		xpath  = "//*[@class='oajrlxb2 bp9cbjyn g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 pq6dq46d mg4g778l btwxx1t3 g5gj957u p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys p8fzw8mz qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh gpro0wi8 m9osqain buofh1pr']"
		uncollapse_button = driver.find_elements_by_xpath(xpath)
		for item in uncollapse_button:
			
			# click element by executing javascript
			driver.execute_script("arguments[0].click();", item)

	@staticmethod
	def __get_comments_from_posts(driver, comment_number):
		"""finds comments of the facebook post using selenium's webdriver's method"""

		comment_list = []
		

		print(comment_number)
		follow_loop = range(1,comment_number)
		for x in follow_loop:
			reply_list = []
			try:

				base_xpath = "//div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/ul/li["
				base_xpath += str(x)
				comment_author_xpath = base_xpath + "]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div[1]/a"
				comment_xpath = base_xpath + "]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div[2]"
				reply_xpath = base_xpath + "]/div[2]/div/ul"
				comment_author = driver.find_element_by_xpath(comment_author_xpath)
				comment_author = comment_author.text
				comment_author_url = driver.find_element_by_xpath(comment_author_xpath).get_attribute("href")
				try:
					comment = driver.find_element_by_xpath(comment_xpath).text
				except:
					comment = ""
				comment_dict = {"username":comment_author, "user_url":comment_author_url, "text":comment}
				reply_check = DriverFunctions._DriverFunctions__check_exists_by_xpath(driver,reply_xpath)
				if reply_check == True:
					reply_elements = driver.find_element_by_xpath(reply_xpath)
					reply_elements = reply_elements.find_elements_by_tag_name("li")
					for item in reply_elements:
						try:
							reply = item.find_element_by_xpath(".//*[@class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']")
							reply_user_url =  item.find_element_by_xpath(".//a").get_attribute("href")
							reply_author = reply.text.splitlines()[0]
							reply_text = reply.text.splitlines()[1]
							reply_dict = {"username":reply_author, "user_profile_url":reply_user_url,"text":reply_text}
							reply_list.append(reply_dict)
						except:
							pass
					comment_dict["reply_list"] = reply_list
				else:
					comment_dict["reply_list"] = []
				comment_list.append(comment_dict)
			except:
				pass

		return comment_list

	@staticmethod
	def __get_comment_dict(driver):
		comment_number = Finder._Finder__find_comments_number(driver)
		Finder._Finder__uncollapse_comments(driver)
		comment_list = Finder._Finder__get_comments_from_posts(driver, comment_number)
		print(comment_list)
		return comment_list


	@staticmethod
	def __find_share_count(post):
		"""finds shares count of the facebook post using selenium's webdriver's method"""
		xpath = "//*[contains(text(), 'Paylaşım')]"
		try:
			#aim is to find element that have datatest-id attribute as UFI2SharesCount/root 
			shares = post.find_element_by_xpath(xpath).text
			shares = HelperFunctions._HelperFunctions__format_numbers(shares)

		except NoSuchElementException:
			#if element is not present that means there wasn't any shares
			shares = 0
	@staticmethod
	def __find_hashtag_post_number(driver):
		try:
			number_string = driver.find_element_by_xpath("//*[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr knj5qynh m9osqain hzawbc8m']").text
			number = HelperFunctions._HelperFunctions__hashtag_number(number_string)
			print(number)
			return number
		except:
			number = 0
			return number

	@staticmethod
	def __find_post_details(driver):
		try:
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='article']")
			username = driver.find_element_by_xpath("//h2//strong").text
			post_date = Finder._Finder__find_post_date(driver)
			content_text, hashtags_in_content, mentions_in_content = Finder._Finder__find_post_content(driver)
			shared_url = Finder._Finder__find_post_shared_url(driver)
			img_url_list = Finder._Finder__find_img_url_list(driver)
			video_url = Finder._Finder__find_video_url(driver)
			like_dict = FindReactions._FindReactions__find_likes(driver)
			sad_dict = FindReactions._FindReactions__find_sad(driver)
			wow_dict = FindReactions._FindReactions__find_wow(driver)
			care_dict = FindReactions._FindReactions__find_care(driver)
			haha_dict = FindReactions._FindReactions__find_haha(driver)
			angry_dict = FindReactions._FindReactions__find_angry(driver)
			love_dict = FindReactions._FindReactions__find_love(driver)
			comment_dict = Finder._Finder__get_comment_dict(driver)

			post_url = driver.current_url

			post_dict = {"post_url":post_url,"username":username, "post_date":post_date, "content_text":content_text,
			 "hashtags_in_content":hashtags_in_content, "mentions_in_content":mentions_in_content,
			 "shared_url":shared_url, "img_url_list":img_url_list, "video_url":video_url, "like_dict":like_dict,
			 "sad_dict":sad_dict, "wow_dict":wow_dict, "care_dict":care_dict, "haha_dict":haha_dict,
			 "angry_dict":angry_dict, "love_dict":love_dict, "comment_dict":comment_dict }
			return post_dict
		except Exception as e:
			print(e)
			username = []
			post_date = []
			content_text, hashtags_in_content, mentions_in_content = "", [], []
			shared_url = []
			img_url_list = []
			video_url = []
			like_dict = []
			sad_dict = []
			wow_dict = []
			care_dict = []
			haha_dict = []
			angry_dict = []
			love_dict = []
			post_dict = {"username":username, "post_date":post_date, "content_text":content_text,
			 "hashtags_in_content":hashtags_in_content, "mentions_in_content":mentions_in_content,
			 "shared_url":shared_url, "img_url_list":img_url_list, "video_url":video_url, "like_dict":like_dict,
			 "sad_dict":sad_dict, "wow_dict":wow_dict, "care_dict":care_dict, "haha_dict":haha_dict,
			 "angry_dict":angry_dict, "love_dict":love_dict }



	@staticmethod
	def __find_user_work_and_education(driver, username):

		about_page_url = "/%s/about_work_and_education" % (username)
		DriverFunctions._DriverFunctions__open_new_tab(driver, about_page_url)
		try:
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//*[@data-pagelet='ProfileAppSection_0']")
			result_list = []
			company_list = []
			education_list = []
			items = driver.find_elements_by_xpath("//*[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr o8rfisnq p8fzw8mz pcp91wgn iuny7tx3 ipjc6fyt']")
			for item in items:
				result_list.append(item.text)
			for item in result_list:
				if HelperFunctions._HelperFunctions__get_career(item) != " ":
					company, position, duration, city = HelperFunctions._HelperFunctions__get_career(item)
					company_info = {"company_name":company, "position":position, "duration":duration, "location":city}
					company_list.append(company_info)
				elif HelperFunctions._HelperFunctions__get_university(item) != " ":
					univ, graduateYear, faculty = HelperFunctions._HelperFunctions__get_university(item)
					uni_info = {"university_name":univ, "grad_year":graduateYear, "faculty":faculty}
					education_list.append(uni_info)				
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			result_dict = {"company_list":company_list, "education_list":education_list}
			return result_dict
		except:
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			company_list = []
			education_list = []
			result_dict = {"company_list":company_list, "education_list":education_list}
			return result_dict


	@staticmethod
	def __find_user_about_places(driver, username):
		try:
			about_page_url = "/%s/about_places" % (username)
			DriverFunctions._DriverFunctions__open_new_tab(driver, about_page_url)
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"class","c9zspvje")
			elements = driver.find_elements_by_xpath("//*[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr o8rfisnq p8fzw8mz pcp91wgn iuny7tx3 ipjc6fyt']")
			live_in = ""
			born_in = ""
			for element in elements:
				if "Yaşadığı şehir" in element.text:
					live_in = element.text.splitlines()[0]
				elif "Memleket" in element.text:
					born_in = element.text.splitlines()[0]
			

			DriverFunctions._DriverFunctions__close_current_tab(driver)
			result_dict = {"live_in":live_in, "born_in":born_in}
			return result_dict
		except:
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			result_dict = {"live_in":"", "born_in":""}
			return result_dict

	@staticmethod
	def __find_liked_page_sports(driver,category, username):
		try:
			liked_page_list = []	 
			about_page_url = "/%s/%s" % ( username, category)
			xpath = "//*[@data-pagelet='ProfileAppSection_0']"
			DriverFunctions._DriverFunctions__open_new_tab(driver, about_page_url)
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",xpath)
			category_block = driver.find_element_by_xpath(xpath)
			block_height = category_block.size['height']
			while True:

				DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME = 0.5, SCROLL_NUMBER = 2)
				category_block = driver.find_element_by_xpath(xpath)
				new_block_height = category_block.size['height']
				if new_block_height == block_height:
					break
				block_height = new_block_height


			category_block = driver.find_element_by_xpath(xpath)

			liked_elements = category_block.find_elements_by_tag_name("a")
			for element in liked_elements:
				try:
					page_url = element.get_attribute("href")
					page_name = element.text.splitlines()[0]
					page_category = element.text.splitlines()[1]
					page_dict = {"page_url":page_url, "page_name":page_name, "page_category":page_category}
					liked_page_list.append(page_dict)
				except:
					continue

			DriverFunctions._DriverFunctions__close_current_tab(driver)
			return liked_page_list
		except:
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			liked_page_list = []
			return liked_page_list

	@staticmethod
	def __find_liked_page(driver,category, username):
		try:
			liked_page_list = []	 
			about_page_url = "/%s/%s" % ( username, category)
			xpath = "//*[@data-pagelet='ProfileAppSection_0']"
			DriverFunctions._DriverFunctions__open_new_tab(driver, about_page_url)
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",xpath)
			category_block = driver.find_element_by_xpath(xpath)
			block_height = category_block.size['height']
			while True:

				DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME = 0.5, SCROLL_NUMBER = 2)
				category_block = driver.find_element_by_xpath(xpath)
				new_block_height = category_block.size['height']
				if new_block_height == block_height:
					break
				block_height = new_block_height


			category_block = driver.find_element_by_xpath(xpath)

			liked_elements = category_block.find_elements_by_xpath(".//*[@class='buofh1pr hv4rvrfc']")
			for element in liked_elements:
				try:
					page_url = element.find_element_by_tag_name("a").get_attribute("href")
					page_name = element.text.splitlines()[0]
					page_category = element.text.splitlines()[1]
					page_dict = {"page_url":page_url, "page_name":page_name, "page_category":page_category}
					liked_page_list.append(page_dict)
				except:
					continue

			DriverFunctions._DriverFunctions__close_current_tab(driver)
			return liked_page_list
		except:
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			liked_page_list = []
			return liked_page_list

	@staticmethod
	def __find_user_friends(driver, username):
		try:
			friend_list = []
			about_page_url = "/%s/friends_all" % (username)
			DriverFunctions._DriverFunctions__open_new_tab(driver, about_page_url)
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//*[@class='j83agx80 btwxx1t3 lhclo0ds i1fnvgqd']")
			time.sleep(3)
			
			while True:
				friend_elements = driver.find_elements_by_xpath("//*[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8']")

				if (DriverFunctions._DriverFunctions__check_exists_by_xpath(driver, "//*[@data-pagelet='ProfileAppSection_1']") == True):
					break
				DriverFunctions._DriverFunctions__scroll_down_with_space(driver, SCROLL_PAUSE_TIME = 0.5, SCROLL_NUMBER = 1)
				time.sleep(2)

			for element in friend_elements:
				try:

					user_url = element.get_attribute("href")
					username = user_url.split("/")[-1]
					screen_name = element.text
					user = {"user_url":user_url, "username":username, "screen_name":screen_name}

					friend_list.append(user)
				except:
					continue
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			return friend_list
		except:
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			return friend_list
	@staticmethod
	def __find_user_details(driver, username, detail):
		try:
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//a[@class='oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l oo9gr5id']/div/svg/g/image")
			profile_img_url = driver.find_element_by_xpath("//a[@class='oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l oo9gr5id']/div/svg/g/image").get_attribute("xlink:href")
		except:
			profile_img_url = ""
		try:
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//h1[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80']")		
			screen_name = driver.find_element_by_xpath("//h1[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80']").text
		except:
			screen_name = ""
			print("cannnot get screen name")
		
		try:
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr knj5qynh m9osqain oqcyycmt']")
			user_description = driver.find_element_by_xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr knj5qynh m9osqain oqcyycmt']").text
		except:
			user_description = ""
			print("cannot get user description")
		

		if detail == True:
			user_work_and_education = Finder._Finder__find_user_work_and_education(driver, username)					
			user_about_places = Finder._Finder__find_user_about_places(driver, username)
			user_liked_sport_pages = Finder._Finder__find_liked_page_sports(driver,"sports", username)
			user_liked_music_pages = Finder._Finder__find_liked_page(driver,"music", username)
			user_liked_tv_pages = Finder._Finder__find_liked_page(driver,"tv", username)
			user_liked_movie_pages = Finder._Finder__find_liked_page(driver,"movies", username)
			user_liked_book_pages = Finder._Finder__find_liked_page(driver,"books", username)
			user_friends = Finder._Finder__find_user_friends(driver, username)
		else:
			user_work_and_education = []
			user_about_places = []
			user_liked_sport_pages = []
			user_liked_music_pages = []
			user_liked_tv_pages = []
			user_liked_movie_pages = []
			user_liked_book_pages = []
			user_friends = []
		user_profile_url = driver.current_url

			# Finder._Finder__find_user_map

		result_dict = {"profile_url":user_profile_url,"username":username, "screen_name":screen_name, "user_description":user_description, 
		"profile_img_url":profile_img_url,"user_work_and_education":user_work_and_education, "user_about_places":user_about_places,
		"user_liked_sport_pages":user_liked_sport_pages, "user_liked_music_pages":user_liked_music_pages,
		"user_liked_tv_pages":user_liked_tv_pages, "user_liked_movie_pages":user_liked_movie_pages,
		"user_liked_book_pages":user_liked_book_pages, "user_friends":user_friends}

		return result_dict

	@staticmethod
	def __find_page_details(driver):
		#page_url, page_name, screen_name, category, liked_number, follower_number, bio
		try:
			page_url = driver.current_url[:-1]
			DriverFunctions._DriverFunctions__open_new_tab(driver,"about")
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//*[@class='dati1w0a ihqw7lf3 hv4rvrfc discj3wi d2edcug0 f9o22wc5 nzypyw8j ad2k81qe tr9rh885 rq0escxv l82x9zwi uo3d90p7 pw54ja7n ue3kfks5 hybvsw6c']")
			page_category = driver.find_element_by_xpath("//*[@class='qzhwtbm6 knvmm38d']/span/span/a").text
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//div[@class='bi6gxh9e aov4n071']/h2[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl d2edcug0 hpfvmrgz']")
			screen_name = driver.find_element_by_xpath("//div[@class='bi6gxh9e aov4n071']/h2[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl d2edcug0 hpfvmrgz']").text
			try:
				DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//span/span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']")
				page_name = driver.find_element_by_xpath("//span/span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']").text
			except:
				page_name = ""
			number_elements = driver.find_elements_by_xpath("//*[contains(text(), 'kişi')]")
			like_number = HelperFunctions._HelperFunctions__format_numbers(number_elements[0].text)
			follower_number = HelperFunctions._HelperFunctions__format_numbers(number_elements[1].text)
			# DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath","//*[@class='oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l oo9gr5id']/div/svg/g/image")
			# profile_img_url = driver.find_element_by_xpath("//*[@class='oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l oo9gr5id']/div/svg/g/image").get_attribute("xlink:href")
			description_elements = driver.find_elements_by_xpath("//*[@class='j83agx80 cbu4d94t ew0dbk1b irj2b8pg']")
			for element in description_elements:
				if "Hakkında" in element.text:
					description = element.find_element_by_xpath(".//*[@class = 'qzhwtbm6 knvmm38d']").text
					break
				else:
					description =  ""
				
				
			result_dict = {"page_url":page_url, "page_name":page_name, "screen_name":screen_name, "category":page_category,
			 "liked_number":like_number, "follower_number":follower_number, "bio":description}
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			return result_dict
		except:
			result_dict = {"page_url":"", "page_name":"", "screen_name":"", "category":"",
			 "liked_number":"", "follower_number":"", "bio":""}
			DriverFunctions._DriverFunctions__close_current_tab(driver)
			return result_dict


	@staticmethod
	def __find_posts(driver, post_link_list):
		post_list = []
		for post_link in post_link_list:
			DriverFunctions._DriverFunctions__open_new_tab(driver, post_link)
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='article']")
			post_dict = Finder._Finder__find_post_details(driver)
			post_dict["post_url"] = post_link
			post_list.append(post_dict)
			DriverFunctions._DriverFunctions__close_current_tab(driver)
		
		return post_list

	@staticmethod
	def __find_all_posts(driver, post_number = 10):
		"""finds all posts of the facebook search result using selenium's webdriver's method"""
		
		post_links = Finder._Finder__find_post_links(driver, post_number)
		post_details_list = Finder._Finder__find_posts(driver, post_links)
		return post_details_list
		
	@staticmethod
	def __find_posts_clicking_date_in_hashtag(driver, post_number = 3, username = None):
		"""finds all posts of the facebook hashtag search result using selenium's webdriver's method"""
		post_list = []
		post_xpath = "//*[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']"

		while True:

			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='article']")
			post_elements = driver.find_elements_by_xpath(post_xpath)
			for post in post_elements:
				if post.text == '':
					continue
				DriverFunctions._DriverFunctions__open_new_tab_ctrl(driver,post)
				if username != None and username not in driver.current_url:
					#DriverFunctions._DriverFunctions__close_current_tab(driver)
					continue
				p = Finder._Finder__find_post_details(driver)
				post_list.append(p)
				DriverFunctions._DriverFunctions__close_current_tab(driver)
				time.sleep(2)
				if len(post_list) >= post_number:
					break
			post_list = [i for n, i in enumerate(post_list) if i not in post_list[n + 1:]]
			if len(post_list) >= post_number:
				break
			DriverFunctions._DriverFunctions__scroll_down_with_space(driver, SCROLL_PAUSE_TIME =1, SCROLL_NUMBER = 4)
		return post_list

	# @staticmethod
	# def __find_posts_clicking_date_in_page(driver, post_number = 10):
	# 	"""finds all posts of the facebook hashtag search result using selenium's webdriver's method"""
	# 	post_list = []
	# 	post_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div//div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a"
	# 	while True:
			
	# 		DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='article']")
	# 		post_elements = driver.find_elements_by_xpath(post_xpath)
	# 		for post in post_elements:
	# 			if post.text == '':
	# 				continue
	# 			DriverFunctions._DriverFunctions__open_new_tab_ctrl(driver,post)

	# 			p = Finder._Finder__find_post_details(driver)
	# 			post_list.append(p)
	# 			DriverFunctions._DriverFunctions__close_current_tab(driver)
	# 			time.sleep(2)
	# 			if len(post_list) >= post_number:
	# 				break
	# 		post_list = [i for n, i in enumerate(post_list) if i not in post_list[n + 1:]]
	# 		if len(post_list) >= post_number:
	# 			break
	# 		DriverFunctions._DriverFunctions__scroll_down_with_space(driver, SCROLL_PAUSE_TIME = 0.5, SCROLL_NUMBER = 2)
	# 	return post_list

		






	