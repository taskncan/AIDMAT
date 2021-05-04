from driver_functions import DriverFunctions


class DatabaseHelper:

    @staticmethod
    def __create_detailed_user(app, instagram, username):
        DatabaseHelper._DatabaseHelper__create_user_helper(app, instagram, username)
        profile = instagram.get_user_profile(username, False)
        follower_list = profile["follower_list"]
        following_list = profile["following_list"]
        tagged_post_list = profile["tagged_post_list"]
        if follower_list != []:
            for follower in follower_list:
                DatabaseHelper._DatabaseHelper__create_user_helper(app, instagram, follower)
                app.create_follow_relationship(follower, username)
        if following_list != []:
            for following in following_list:
                DatabaseHelper._DatabaseHelper__create_user_helper(app, instagram, following)
                app.create_follow_relationship(username, following)
        if tagged_post_list != []:
            for post in tagged_post_list:
                DatabaseHelper._DatabaseHelper__create_post(instagram, app, post)
                DriverFunctions._DriverFunctions__close_current_tab(instagram.driver)
                app.create_tagged_in_post_relationship(username, post)

    @staticmethod
    def __create_user_helper(app, instagram, username):
        if len(app.find_node("InstagramUser { username: '" + username + "' }")) == 0:
            profile = instagram.get_user_profile(username, True)
            DriverFunctions._DriverFunctions__close_current_tab(instagram.driver)
            p_name = profile["name"]
            p_bio = profile["desc"]
            p_profil_img_url = profile["photo_url"]
            p_post_num = profile["post_num"]
            p_follower_num = profile["follower_num"]
            p_following_num = profile["following_num"]
            app.create_user(username, p_name, p_profil_img_url, p_post_num, p_follower_num, p_following_num, p_bio)

    @staticmethod
    def __create_post(instagram, app, post):

        post_url = post["post_url"]
        date = post["datetime"]
        try:
            like_num = post["likes_dict"]["like_num"]
        except:
            like_num = post["likes_dict"]["video_like_num"]
        img_desc = post["img_description"]
        if post["caption"] != None:
            caption = post["caption"]["caption"]
            hashtag = post["caption"]["hashtags"]
            mention = post["caption"]["mentions"]
        else:
            caption = ""
            hashtag = []
            mention = []

        username = post["username"]
        try:
            liker_list = post["likes_dict"]["likers"]
        except:
            liker_list = []
        comment_dict = post["comment_dict"]

        app.create_post(post_url, caption, img_desc, date, like_num)
        app.create_posted_relationship(username, post_url)
        if hashtag != None and hashtag != []:
            for h in hashtag:
                app.create_hashtag(h)
                app.create_hashtagged_post_relationship(post_url, h)
        if mention != None and mention != []:
            for m in mention:
                try:
                    DatabaseHelper._DatabaseHelper__create_user_helper(app, instagram, m)
                    app.create_mentioned_in_post_relationship(post_url, m)
                except:
                    continue
        if liker_list != []:
            for l in liker_list:
                DatabaseHelper._DatabaseHelper__create_user_helper(app, instagram, l)
                app.create_liked_post_relationship(post_url, l)
        if comment_dict != []:
            for c in comment_dict:
                c_username = c["username"]
                c_text = c["text"]
                DatabaseHelper._DatabaseHelper__create_user_helper(app, instagram, c_username)

                app.create_comment(c_text)
                app.create_commented_relationship(c_text, c_username)
                app.create_commented_on_relationship(c_text, post_url)
                if c["reply_dict"] != [{}]:
                    for r in c["reply_dict"]:
                        if r != {}:
                            r_username = r["username"]
                            r_text = r["text"]
                            DatabaseHelper._DatabaseHelper__create_user_helper(app, instagram, r_username)
                            app.create_comment(r_text)
                            app.create_commented_relationship(r_text, r_username)
                            app.create_replied_on_relationship(r_text, c_text)

    @staticmethod
    def __find_posts(instagram, app, username, post_num):
        DatabaseHelper._DatabaseHelper__create_user_helper(app, instagram, username)
        post_list = instagram.get_user_posts(username, post_num)
        for post in post_list:
            DatabaseHelper._DatabaseHelper__create_post(instagram, app, post)
            if (len(instagram.driver.window_handles) > 1):
                DriverFunctions._DriverFunctions__close_current_tab(instagram.driver)

    @staticmethod
    def __find_hashtag_posts(instagram, app, hashtag, post_num):
        post_list = instagram.get_hashtag_results(hashtag, post_num)
        for post in post_list:
            DatabaseHelper._DatabaseHelper__create_post(instagram, app, post)
            if (len(instagram.driver.window_handles) > 1):
                DriverFunctions._DriverFunctions__close_current_tab(instagram.driver)
