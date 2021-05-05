from helper import HelperFunctions
from selenium.common.exceptions import NoSuchElementException
from driver_functions import DriverFunctions
import time


class Finder():
    """
	Holds the collections of methods that finds element of the instagram posts using selenium's 
	webdriver's methods  
	"""

    @staticmethod
    def __find_post_urls(driver, post_number=None):
        """ finds URL of the post, then extracts link from that URL and returns it """

        xpath = "//*[@class='v1Nh3 kIKUG  _bz0w']"
        post_url_list = []
        old_len = 0
        while True:
            try:
                # aim is to find post url
                # after finding that element, get it's href value and pass it to different method
                # that extracts post_id from that href

                DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "class", "_9AhH0")
                post_url_elements = driver.find_elements_by_xpath(xpath)
                for element in post_url_elements:
                    post_url = element.find_element_by_tag_name("a").get_attribute("href")
                    post_url_list.append(post_url)
                post_url_list = list(set(post_url_list))
                new_len = len(post_url_list)
                if new_len == old_len:
                    break
                old_len = new_len

                if post_number != None and len(post_url_list) >= post_number:
                    break

                DriverFunctions._DriverFunctions__scroll_down(driver, SCROLL_PAUSE_TIME=0.5,
                                                              SCROLL_NUMBER=1)  # if scroll_number is None, page will scroll to the end
            except:
                post_url_list = []
        return post_url_list

    @staticmethod
    def __find_post_likes(driver):
        """ if the post is photo, find like number and all likers of the photo. """
        try:

            el_likes = driver.find_element_by_class_name("zV_Nj")
            likes = el_likes.text
            likes = likes.split()[0]
            like_num = int(likes.replace(",", "").replace(".", "")) if likes is not None else 0
            likers = Finder._Finder__find_post_likers(driver)
        except:
            like_num = 0
            likers = []
        driver.find_element_by_xpath("//*[@aria-label='Close']").click()
        return {"like_num": like_num, "likers": likers}

    @staticmethod
    def __find_post_comments(driver):
        """
			get all comments of post. in order to get all comments first click all load more buttons and see 
			replies buttons to make every comment visible. then get every comment with its replies.
		"""

        comment_list = []
        comment_blocks = driver.find_elements_by_class_name('Mr508')
        for item in comment_blocks:
            comment = {}
            reply_list = []
            try:

                text = item.find_elements_by_tag_name("span")[1].text
                user = item.find_element_by_tag_name("a").get_attribute("href")
                user = user.split('/')[3]
                comment["username"] = user
                comment["text"] = text
                comment_list.append(comment)
            except:
                continue
            try:
                try:
                    load_replies = driver.find_element_by_xpath("//*[@class='sqdOP yWX7d    y3zKF     ']")
                    # print("Found {}".format(str(load_replies)))
                    load_replies.click()
                    time.sleep(1.5)

                except Exception:
                    # print(e)
                    pass

                replies = item.find_elements_by_class_name('TCSYW')
                if replies == []:
                    raise Exception
                for reply in replies:
                    reply_dict = {}
                    r_user = reply.find_element_by_tag_name("a").get_attribute("href")
                    r_user = r_user.split('/')[3]
                    r_text = reply.find_elements_by_tag_name("span")[2].text
                    r_text = r_text.split(' ', 1)[1]
                    reply_dict["username"] = r_user
                    reply_dict["text"] = r_text
                    reply_list.append(reply_dict)
                    comment["reply_dict"] = reply_list
                    comment_list.append(comment)
            except:
                reply_dict = {}
                reply_list.append(reply_dict)
                comment["reply_dict"] = reply_list
        return comment_list

    @staticmethod
    def __find_datetime(driver):
        """ find the posted time """

        ele_datetime = driver.find_element_by_css_selector(".eo2As .c-Yi7 ._1o9PC")
        datetime = ele_datetime.get_attribute("datetime")
        datetime = HelperFunctions._HelperFunctions__get_datetime(datetime)
        return datetime

    @staticmethod
    def __find_caption(driver):
        """ find the user caption of the post with hashtag and mentions list in caption """

        ele_comments = driver.find_elements_by_css_selector(".eo2As .gElp9")

        if len(ele_comments) > 0:

            temp_element = ele_comments[0].find_elements_by_css_selector("span")

            for element in temp_element:

                if element.text not in ['Verified', '']:
                    caption = element.text

            mentions = HelperFunctions._HelperFunctions__get_parsed_mentions(caption)
            hashtags = HelperFunctions._HelperFunctions__get_parsed_hashtags(caption)

            return {"caption": caption, "mentions": mentions, "hashtags": hashtags}

    @staticmethod
    def __find_video_like_num(driver):
        """ if the post is video return seen number and liked number"""

        el_see_likes = driver.find_element_by_css_selector(".vcOH2")
        el_plays = driver.find_element_by_css_selector(".vcOH2 > span")
        video_play_num = el_plays.text

        el_see_likes.click()
        el_likes = driver.find_element_by_css_selector(".vJRqr > span")
        video_like_num = el_likes.text

        return {"video_play_number": video_play_num, "video_like_num": video_like_num}

    @staticmethod
    def __find_post_likers(driver):
        """ find all users that liked the post"""

        liker_list = []
        current_url = driver.current_url
        post_id = current_url.split("/")[4]
        href = "//*[@href='/p/" + post_id + "/liked_by/']"
        # print(post_id)
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", href)
        time.sleep(3)
        driver.find_element_by_xpath(href).click()
        # DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='dialog']" )
        time.sleep(3)
        try:
            height = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/div").value_of_css_property(
                "padding-top")
        except:

            height = driver.find_element_by_xpath(
                "//*[@class='                     Igw0E     IwRSH      eGOV_        vwCYk                                                                            i0EQd                                   ']/div/div").value_of_css_property(
                "padding-top")
        match = False
        # scroll down until all likers are get
        while match == False:
            lastHeight = height
            elements = driver.find_elements_by_xpath("//*[@id]/div/span/a")
            for element in elements:
                if element.get_attribute('title') not in liker_list:
                    liker_list.append(element.get_attribute('title'))
            driver.execute_script("return arguments[0].scrollIntoView();", elements[-1])
            time.sleep(1)
            height = driver.find_element_by_xpath(
                "//*[@class='                     Igw0E     IwRSH      eGOV_        vwCYk                                                                            i0EQd                                   ']/div/div").value_of_css_property(
                "padding-top")
            if lastHeight == height:
                match = True
        # close_element = driver.find_element_by_xpath('//*[@aria-label="Close"]').click()
        return liker_list

    @staticmethod
    def __find_followers(driver, follower_num):
        """ find all followers of user """
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "class", "-nal3 ")

        x = driver.find_elements_by_class_name("-nal3 ")[1]
        x.click()
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "class", "_1XyCr")
        DriverFunctions._DriverFunctions__scroll_down_pop_up_window(driver, SCROLL_PAUSE_TIME=0.8, NUMBER=follower_num)
        follower_elements = driver.find_elements_by_xpath("//*[@class='FPmhX notranslate  _0imsa ']")
        follower_list = []
        for element in follower_elements:
            follower_list.append(element.text)
        driver.find_element_by_xpath("//*[@aria-label='Close']").click()
        return follower_list

    @staticmethod
    def __find_followings(driver, following_num):
        """ find all users that user is following """
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath",
                                                                     '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]')

        x = driver.find_elements_by_class_name("-nal3 ")[2]
        x.click()
        if DriverFunctions._DriverFunctions__check_exists_by_class_name(driver, "_1XyCr"):
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "class", "_1XyCr")
            DriverFunctions._DriverFunctions__scroll_down_pop_up_window(driver, SCROLL_PAUSE_TIME=0.5,
                                                                        NUMBER=following_num)
            following_elements = driver.find_elements_by_xpath("//*[@class='FPmhX notranslate  _0imsa ']")
            following_list = []
            for element in following_elements:
                following_list.append(element.text)
            driver.find_element_by_xpath("//*[@aria-label='Close']").click()
            return following_list
        else:
            return []

    @staticmethod
    def __find_tagged_posts(driver, username, post_number):
        """
			get tagged posts of given username. wanted post number can be given. if does not given
			function will return all posts that the user is tagged.
		"""

        tagged_posts_url = "https://www.instagram.com/" + username + "/tagged"
        DriverFunctions._DriverFunctions__open_new_tab(driver, tagged_posts_url)
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "class", "_2z6nI")

        post_url_list = Finder._Finder__find_post_urls(driver, post_number)  # find all posts
        if len(driver.window_handles) > 1:
            DriverFunctions._DriverFunctions__close_current_tab(driver)
        result_list = []
        if post_number == None:
            for post_url in post_url_list:
                result_list.append(Finder._Finder__get_post(driver, post_url))


        else:
            for post_url in post_url_list[:post_number]:
                result_list.append(Finder._Finder__get_post(driver, post_url))

        return result_list

    @staticmethod
    def __find_profile_statistics(driver):
        """
			this functions finds post number, follower number, and following number of user.
		"""
        time.sleep(3)
        post_num = driver.find_elements_by_css_selector(".g47SY")[0]
        follower_num = driver.find_elements_by_css_selector(".g47SY")[1]
        following_num = driver.find_elements_by_css_selector(".g47SY")[2]

        # if the number is large, exact number is in title attribute, so we need to check whether it is
        # exist.

        if post_num.get_attribute("title") != '':
            post_num = post_num.get_attribute("title")
        else:
            post_num = post_num.text

        if follower_num.get_attribute("title") != '':
            follower_num = follower_num.get_attribute("title")
        else:
            follower_num = follower_num.text

        if following_num.get_attribute("title") != '':
            following_num = following_num.get_attribute("title")
        else:
            following_num = following_num.text

        post_num = HelperFunctions._HelperFunctions__get_int(post_num)
        follower_num = HelperFunctions._HelperFunctions__get_int(follower_num)
        following_num = HelperFunctions._HelperFunctions__get_int(following_num)

        return post_num, follower_num, following_num

    @staticmethod
    def __is_video(driver):
        is_video = DriverFunctions._DriverFunctions__check_exists_by_tag_name(driver, "video")
        return is_video

    @staticmethod
    def __get_post(driver, post_url):
        """
			get post details for given post url. If the post is video then it will find like number
			and how many times seen. If it is photo it will find like number and liker list of post.
			Other details of post are comment dictionary, image alt description, posted date and caption
			dictionary which includes mentions and hashtags in post description. Also comment dictionary
			includes replies of comments. 
		"""
        DriverFunctions._DriverFunctions__open_new_tab(driver, post_url)
        DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "xpath", "//*[@role='main']")

        is_video = Finder._Finder__is_video(driver)
        if is_video == True:
            likes = Finder._Finder__find_video_like_num(driver)

        else:
            likes = Finder._Finder__find_post_likes(driver)

        comment_dict = Finder._Finder__find_post_comments(driver) # 2 kere ayni seyi aliyor
        img_element = driver.find_element_by_css_selector(".KL4Bh img")
        img_desc = img_element.get_attribute("alt")
        caption_dict = Finder._Finder__find_caption(driver)
        datetime = Finder._Finder__find_datetime(driver)
        username = driver.find_element_by_xpath("//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']").text

        if len(driver.window_handles) > 1:
            DriverFunctions._DriverFunctions__close_current_tab(driver)
        result_dict = {"post_url": post_url, "datetime": datetime, "img_description": img_desc,
                       "caption": caption_dict, "comment_dict": comment_dict, "is_video": is_video,
                       "likes_dict": likes, "username": username}
        return result_dict

    @staticmethod
    def __get_posts(driver, post_number):
        """get elements of search result of posts and add them to data_dict"""

        time.sleep(3)
        try:
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "class", "_2z6nI")
        except:
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "class", "EZdmt")

        post_url_list = Finder._Finder__find_post_urls(driver, post_number)  # find all posts
        result_list = []

        # print(post_number)
        for post_url in post_url_list[:int(post_number)]:
            result_list.append(Finder._Finder__get_post(driver, post_url))
        return result_list

    @staticmethod
    def __find_user_profile(driver, username, is_search_post):

        """
			Find user details like screenname, user description, profile img url, post number, follower number,
			following number. If function is not called from find posts function, it will return more detailed
			info about user such as following user list, follower user list, tagged posts.
		"""

        # try to get screen name of user, if does not exist return empty string
        try:
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "css_selector", ".rhpdm")
            name = driver.find_element_by_css_selector(".rhpdm").text
        except:
            name = " "

        # try to get description of user profile, if does not exist return empty string
        try:
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "css_selector", ".-vDIg span")
            desc = driver.find_element_by_css_selector(".-vDIg span").text
        except:
            desc = " "

        # try to get profile image url, if does not exist return empty string
        try:
            DriverFunctions._DriverFunctions__wait_for_element_to_appear(driver, "css_selector", "._6q-tv")
            photo = driver.find_element_by_css_selector("._6q-tv").get_attribute("src")
        except:
            photo = " "

        post_num, follower_num, following_num = Finder._Finder__find_profile_statistics(driver)
        follower_list = []
        following_list = []
        tagged_post_list = []
        tagged_post_num = 0

        # check if the profile is public or not, if it is not public we cannot get follower, following,
        # and tagged list. Also we dont want to get users every detail when we are searching posts
        check_profile_posts = DriverFunctions._DriverFunctions__check_exists_by_class_name(driver, "_9AhH0")
        if is_search_post == False and check_profile_posts == True:
            follower_list = Finder._Finder__find_followers(driver, follower_num)
            following_list = Finder._Finder__find_followings(driver, following_num)
            tagged_post_list = Finder._Finder__find_tagged_posts(driver, username, None)
            tagged_post_num = len(tagged_post_list)

        # return the result dictionary
        result_dict = {"name": name, "desc": desc,
                       "photo_url": photo, "post_num": post_num, "follower_num": follower_num,
                       "following_num": following_num, "follower_list": follower_list, "following_list": following_list,
                       "tagged_post_num": tagged_post_num, "tagged_post_list": tagged_post_list}
        return result_dict


"""
todo: 
1)yorumları beğenenler kişileri al:
	her bir Mr508 classında button[@class='FH9sR'] leri al, bu listeden
	sıfırıncı eleman yoruma gelen beğeni sayısını ifade ediyor. Buna tıklayıp
	yorumu likelayanları al.

2)scroll number direk userdan alınabilecek şekilde parametrik olsun mu??

3)bu fonksiyonları direk db ile bağlayacaksak getlerde ufak değişiklikler lazım.
Mesela given username dbde var mı diye kontrol et, yoksa al falan gibi.

4)eğer post video ise bu videonun linki eklenecek?? ---video linki yok sanırım

"""
