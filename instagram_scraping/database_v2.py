import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import scraper
from database_helper import DatabaseHelper
import sys


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_user(self, username, name, profile_img_url, post_number, follower_number, following_number, bio):
        with self.driver.session() as session:
            try:
                # Write transactions allow the driver to handle retries and transient errors
                result = session.write_transaction(
                    self.__create_user, username, name, profile_img_url, post_number, follower_number, following_number,
                    bio)
                for record in result:
                    print("Created user: {u}".format(u=record['u']))
            except:
                print("already exists")

    @staticmethod
    def __create_user(tx, username, name, profile_img_url, post_number, follower_number, following_number, bio):

        query = (
            "MERGE (u: InstagramUser {username: $username, name:$name, profile_img_url: $profile_img_url, post_number: $post_number, follower_number: $follower_number, following_number: $following_number}) "
            "RETURN (u) "
        )
        result = tx.run(query, username=username, name=name, profile_img_url=profile_img_url, post_number=post_number,
                        follower_number=follower_number, following_number=following_number, bio=bio)
        try:
            return [{"u": record["u"]["username"]} for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(query=query, exception=exception))
            raise

    def create_post(self, post_url, caption, description, date, like_num):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            try:

                result = session.write_transaction(
                    self.__create_post, post_url, caption, description, date, like_num)
                for record in result:
                    print("Created post: {p}".format(p=record['p']))
            except:
                print("already exists")

    @staticmethod
    def __create_post(tx, post_url, caption, description, date, like_num):

        query = (
            "MERGE (p:InstagramPost {post_url: $post_url, caption:$caption, description: $description, date: $date, like_num: $like_num}) "
            "RETURN p "
        )

        result = tx.run(query, post_url=post_url, caption=caption, description=description, date=date,
                        like_num=like_num)

        try:
            return [{"p": record["p"]["post_url"], "p": record["p"]["caption"], "p": record["p"]["description"],
                     "p": record["p"]["date"], "p": record["p"]["like_num"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_posted_relationship(self, username, post_url):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_and_return_posted_relationship, username, post_url)
            for record in result:
                print("Created posted between: {u}, {p}".format(u=record['u'], p=record['p']))

    @staticmethod
    def __create_and_return_posted_relationship(tx, username, post_url):

        query = (
            "MATCH (u: InstagramUser), (p: InstagramPost) "
            "WHERE p.post_url= $post_url AND u.username= $username "
            "MERGE (u)-[:POSTED]->(p) "
            "RETURN u, p "
        )
        result = tx.run(query, username=username, post_url=post_url)
        try:
            return [{"u": record["u"]["username"], "p": record["p"]["post_url"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_hashtag(self, hashtag):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_hashtag, hashtag)
            for record in result:
                print("Created hashtag: {h}".format(h=record['h']))

    @staticmethod
    def __create_hashtag(tx, hashtag):

        query = (
            "MERGE (h:Hashtag {hashtag: $hashtag}) "
            "RETURN h "
        )
        result = tx.run(query, hashtag=hashtag)
        try:
            return [{"h": record["h"]["hashtag"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_hashtagged_post_relationship(self, post_url, hashtag):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_and_return_hashtagged_post_relationship, post_url, hashtag)
            for record in result:
                print("Created hashtagged post between: {p}, {h}".format(p=record['p'], h=record['h']))

    @staticmethod
    def __create_and_return_hashtagged_post_relationship(tx, post_url, hashtag):

        query = (
            "MATCH (h: Hashtag), (p: InstagramPost) "
            "WHERE p.post_url= $post_url AND h.hashtag= $hashtag "
            "MERGE (p)-[:HASHTAGGED]->(h) "
            "RETURN h, p "
        )
        result = tx.run(query, post_url=post_url, hashtag=hashtag)
        try:
            return [{"h": record["h"]["hashtag"], "p": record["p"]["post_url"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_hashtagged_comment_relationship(self, comment, hashtag):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_hashtagged_comment_relationship, comment, hashtag)
            for record in result:
                print("Created hashtagged comment between: {c}, {h}".format(c=record['c'], h=record['h']))

    @staticmethod
    def _create_and_return_hashtagged_comment_relationship(tx, comment, hashtag):

        query = (
            "MATCH (h: Hashtag), (c: InstagramComment) "
            "WHERE p.post_url= $post_url AND c.comment= $comment "
            "MERGE (c)-[:HASHTAGGED]->(h) "
            "RETURN h, c "
        )
        result = tx.run(query, comment=comment, hashtag=hashtag)
        try:
            return [{"h": record["h"]["hashtag"], "p": record["c"]["comment"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_mentioned_in_post_relationship(self, post_url, username):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_and_return_create_mentioned_in_post_relationship, post_url, username)
            for record in result:
                print("Created mentioned on comment between: {p}, {u}".format(p=record['p'], u=record['u']))

    @staticmethod
    def __create_and_return_create_mentioned_in_post_relationship(tx, post_url, username):

        query = (
            "MATCH (u: InstagramUser), (p: InstagramPost) "
            "WHERE p.post_url= $post_url AND u.username= $username "
            "MERGE (u)-[:MENTIONED_IN]->(p) "
            "RETURN u, p "
        )
        result = tx.run(query, username=username, post_url=post_url)
        try:
            return [{"u": record["u"]["username"], "p": record["p"]["post_url"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_tagged_in_post_relationship(self, username, post_url):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            try:
                result = session.write_transaction(
                    self.__create_and_return_create_tagged_in_post_relationship, post_url, username)
                for record in result:
                    print("Created tagged in comment between: {p}, {u}".format(p=record['p'], u=record['u']))
            except:
                print("already exist")

    @staticmethod
    def __create_and_return_create_tagged_in_post_relationship(tx, username, post_url):

        query = (
            "MATCH (u: InstagramUser), (p: InstagramPost) "
            "WHERE p.post_url= $post_url AND u.username= $username "
            "MERGE (u)-[:TAGGED_IN]->(p) "
            "RETURN u, p "
        )

        result = tx.run(query, username=username, post_url=post_url)

        try:
            return [{"u": record["u"]["username"], "p": record["p"]["post_url"]} for record in result]

        except ServiceUnavailable as exception:
            return [{"u": "", "p": ""} for record in result]
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))

            raise

    def create_liked_post_relationship(self, post_url, username):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_and_return_liked_post_relationship, post_url, username)
            for record in result:
                print("Created liked post between: {p}, {u}".format(p=record['p'], u=record['u']))

    @staticmethod
    def __create_and_return_liked_post_relationship(tx, post_url, username):

        query = (
            "MATCH (u: InstagramUser), (p: InstagramPost) "
            "WHERE p.post_url= $post_url AND u.username= $username "
            "MERGE (u)-[:LIKED]->(p) "
            "RETURN u, p "
        )
        result = tx.run(query, post_url=post_url, username=username)
        try:
            return [{"u": record["u"]["username"], "p": record["p"]["post_url"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_comment(self, comment):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_comment, comment)
            for record in result:
                print("Created comment: {c}".format(c=record['c']))

    @staticmethod
    def __create_comment(tx, comment):

        query = (
            "MERGE (c:InstagramComment {comment: {comment}}) "
            "RETURN c "
        )
        result = tx.run(query, comment=comment)
        try:
            return [{"c": record["c"]["comment"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_commented_on_relationship(self, comment, post_url):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_and_return_commented_on_relationship, comment, post_url)
            for record in result:
                print("Created commented on between: {c}, {p}".format(c=record['c'], p=record['p']))

    @staticmethod
    def __create_and_return_commented_on_relationship(tx, comment, post_url):

        query = (
            "MATCH (c: InstagramComment), (p: InstagramPost) "
            "WHERE p.post_url= $post_url AND c.comment= $comment "
            "MERGE (c)-[:COMMENTED_ON]->(p) "
            "RETURN c, p "
        )
        result = tx.run(query, comment=comment, post_url=post_url)
        try:
            return [{"c": record["c"]["comment"], "p": record["p"]["post_url"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_commented_relationship(self, comment, username):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_and_return_commented_relationship, comment, username)
            for record in result:
                print("Created commented on between: {c}, {u}".format(c=record['c'], u=record['u']))

    @staticmethod
    def __create_and_return_commented_relationship(tx, comment, username):

        query = (
            "MATCH (c: InstagramComment), (u: InstagramUser) "
            "WHERE c.comment= $comment AND u.username= $username "
            "MERGE (u)-[:COMMENTED]->(c) "
            "RETURN u, c "
        )
        result = tx.run(query, comment=comment, username=username)
        try:
            return [{"c": record["c"]["comment"], "u": record["u"]["username"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_replied_on_relationship(self, c1, c2):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_and_return_replied_on_relationship, c1, c2)
            for record in result:
                print("Created commented on between: {c1}, {c2}".format(c1=record['c1'], c2=record['c2']))

    @staticmethod
    def __create_and_return_replied_on_relationship(tx, c1, c2):

        query = (
            "MATCH (c1: InstagramComment), (c2: InstagramComment) "
            "WHERE c1.comment= $c1 AND c2.comment= $c2 "
            "MERGE (c1)-[:REPLIED]->(c2) "
            "RETURN c1, c2 "
        )
        result = tx.run(query, c1=c1, c2=c2)
        try:
            return [{"c1": record["c1"]["comment"], "c2": record["c2"]["post_url"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_follow_relationship(self, u1, u2):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__create_and_return_follow_relationship, u1, u2)
            for record in result:
                print("Created follow relationship between: {u1}, {u2}".format(u1=record['u1'], u2=record['u2']))

    @staticmethod
    def __create_and_return_follow_relationship(tx, u1, u2):

        query = (
            "MATCH (u1: InstagramUser), (u2: InstagramUser) "
            "WHERE u1.username= $u1 AND u2.username= $u2 "
            "MERGE (u1)-[:FOLLOWS]->(u2) "
            "RETURN u1, u2 "
        )
        result = tx.run(query, u1=u1, u2=u2)
        try:
            return [{"u1": record["u1"]["username"], "u2": record["u2"]["username"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_node(self, q):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.__find_and_return_node, q)
            return result
        # for record in result:
        # 	print("Found node: {c1}".format(n=record['n']))

    @staticmethod
    def __find_and_return_node(tx, q):
        query = (
                "MATCH (n:" + q + ") "
                                  "RETURN n "
        )
        result = tx.run(query)
        try:
            return [{"n": record["n"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


if __name__ == "__main__":

    port = 7687
    url = "bolt://213.238.179.211:7687"
    usr = "neo4j"
    password = "Aksaray68"
    app = App(url, usr, password)
    instagram = scraper.Instagram_scraper()

    # login_username = "rdctest"
    # login_password = "aidMAT787#%*"
    # login_username = "rdcplus"
    # login_password = "rdc.plusSM20*"

    # login_username = "anrdc7"
    # login_password = "Can657006.."

    login_username = sys.argv[1]
    login_password = sys.argv[2]

    instagram.start_driver()
    instagram.driver.get(instagram.URL)
    instagram.login(login_username, login_password)

    option = sys.argv[3]
    if option == 'create_user':
        username = sys.argv[4]
        DatabaseHelper._DatabaseHelper__create_detailed_user(app, instagram, username)
    elif option == 'create_posts':
        username = sys.argv[4]
        try:
            post_num = sys.argv[5]
        except:
            post_num = None
        DatabaseHelper._DatabaseHelper__find_posts(instagram, app, username, post_num=post_num)
    elif option == 'hashtag_search':
        keyword = sys.argv[4]
        post_num = sys.argv[5]
        DatabaseHelper._DatabaseHelper__find_hashtag_posts(instagram, app, keyword, post_num=post_num)
    instagram.driver.quit()
    app.close()
