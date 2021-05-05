from element_finder import Finder


class DatabaseHelper():
    @staticmethod
    def __create_post(app, twitter, post):

        post_id = post["post_id"]
        post_url = post["post_url"]
        post_date = post["post_date"]
        retweet_count = post["retweet_count"]
        like_count = post["like_count"]
        quote_count = post["quote_count"]
        username = post["username"]
        hashtags = post["hashtags"]
        post_content = post["post_content"]
        user_mentions = post["user_mentions"]
        urls_in_post_text = post["urls_in_post_text"]
        shared_url = post["shared_url"]
        img_urls = post["img_urls"]
        video_link = post["video_link"]
        retweeter_list = post["retweeter_list"]
        quotes_list = post["quotes_list"]
        liker_list = post["liker_list"]
        reply_list = post["reply_dict"]

        app.create_post(post_id, post_url, post_date, username, retweet_count, like_count, quote_count, post_content,
                        img_urls, shared_url)
        app.create_posted_relationship(username, post_id)
        if reply_list != []:
                replies = twitter.get_user_posts_with_url(reply_list)
                for item in replies:
                    r_post_id = item["post_id"]
                    r_post_url = item["post_url"]
                    r_post_date = item["post_date"]
                    r_retweet_count = item["retweet_count"]
                    r_like_count = item["like_count"]
                    r_quote_count = item["quote_count"]
                    r_username = item["username"]
                    r_hashtags = item["hashtags"]
                    r_post_content = item["post_content"]
                    r_user_mentions = item["user_mentions"]
                    r_urls_in_post_text = item["urls_in_post_text"]
                    r_shared_url = item["shared_url"]
                    r_img_urls = item["img_urls"]
                    r_video_link = item["video_link"]
                    r_retweeter_list = item["retweeter_list"]
                    r_quotes_list = item["quotes_list"]
                    r_liker_list = item["liker_list"]
                    r_reply_list = item["reply_dict"]
                    if app.find_user(username) == []:
                        DatabaseHelper._DatabaseHelper__create_user(app, twitter, username, is_detail=False)

                    app.create_post(r_post_id, r_post_url, r_post_date, r_username, r_retweet_count, r_like_count, r_quote_count, r_post_content,r_img_urls, r_shared_url)
                    app.create_replied_post_relationship(post_id, r_post_id)

        if hashtags != []:
            for h in hashtags:
                app.create_hashtag(h)
                app.create_hashtagged_post_relationship(post_id, h)

        if user_mentions != []:
            for m in user_mentions:
                m_username = DatabaseHelper._DatabaseHelper__create_user(app, twitter, m, is_detail=False)
                app.create_mentioned_in_post(post_id, m_username)

        if retweeter_list != []:
            for r in retweeter_list:
                r_username = DatabaseHelper._DatabaseHelper__create_user(app, twitter, r, is_detail=False)
                app.create_retweeted_post_relationship(post_id, r_username)

        if liker_list != []:
            for l in liker_list:
                l_username = DatabaseHelper._DatabaseHelper__create_user(app, twitter, l, is_detail=False)
                app.create_liked_post_relationship(post_id, l_username)

        if quotes_list != []:
            for q in quotes_list:
                q_username = q["username"]
                q_text = q["text"]

                l_username = DatabaseHelper._DatabaseHelper__create_user(app, twitter, q_username, is_detail=False)
                app.create_quoted_post_relationship(post_id, l_username)

    @staticmethod
    def __following_helper(app, twitter, username, username_list):
        if username_list != []:
            for f in username_list:
                f_username = DatabaseHelper._DatabaseHelper__create_user(app, twitter, f, is_detail=False)
                app.create_following_relationship(username, f_username)

    @staticmethod
    def __follower_helper(app, twitter, username, username_list):
        if username_list != []:
            for f in username_list:
                f_username = DatabaseHelper._DatabaseHelper__create_user(app, twitter, f, is_detail=False)
                app.create_following_relationship(f_username, username)

    @staticmethod
    def __create_user(app, twitter, username, is_detail=True):
        try:
            profile = twitter.get_user_profile(username, is_detail)
            p_username = profile["username"]
            p_screenname = profile["screen_name"]
            p_description = profile["user_description"]
            p_user_website = profile["user_website"]
            p_join_date = profile["join_date"]
            p_following_num = profile["following_number"]
            p_post_number = profile["post_number"]
            p_img_url = profile["profile_img_url"]
            p_follower_number = profile["follower_number"]
            p_following_list = profile["follower_list"]
            p_follower_list = profile["following_list"]


            app.create_user(p_username, p_screenname, p_img_url, p_post_number, p_follower_number, p_following_num,
                            p_description, p_user_website, p_join_date)

            if p_follower_list != []:
                DatabaseHelper._DatabaseHelper__follower_helper(app, twitter, p_username, p_following_list)

            if p_following_list != []:
                DatabaseHelper._DatabaseHelper__following_helper(app, twitter, p_username, p_following_list)

            print("created user:", username)
            return p_username
        except:
            print("user not created")

    @staticmethod
    def __find_posts(app, twitter, username, post_number=None):
        post_list = twitter.get_user_posts(username, post_number)
        if app.find_user(username) == []:
            DatabaseHelper._DatabaseHelper__create_user(app, twitter, username, is_detail=False)

        for post in post_list:
            DatabaseHelper._DatabaseHelper__create_post(app, twitter, post)
