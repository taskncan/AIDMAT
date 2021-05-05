from selenium.common.exceptions import NoSuchElementException
from helper import HelperFunctions
from driver_functions import DriverFunctions
import sys
import urllib.request
import re
import time
import locale
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from selenium.webdriver.common.keys import Keys


class Finder():
    """
	Holds the collections of methods that finds element of the instagram posts using selenium's webdriver's methods  
	"""

    @staticmethod
    def __find_user_profile_header(driver):
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath",
                                                                     "//*[@data-testid='UserProfileHeader_Items']")
        elements = driver.find_elements_by_xpath("//*[@data-testid='UserProfileHeader_Items']")
        for element in elements:
            print(element.text)

    @staticmethod
    def __find_user_description(driver):

        is_exist = DriverFunctions._DriverFunctions__check_exists_by_xpath(driver,
                                                                           "//*[@data-testid='UserDescription']")
        if is_exist == True:
            element = driver.find_element_by_xpath("//*[@data-testid='UserDescription']").text
            return element
        else:
            return ""

    @staticmethod
    def __find_user_website(driver):

        is_exist = DriverFunctions._DriverFunctions__check_exists_by_xpath(driver,
                                                                           "//*[@class='css-4rbku5 css-18t94o4 css-901oao css-16my406 r-13gxpu9 r-1loqt21 r-4qtqp9 r-poiln3 r-zso239 r-bcqeeo r-qvutc0']")
        if is_exist == True:
            element = driver.find_element_by_xpath(
                "//*[@class='css-4rbku5 css-18t94o4 css-901oao css-16my406 r-13gxpu9 r-1loqt21 r-4qtqp9 r-poiln3 r-zso239 r-bcqeeo r-qvutc0']").text
            return element
        else:
            return ""

    @staticmethod
    def __find_user_join_date(driver):

        is_exist = DriverFunctions._DriverFunctions__check_exists_by_xpath(driver, "//*[contains(text(), 'Joined')]")
        if is_exist == True:
            element = driver.find_element_by_xpath("//*[contains(text(), 'Joined')]").text
            element = element.split()[1:]
            date = " ".join(element)
            date_time_obj = datetime.strptime(date, '%B %Y')
            return date_time_obj
        else:
            return ""

    @staticmethod
    def __find_user_following_number(driver, username):

        is_exist = DriverFunctions._DriverFunctions__check_exists_by_xpath(driver,
                                                                           "//*[@class='css-4rbku5 css-18t94o4 css-901oao r-1fmj7o5 r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']")
        if is_exist == True:

            try:
                element_to_hover_over = driver.find_element_by_xpath("//a[@href='/" + username + "/following']")
                number = element_to_hover_over.text
                number = HelperFunctions._HelperFunctions__format_number(number)
                return number
            except:
                element = driver.find_element_by_xpath("//a[@href='/" + username + "/following']").text
                number = HelperFunctions._HelperFunctions__extract_number(element)
                return number
        else:
            return ""

    @staticmethod
    def __find_user_follower_number(driver, username):

        is_exist = DriverFunctions._DriverFunctions__check_exists_by_xpath(driver,
                                                                           "//*[@class='css-4rbku5 css-18t94o4 css-901oao r-1fmj7o5 r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']")
        if is_exist == True:

            try:
                element_to_hover_over = driver.find_element_by_xpath("//a[@href='/" + username + "/followers']")

                number = element_to_hover_over.text
                number = HelperFunctions._HelperFunctions__format_number(number)

                return number
            except:
                element = driver.find_element_by_xpath("//a[@href='/" + username + "/followers']").text
                number = HelperFunctions._HelperFunctions__extract_number(element)

                return number
        else:
            return ""

    @staticmethod
    def __find_user_following_list(driver, username, following_number):
        username_list = []
        url = "https://twitter.com/" + username + "/following"
        try:
            DriverFunctions._DriverFunctions__open_new_tab(driver, url)

            while True:
                DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath",
                                                                             "//*[@class='css-1dbjc4n r-18u37iz r-1wbh5a2']")
                user_elements = driver.find_elements_by_xpath("//*[@class='css-1dbjc4n r-18u37iz r-1wbh5a2']")
                for element in user_elements:
                    if len(username_list) == following_number:
                        break
                    username = HelperFunctions._HelperFunctions__extract_username(element.text)
                    username_list.append(username)
                username_list = list(set(username_list))
                if len(username_list) >= following_number:
                    break
                DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME=0.5, SCROLL_NUMBER=1)

        except:
            username_list = []
        if len(driver.window_handles) > 2:
            DriverFunctions._DriverFunctions__close_current_tab(driver)
        return username_list

    @staticmethod
    def __find_user_follower_list(driver, username, follower_number):
        username_list = []
        url = "https://twitter.com/" + username + "/followers"

        try:
            DriverFunctions._DriverFunctions__open_new_tab(driver, url)
            while True:
                user_elements = driver.find_elements_by_xpath(
                    "//*[@class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l']")
                for element in user_elements:
                    if len(username_list) == follower_number:
                        break
                    username = HelperFunctions._HelperFunctions__extract_username(element.text)
                    username_list.append(username)
                username_list = list(set(username_list))
                if len(username_list) >= follower_number:
                    break
                DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME=0.5, SCROLL_NUMBER=1)
        except:
            username_list = []
        if len(driver.window_handles) > 2:
            DriverFunctions._DriverFunctions__close_current_tab(driver)
        return username_list

    @staticmethod
    def __find_replies(driver):
        DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME=0.5, SCROLL_NUMBER=1)

    @staticmethod
    def __find_profile_img(driver, username):

        profile_img_url = "twitter.com" + "/" + username + "/photo"
        # profile_img_url = driver.find_element_by_xpath(href).find_element_by_tag_name("img").get_attribute("src")

        return profile_img_url

    @staticmethod
    def __get_retweets(driver, url, login=True, limit=80):
        """
			post_link: the post that you wanted to get retweets
			login: will you login before get the retweets?
			limit: how many users you would like to get: MAX=80
		"""
        users_who_retweeted = []

        # if(login):
        # 	self.driver.get(Twitter_scraper.URL + "/login")
        # 	self.login(login_username, password)
        DriverFunctions._DriverFunctions__open_new_tab(driver, url)
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath",
                                                                     "//*[@class='css-18t94o4 css-1dbjc4n r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg']")
        for i in range(limit):
            element = driver.find_element_by_xpath(
                "//*[@class='css-18t94o4 css-1dbjc4n r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg']")
            users_who_retweeted.append(element.text.split('@')[1].split()[0])
            driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)
        DriverFunctions._DriverFunctions__close_current_tab(driver)
        print(users_who_retweeted)
        return users_who_retweeted

    @staticmethod
    def __get_likes(driver, url, login=True, limit=80):
        """
			post_link: the post that you wanted to get likes
			login: will you login before get the likes?
			limit: how many users you would like to get: MAX=80
		"""
        users_who_liked = []
        # if(login):
        # 	driver.get("https://www.twitter.com/" + "/login")
        # 	self.login(login_username, password)
        DriverFunctions._DriverFunctions__open_new_tab(driver, url)
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath",
                                                                     "//*[@class='css-18t94o4 css-1dbjc4n r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg']")
        for i in range(limit):
            element = driver.find_element_by_xpath(
                "//*[@class='css-18t94o4 css-1dbjc4n r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg']")
            users_who_liked.append(element.text.split('@')[1].split()[0])
            driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)
        DriverFunctions._DriverFunctions__close_current_tab(driver)
        print(users_who_liked)
        return users_who_liked

    @staticmethod
    def __get_quotes(driver, url, login=True, limit=80):
        """
			post_link: the post that you wanted to get retweets
			login: will you login before get the retweets?
			limit: how many users you would like to get: MAX=80
		"""
        users_who_quoted = []

        # if(login):
        # 	self.driver.get(Twitter_scraper.URL + "/login")
        # 	self.login(login_username, password)
        DriverFunctions._DriverFunctions__open_new_tab(driver, url)
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath",
                                                                     "//*[@class='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg']")

        # quote limitten azsa hata veriyo
        for i in range(limit):
            element = driver.find_element_by_xpath(
                "//*[@class='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg']")
            username = element.text.split('@')[1].split()[0]
            text = driver.find_element_by_xpath(
                "//*[@class='css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']").text
            quote_dict = {"username": username, "text": text}
            users_who_quoted.append(quote_dict)
            element_to_remove = driver.find_element_by_xpath(
                "//*[@class='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg']")
            driver.execute_script("""
			var element_to_remove = arguments[0];
			element_to_remove.parentNode.removeChild(element_to_remove);
			""", element_to_remove)
        DriverFunctions._DriverFunctions__close_current_tab(driver)
        print(users_who_quoted)
        return users_who_quoted

    @staticmethod
    def __find_post_details(driver, post_info_list):
        post_list = []
        for item in post_info_list:
            url = item["post_url"]
            date = item["post_date"]
            driver.get(url)

            username = url.split("/")[3]
            post_id = url.split("/")[-1]
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='article']")
            try:
                href = "/" + username + "/status/" + post_id + "/retweets"
                retweet_count = driver.find_element_by_xpath('//a[contains(@href, "%s")]' % href)
                retweet_count = HelperFunctions._HelperFunctions__format_number(retweet_count.text)
            # retweeter_list = Finder._Finder__get_retweets(driver, url+"/retweets", login = True, limit = 80)

            except NoSuchElementException:
                retweet_count = 0
                retweeter_list = []
            try:
                href = "/" + username + "/status/" + post_id + "/likes"
                like_count = driver.find_element_by_xpath('//a[contains(@href, "%s")]' % href)
                like_count = HelperFunctions._HelperFunctions__format_number(like_count.text)
                liker_list = Finder._Finder__get_likes(driver, url + "/likes", login=True, limit=10)
            except NoSuchElementException:
                like_count = 0
                liker_list = []
            try:
                href = "/retweets/with_comments"
                quote_count = driver.find_element_by_xpath('//a[contains(@href, "%s")]' % href)
                quote_count = HelperFunctions._HelperFunctions__format_number(quote_count.text)
                quotes_list = Finder.__get_quotes(driver, url + "/retweets/with_comments", login=True, limit=10)
            except NoSuchElementException:
                quote_count = 0
                quotes_list = []

            try:
                # eğer quotelarda hata olursa current tabi kapatmadan ilerlediği için post contenti falan bulamıyo
                post_content = driver.find_element_by_xpath(
                    "//*[@class='css-901oao r-1fmj7o5 r-1qd0xha r-1blvdjr r-16dba41 r-vrz42v r-bcqeeo r-bnwqim r-qvutc0']").text
                hashtags = HelperFunctions._HelperFunctions__find_hashtags(post_content)
                user_mentions = HelperFunctions._HelperFunctions__find_user_mentions(post_content)
                urls_in_post_text = HelperFunctions._HelperFunctions__find_urls(post_content)
            except:
                post_content = ""
                hashtags = []
                user_mentions = []
                urls_in_post_text = []
            try:
                shared_url = driver.find_element_by_xpath(
                    "//*[@class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1pi2tsx r-1ny4l3l r-1udh08x r-o7ynqc r-6416eg r-13qz1uu']").get_attribute(
                    "href")
            except:
                shared_url = ""
            try:
                img_urls = []
                img_elements = driver.find_elements_by_xpath("//*[@data-testid='tweetPhoto']/img")
                for img in img_elements:
                    img_urls.append(img.get_attribute("src"))
            except:
                img_urls = []
            try:
                video_link = driver.find_element_by_tag_name("video").get_attribute("src")
            except:
                video_link = ""

            post = {"post_id": post_id, "post_url": url, "post_date": date, "retweet_count": retweet_count,
                    "like_count": like_count, "username": username,
                    "quote_count": quote_count, "hashtags": hashtags, "post_content": post_content,
                    "user_mentions": user_mentions, "urls_in_post_text": urls_in_post_text,
                    "shared_url": shared_url, "img_urls": img_urls, "video_link": video_link,
                    "retweeter_list": [], "liker_list": liker_list, "quotes_list": quotes_list}
            post_list.append(post)
        return post_list

    @staticmethod
    def __find_user_profile(driver, username, is_detail=False):
        try:
            # driver.get("https://www.twitter.com/"+username)
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath",
                                                                         "//*[@class='css-901oao css-bfa6kz r-9ilb82 r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']")
            username = driver.find_element_by_xpath(
                "//*[@class='css-901oao css-bfa6kz r-9ilb82 r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']").text
            username = HelperFunctions._HelperFunctions__extract_username(username)
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath",
                                                                         "//*[@class = 'css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs']")
            screen_name = driver.find_element_by_xpath("//*[@class = 'css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs']").text
            profile_img_url = Finder._Finder__find_profile_img(driver, username)
            user_description = Finder._Finder__find_user_description(driver)
            # gerek olmayabilir???
            user_website = Finder._Finder__find_user_website(driver)
            join_date = Finder._Finder__find_user_join_date(driver)
            following_number = Finder._Finder__find_user_following_number(driver, username)
            follower_number = Finder._Finder__find_user_follower_number(driver, username)
            if is_detail == True:
                following_list = Finder._Finder__find_user_following_list(driver, username, following_number)
                follower_list = Finder._Finder__find_user_follower_list(driver, username, follower_number)
            else:
                follower_list = []
                following_list = []
            post_number = driver.find_element_by_xpath(
                "//div[@class='css-901oao css-bfa6kz r-9ilb82 r-1qd0xha r-n6v787 r-16dba41 r-1cwl3u0 r-bcqeeo r-qvutc0']").text
            post_number = HelperFunctions._HelperFunctions__format_number(post_number)
            user = {"username": username, "screen_name": screen_name, "user_description": user_description,
                    "user_website": user_website, "join_date": join_date, "follower_number": following_number,
                    "following_number": follower_number, "following_number": following_number,
                    "follower_list": follower_list, "following_list": following_list, "post_number": post_number,
                    "profile_img_url": profile_img_url
                    }
            return user
        except:
            raise

    @staticmethod
    def __find_posts(driver, username, post_number):
        post_info_list = []
        post_reply_list = []
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='article']")
        count = 0
        while True:

            post_elements = driver.find_elements_by_xpath('//*[@data-testid="tweet"]')

            for post in post_elements:
                try:
                    try:
                        post_url = post.find_elements_by_tag_name("a")[2].get_attribute("href")
                    except:
                        post_url = post.find_element_by_xpath("//*[@class = 'css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']")

                    post_date = post.find_element_by_tag_name("time").get_attribute("datetime")
                    post_info = {"post_url": post_url, "post_date": post_date}
                    if username not in post_url:
                       post_reply_list.append(post_info)
                       post_reply_list = list({x['post_url']: x for x in post_reply_list}.values())
                    else:
                        post_info_list.append(post_info)
                    count += 1

                    if DriverFunctions._DriverFunctions__check_exists_by_xpath(driver, ".//*[@class='css-1dbjc4n r-gu4em3 r-16y2uox r-1jgb5lz r-14gqq1x r-m5arl1']"):
                        next_post = driver.find_elements_by_xpath('.//*[@data-testid="tweet"]')[count]
                        post_url = next_post.find_elements_by_tag_name("a")[2].get_attribute("href")
                        # if username not in post_url:
                        #   continue
                        post_date = next_post.find_element_by_tag_name("time").get_attribute("datetime")
                        post_info = {"post_url": post_url, "post_date": post_date, "reply_dict":post_reply_list}
                        post_info_list.append(post_info)
                    if len(post_info_list) >= post_number:
                        break
                except:
                    continue
            post_info_list = list({x['post_url']: x for x in post_info_list}.values())
            if len(post_info_list) >= post_number:
                break
            DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME=0.5, SCROLL_NUMBER=1)
            time.sleep(3)
        post_info_list.append(post_reply_list)
        posts = Finder._Finder__find_post_details(driver, post_info_list)
        return posts

    @staticmethod
    def __find_hashtag_posts(driver, post_number=10):
        post_info_list = []
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='article']")

        while True:

            post_elements = driver.find_elements_by_xpath(
                '//a[@class="css-4rbku5 css-18t94o4 css-901oao r-9ilb82 r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0"]')
            for post in post_elements:
                try:

                    post_url = post.get_attribute("href")
                    post_date = post.find_element_by_tag_name("time").get_attribute("datetime")
                    post_info = {"post_url": post_url, "post_date": post_date}
                    post_info_list.append(post_info)
                except:
                    continue
            post_info_list = list({x['post_url']: x for x in post_info_list}.values())
            if len(post_info_list) >= post_number:
                break
            DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME=0.5, SCROLL_NUMBER=1)
            time.sleep(3)
        posts = Finder._Finder__find_post_details(driver, post_info_list[:post_number])
        return posts


"""
1)postu retweet edenlerin popupında scroll down yapamıyorum

2)postu likelayanların popupında scroll down yapamıyorum

3)postları alırken article taglerini bulmada sorun oluyor

4)post replyları alamıyorum

5)retweetler ayrı bi şekilde alınsın

6)article tagiyle postları toplarken bazı postları atlıyo

7)quotelar alınacak


"""
