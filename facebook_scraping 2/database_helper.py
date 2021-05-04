from driver_functions import DriverFunctions
class DatabaseHelper:

	@staticmethod
	def __create_detailed_user(app, facebook, username):
		p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app,facebook,username)
		profile = facebook.search_user(username, get_posts = False, detail = True)
		if profile != {}:
			profile_url = profile["profile_url"]
			user_work_and_education = profile["user_work_and_education"]
			user_about_places = profile["user_about_places"]
			user_friends = profile["user_friends"]
			liked_sport_pages = profile["user_liked_sport_pages"]
			liked_music_pages = profile["user_liked_music_pages"]
			liked_tv_pages = profile["user_liked_tv_pages"]
			liked_book_pages = profile["user_liked_book_pages"]
			liked_movie_pages = profile["user_liked_movie_pages"]

			if user_work_and_education["company_list"] != []:
				for item in user_work_and_education["company_list"]:
					app.create_company(item["company_name"])
					app.create_location(item["location"])
					app.create_company_located_in_relationship(item["company_name"], item["location"])
					app.create_worked_relationship(item["company_name"],profile_url, item["position"], item["duration"])

			if user_work_and_education["education_list"] != []:
				for item in user_work_and_education["education_list"]:
					app.create_university(item["university_name"])
					app.create_studied_in_relationship(item["university_name"], item["faculty"], item["grad_year"], profile_url)



			if liked_movie_pages != []:
				for item in liked_movie_pages:
					DatabaseHelper._DatabaseHelper__create_page_helper(app,facebook,item["page_url"],search_post =  False)
					app.create_like_page_relationship(profile_url, item["page_url"])

			if liked_sport_pages != []:
				for item in liked_sport_pages:
					page_name = item["page_url"].split("/")[3]
					DatabaseHelper._DatabaseHelper__create_page_helper(app,facebook,item["page_url"], search_post =  False)
					app.create_like_page_relationship(profile_url, item["page_url"])

			if liked_music_pages != []:
				for item in liked_music_pages:
					page_name = item["page_url"].split("/")[3]
					DatabaseHelper._DatabaseHelper__create_page_helper(app,facebook,item["page_url"], search_post =  False)
					app.create_like_page_relationship(profile_url, item["page_url"])

			if liked_tv_pages != []:
				for item in liked_tv_pages:
					page_name = item["page_url"].split("/")[3]
					DatabaseHelper._DatabaseHelper__create_page_helper(app,facebook,item["page_url"], search_post =  False)
					app.create_like_page_relationship(profile_url, item["page_url"])

			if liked_book_pages != []:
				for item in liked_book_pages:
					page_name = item["page_url"].split("/")[3]
					DatabaseHelper._DatabaseHelper__create_page_helper(app,facebook,item["page_url"], search_post =  False)
					app.create_like_page_relationship(profile_url, item["page_url"])
			count = 0
			if user_friends != []:
				for item in user_friends:
					search_name = item["username"]
					p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app,facebook,search_name, get_posts = False, detail = False)
					app.create_friends_with_relationship(profile_url,item["user_url"]+"/")
					count += 1
					if count ==5:
						break

			if user_about_places["live_in"] != []:
					app.create_location(user_about_places["live_in"])
					app.create_live_in_relationship(profile_url, user_about_places["live_in"] )
			if user_about_places["born_in"] != "":
					app.create_location(user_about_places["born_in"])
					app.create_live_in_relationship(profile_url, user_about_places["born_in"] )

	@staticmethod
	def __create_user_helper(app, facebook, search_string, get_posts = False, detail = False):
		if "www" and "profile" in search_string:
			profile_url = search_string
			username = "profile.php?" +search_string.split('?')[1].split("&")[0]

		elif "www" in search_string:
			username = search_string.split('/')[3].split("?")[0]
			profile_url = search_string.split("?")[0] + "/"
		else:
			profile_url = "https://www.facebook.com/" + search_string + "/"
			username = search_string


		if len(app.find_node("FacebookUser { profile_url: '" +profile_url+"' }")) == 0 :
			profile = facebook.search_user(username, get_posts, detail)
			if profile != {}:
				screen_name = profile["screen_name"]
				username = profile["username"]
				profile_url = profile["profile_url"]
				bio = profile["user_description"]
				profile_img_url = profile["profile_img_url"]
				app.create_user(username,profile_url, screen_name, profile_img_url, bio)
			
		return profile_url

	@staticmethod
	def __create_page_helper(app, facebook, username, search_post =  False):
		if "www" not in username:
			page_url = "https://www.facebook.com/"+username+"/"
		elif "pages" in username:
			page_url = username
			username = "pages/" + username.split('/')[4] + "/" + username.split("/")[5]
		else:
			page_url = username
			username = username.split('/')[3]
		if len(app.find_node("FacebookPage { page_url: '" +page_url+"' }")) == 0 :
			page = facebook.search_page(username, search_post)
			# DriverFunctions._DriverFunctions__close_current_tab(facebook.driver)
			if page["screen_name"] != "":
				page_name = page["screen_name"]
				username = page_name
				category = page["category"]
				liked_number = page["liked_number"]
				# profile_img_url = page["profile_img_url"]
				follower_number = page["follower_number"]
				bio = page["bio"]
				app.create_page(page_url, username, page_name, category, liked_number, follower_number, bio)
			if search_post == True and page["user_posts"] != []:
				for post in page["user_posts"]:
					post_url = DatabaseHelper._DatabaseHelper__create_post(facebook, app, post)
					app.create_page_posted_relationship(page_url, post_url)
		if len(app.find_node("FacebookPage { page_url: '" +page_url+"' }")) == 1 :
			page = facebook.search_page(username, search_post)

			if search_post == True and page["user_posts"] != []:
				for post in page["user_posts"]:
					post_url = DatabaseHelper._DatabaseHelper__create_post(facebook, app, post)
					app.create_page_posted_relationship(page_url, post_url)
	@staticmethod
	def __create_post(facebook, app, post):
		if post != None:
			post_url = post["post_url"]
			username = post["username"]
			post_date = post["post_date"]
			content_text = post["content_text"]
			hashtags_in_content = post["hashtags_in_content"]
			mentions_in_content = post["mentions_in_content"]
			shared_url = post["shared_url"]
			img_url_list = post["img_url_list"]
			video_url = post["video_url"]
			like_dict = post["like_dict"]
			sad_dict = post["sad_dict"]
			wow_dict = post["wow_dict"]
			care_dict = post["care_dict"]
			haha_dict = post["haha_dict"]
			angry_dict = post["angry_dict"]
			love_dict = post["love_dict"]
			comment_dict = post["comment_dict"]
			profile_url = post_url.split("posts")[0]
			if len(app.find_node("FacebookPost { post_url: '" +post_url+"' }")) == 0 :
				app.create_post(post_url ,post_date, content_text, img_url_list, video_url)
			
			if hashtags_in_content !=  []:
				for h in hashtags_in_content:
					app.create_hashtag(h)
					app.create_hashtagged_post_relationship(post_url, h)
			if mentions_in_content != []:
				for m in mentions_in_content:
					try:
						p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, username, get_posts = False, detail = False)
						app.create_mentioned_in_post_relationship(post_url, m)
					except:
						continue
			if like_dict["like_list"] != []:
				for l in like_dict["like_list"]:
					try:
						p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, l["like_user_profile_url"],get_posts = False, detail = False)
						app.create_like_reaction_to_post_relationship(post_url, p_url)
					except:
						continue
			if sad_dict["sad_list"] != []:
				for s in sad_dict["sad_list"]:
					
					p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, s["sad_user_profile_url"],get_posts = False, detail = False)
					app.create_love_reaction_to_post_relationship(post_url, s["sad_user_profile_url"])
			if wow_dict["wow_list"] != []:
				for w in wow_dict["wow_list"]:
					
					p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, w["wow_user_profile_url"],get_posts = False, detail = False)
					app.create_wow_reaction_to_post_relationship(post_url,  w["wow_user_profile_url"])
			if care_dict["care_list"] != []:
				for c in care_dict["care_list"]:
					
					p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, c["care_user_profile_url"],get_posts = False, detail = False)
					app.create_care_reaction_to_post_relationship(post_url, c["care_user_profile_url"])
			if haha_dict["haha_list"] != []:
				for h in haha_dict["haha_list"]:
					
					p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, h["haha_user_profile_url"],get_posts = False, detail = False)
					app.create_haha_reaction_to_post_relationship(post_url, h["haha_user_profile_url"])
			if angry_dict["angry_list"] != []:
				for a in angry_dict["angry_list"]:
					
					p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, a["angry_user_profile_url"],get_posts = False, detail = False)
					app.create_angry_reaction_to_post_relationship(post_url, a["angry_user_profile_url"])
			if love_dict["love_list"] != []:
				for l in love_dict["love_list"]:
					
					p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, l["love_user_profile_url"],get_posts = False, detail = False)
					app.create_love_reaction_to_post_relationship(post_url, l["love_user_profile_url"])

			if comment_dict != []:
				for c in comment_dict:
					c_user_url = c["user_url"].split("?")[0]+"/"
					c_text = c["text"]
					p_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, c_user_url,get_posts = False, detail = False)
	
					app.create_comment(c_text)
					app.create_commented_relationship(c_text, c_user_url)
					app.create_commented_on_relationship(c_text, post_url)
					if c["reply_list"] != []:
						for r in c["reply_list"]:
							r_user_url = r["user_profile_url"].split("?")[0]
							r_text = r["text"]
							r_url = DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, r_user_url, get_posts = False, detail = False)
							app.create_comment(r_text)
							app.create_commented_relationship(r_text, r_user_url)
							app.create_replied_on_relationship(r_text, c_text)
			return post_url



	@staticmethod
	def __find_posts(facebook,app,username):
		DatabaseHelper._DatabaseHelper__create_user_helper(app, facebook, username)
		profile = facebook.search_user(username, get_posts = True, detail = False)
		post_list = profile["user_posts"]
		for post in post_list:
			post_url = DatabaseHelper._DatabaseHelper__create_post(facebook, app, post)
			profile_url = post_url.split("posts")[0]
			app.create_posted_relationship(profile_url, post_url)
			# DriverFunctions._DriverFunctions__close_current_tab(facebook.driver)