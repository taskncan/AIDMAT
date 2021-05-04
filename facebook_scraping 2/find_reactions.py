from helper import HelperFunctions
from driver_functions import DriverFunctions
import time
class FindReactions():

	@staticmethod
	def __find_likes(driver):
		liker_list = []
		xpath = "//*[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/*[contains(@aria-label,'Beğen') and (@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l')]"
		try:
			element = driver.find_element_by_xpath(xpath)
			like_number_element = element.get_attribute("aria-label")
			like_number = HelperFunctions._HelperFunctions__extract_number(like_number_element)

			driver.execute_script("arguments[0].click();", element)

			popup_element_xpath = "//*[@class='q5bimw55 rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 eg9m0zos l9j0dhe7 du4w35lb ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 kh7kg01d c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso']//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",popup_element_xpath)

			#scroll_bar_xpath = "//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			user_element_xpath = "//*[@class='ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi a8c37x1j']/div/div[2]/div[1]/div/div/div/span/div/a"
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",popup_element_xpath)
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",user_element_xpath)
			scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")

			while True:
			
				item_list = driver.find_elements_by_xpath(user_element_xpath)
				
				driver.execute_script("arguments[0].scrollIntoView();", item_list[-1])
				time.sleep(2)
				new_scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
				if scroll_bar_height == new_scroll_bar_height:
					break
				scroll_bar_height = new_scroll_bar_height

			for item in item_list:
				try:
					like_user_profile_url = item.get_attribute("href")
					like_username = item.text
					like = {"like_username":like_username, "like_user_profile_url":like_user_profile_url}
					liker_list.append(like)
				except:
					like = {"like_username":"", "like_user_profile_url":""}
					liker_list.append(like)


			like_dict = {"like_number":like_number, "like_list":liker_list}
			close_xpath = "//*[contains(@aria-label,'Kapat')]"
			driver.find_element_by_xpath(close_xpath).click()
			return like_dict
		except Exception as e:
			print(e)
			like_number = 0
			liker_list = []
			like_dict = {"like_number":like_number, "like_list":liker_list}
			return like_dict


	@staticmethod
	def __find_sad(driver):

		sad_list = []
		xpath = "//*[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/*[contains(@aria-label,'Üzgün') and (@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l')]"
		try:
			element = driver.find_element_by_xpath(xpath)
			sad_number_element = element.get_attribute("aria-label")
			sad_number = HelperFunctions._HelperFunctions__extract_number(sad_number_element)

			driver.execute_script("arguments[0].click();", element)
			
			popup_element_xpath = "//*[@class='q5bimw55 rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 eg9m0zos l9j0dhe7 du4w35lb ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 kh7kg01d c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso']//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",popup_element_xpath)

			#scroll_bar_xpath = "//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			user_element_xpath = "//div[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m')]//a"
						
			scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
			while True:
			
				item_list = driver.find_elements_by_xpath(user_element_xpath)
			
				driver.execute_script("arguments[0].scrollIntoView();", item_list[-1])
				time.sleep(1)
				new_scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
				if scroll_bar_height == new_scroll_bar_height:
					break
				scroll_bar_height = new_scroll_bar_height

			for item in item_list:
				#print(item.find_element_by_tag_name("a"))
				sad_user_profile_url = item.get_attribute("href")
				sad_username = item.text
				sad = {"sad_username":sad_username, "sad_user_profile_url":sad_user_profile_url}
				sad_list.append(sad)


			sad_dict = {"sad_number":sad_number, "sad_list":sad_list}
			close_xpath = "//*[contains(@aria-label,'Kapat')]"
			driver.find_element_by_xpath(close_xpath).click()
			return sad_dict

		except Exception as e:
			sad_number = 0
			sad_list = []
			sad_dict = {"sad_number":sad_number, "sad_list":sad_list}
			return sad_dict

	@staticmethod
	def __find_wow(driver):

		wow_list = []
		xpath = "//*[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/*[contains(@aria-label,'İnanılmaz') and (@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l')]"
		try:
			element = driver.find_element_by_xpath(xpath)
			wow_number_element = element.get_attribute("aria-label")
			wow_number = HelperFunctions._HelperFunctions__extract_number(wow_number_element)

			driver.execute_script("arguments[0].click();", element)

			popup_element_xpath = "//*[@class='q5bimw55 rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 eg9m0zos l9j0dhe7 du4w35lb ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 kh7kg01d c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso']//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",popup_element_xpath)

			#scroll_bar_xpath = "//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			user_element_xpath = "//div[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m')]//a"
			time.sleep(2)
			scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
			while True:
			
				item_list = driver.find_elements_by_xpath(user_element_xpath)
			
				driver.execute_script("arguments[0].scrollIntoView();", item_list[-1])
				time.sleep(2)
				new_scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
				if scroll_bar_height == new_scroll_bar_height:
					break
				scroll_bar_height = new_scroll_bar_height

			for item in item_list:
				#print(item.find_element_by_tag_name("a"))
				wow_user_profile_url = item.get_attribute("href")
				wow_username = item.text
				wow = {"wow_username":wow_username, "wow_user_profile_url":wow_user_profile_url}
				wow_list.append(wow)


			wow_dict = {"wow_number":wow_number, "wow_list":wow_list}
			close_xpath = "//*[contains(@aria-label,'Kapat')]"
			driver.find_element_by_xpath(close_xpath).click()
			return wow_dict

		except Exception as e:
			wow_number = 0
			wow_list = []
			wow_dict = {"wow_number":wow_number, "wow_list":wow_list}
			return wow_dict

	@staticmethod
	def __find_care(driver):

		care_list = []
		xpath = "//*[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/*[contains(@aria-label,'Yanındayım') and (@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l')]"
		try:
			element = driver.find_element_by_xpath(xpath)
			care_number_element = element.get_attribute("aria-label")
			care_number = HelperFunctions._HelperFunctions__extract_number(care_number_element)

			driver.execute_script("arguments[0].click();", element)

			popup_element_xpath = "//*[@class='q5bimw55 rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 eg9m0zos l9j0dhe7 du4w35lb ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 kh7kg01d c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso']//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",popup_element_xpath)

			#scroll_bar_xpath = "//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			user_element_xpath = "//div[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m')]//a"
			time.sleep(2)
			scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
			while True:
			
				item_list = driver.find_elements_by_xpath(user_element_xpath)
			
				driver.execute_script("arguments[0].scrollIntoView();", item_list[-1])
				time.sleep(2)
				new_scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
				if scroll_bar_height == new_scroll_bar_height:
					break
				scroll_bar_height = new_scroll_bar_height

			for item in item_list:
				#print(item.find_element_by_tag_name("a"))
				care_user_profile_url = item.get_attribute("href")
				care_username = item.text
				care = {"care_username":care_username, "care_user_profile_url":care_user_profile_url}
				care_list.append(care)


			care_dict = {"care_number":care_number, "care_list":care_list}
			close_xpath = "//*[contains(@aria-label,'Kapat')]"
			driver.find_element_by_xpath(close_xpath).click()
			return care_dict

		except Exception as e:
			care_number = 0
			care_list = []
			care_dict = {"care_number":care_number, "care_list":care_list}
			return care_dict


	@staticmethod
	def __find_haha(driver):

		haha_list = []
		xpath = "//*[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/*[contains(@aria-label,'Hahaha') and (@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l')]"
		try:
			element = driver.find_element_by_xpath(xpath)
			haha_number_element = element.get_attribute("aria-label")
			haha_number = HelperFunctions._HelperFunctions__extract_number(haha_number_element)

			driver.execute_script("arguments[0].click();", element)

			popup_element_xpath = "//*[@class='q5bimw55 rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 eg9m0zos l9j0dhe7 du4w35lb ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 kh7kg01d c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso']//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",popup_element_xpath)
			#scroll_bar_xpath = "//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			user_element_xpath = "//div[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m')]//a"
			time.sleep(2)
			scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
			while True:
			
				item_list = driver.find_elements_by_xpath(user_element_xpath)
			
				driver.execute_script("arguments[0].scrollIntoView();", item_list[-1])
				time.sleep(2)
				new_scroll_bar_height = driver.find_elements_by_xpath(scroll_bar_xpath)[1].value_of_css_property("height")
				if scroll_bar_height == new_scroll_bar_height:
					break
				scroll_bar_height = new_scroll_bar_height

			for item in item_list:
				haha_user_profile_url = item.get_attribute("href")
				haha_username = item.text
				haha = {"haha_username":haha_username, "haha_user_profile_url":haha_user_profile_url}
				haha_list.append(haha)
		


			haha_dict = {"haha_number":haha_number, "haha_list":haha_list}
			close_xpath = "//*[contains(@aria-label,'Kapat')]"
			driver.find_element_by_xpath(close_xpath).click()
			return haha_dict

		except Exception as e:
			haha_number = 0
			haha_list = []
			haha_dict = {"haha_number":haha_number, "haha_list":haha_list}
			return haha_dict

	@staticmethod
	def __find_angry(driver):

		angry_list = []
		xpath = "//*[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/*[contains(@aria-label,'Kızgın') and (@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l')]"
		try:
			element = driver.find_element_by_xpath(xpath)
			angry_number_element = element.get_attribute("aria-label")
			angry_number = HelperFunctions._HelperFunctions__extract_number(angry_number_element)

			driver.execute_script("arguments[0].click();", element)

			popup_element_xpath = "//*[@class='q5bimw55 rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 eg9m0zos l9j0dhe7 du4w35lb ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 kh7kg01d c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso']//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",popup_element_xpath)

			#scroll_bar_xpath = "//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			user_element_xpath = "//div[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m')]//a"
			time.sleep(2)
			scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
			while True:
			
				item_list = driver.find_elements_by_xpath(user_element_xpath)
			
				driver.execute_script("arguments[0].scrollIntoView();", item_list[-1])
				time.sleep(2)
				new_scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
				if scroll_bar_height == new_scroll_bar_height:
					break
				scroll_bar_height = new_scroll_bar_height

			for item in item_list:
				#print(item.find_element_by_tag_name("a"))
				angry_user_profile_url = item.get_attribute("href")
				angry_username = item.text
				angry = {"angry_username":angry_username, "angry_user_profile_url":angry_user_profile_url}
				angry_list.append(angry)


			angry_dict = {"angry_number":angry_number, "angry_list":angry_list}
			close_xpath = "//*[contains(@aria-label,'Kapat')]"
			driver.find_element_by_xpath(close_xpath).click()
			return angry_dict

		except Exception as e:
			angry_number = 0
			angry_list = []
			angry_dict = {"angry_number":angry_number, "angry_list":angry_list}
			return angry_dict

	@staticmethod
	def __find_love(driver):

		love_list = []
		xpath = "//*[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/*[contains(@aria-label,'Muhteşem') and (@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l')]"
		try:
			element = driver.find_element_by_xpath(xpath)
			love_number_element = element.get_attribute("aria-label")
			love_number = HelperFunctions._HelperFunctions__extract_number(love_number_element)

			driver.execute_script("arguments[0].click();", element)

			popup_element_xpath = "//*[@class='q5bimw55 rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 eg9m0zos l9j0dhe7 du4w35lb ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 kh7kg01d c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso']//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver,"xpath",popup_element_xpath)

			#scroll_bar_xpath = "//*[@class='rq0escxv mkhogb32 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kwrap0ej kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']"
			user_element_xpath = "//div[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m')]//a"
			time.sleep(2)
			scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
			while True:
			
				item_list = driver.find_elements_by_xpath(user_element_xpath)
			
				driver.execute_script("arguments[0].scrollIntoView();", item_list[-1])
				time.sleep(2)
				new_scroll_bar_height = driver.find_element_by_xpath(popup_element_xpath).value_of_css_property("height")
				if scroll_bar_height == new_scroll_bar_height:
					break
				scroll_bar_height = new_scroll_bar_height

			for item in item_list:
				#print(item.find_element_by_tag_name("a"))
				love_user_profile_url = item.get_attribute("href")
				love_username = item.text
				love = {"love_username":love_username, "love_user_profile_url":love_user_profile_url}
				love_list.append(love)


			love_dict = {"love_number":love_number, "love_list":love_list}
			close_xpath = "//*[contains(@aria-label,'Kapat')]"
			driver.find_element_by_xpath(close_xpath).click()
			return love_dict

		except Exception as e:
			love_number = 0
			love_list = []
			love_dict = {"love_number":love_number, "love_list":love_list}
			return love_dict