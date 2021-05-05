import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import scraper
from database_helper import DatabaseHelper


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_user(self, username, screen_name, profile_img_url, post_number, follower_number, following_number,
                    user_description,
                    user_website, join_date):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_user, username, screen_name, profile_img_url, post_number, follower_number,
                following_number,
                user_description, user_website, join_date)
            for record in result:
                print("Created user: {u}".format(u=record['u']))

    @staticmethod
    def _create_user(tx, username, screen_name, profile_img_url, post_number, follower_number, following_number,
                     user_description,
                     user_website, join_date):

        query = (
            "MERGE (u:TwitterUser { username: $username, screen_name:$screen_name, profile_img_url: $profile_img_url, post_number: $post_number, follower_number: $follower_number, following_number: $following_number}) "
            "RETURN u"
        )
        result = tx.run(query, username=username, screen_name=screen_name, profile_img_url=profile_img_url,
                        post_number=post_number,
                        follower_number=follower_number, following_number=following_number,
                        user_description=user_description, user_website=user_website, join_date=join_date)
        try:
            return [{"u": record["u"]["username"], "u": record["u"]["name"], "u": record["u"]["profile_img_url"],
                     "u": record["u"]["post_number"], "u": record["u"]["follower_number"],
                     "u": record["u"]["following_number"],
                     "u": record["u"]["user_description"], "u": record["u"]["user_website"],
                     "u": record["u"]["join_date"]} for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(query=query, exception=exception))
            raise

    def find_user(self, username):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_user, username)
            for record in result:
                print("Found twitter person: {record}".format(record=record))
            return result

    @staticmethod
    def _find_and_return_user(tx, username):
        query = (
            "MATCH (u:TwitterUser) "
            "WHERE u.username = $username "
            "RETURN u.username AS username "
        )
        result = tx.run(query, username=username)

        return [record["username"] for record in result]

    def create_post(self, post_id, post_url, post_date, username, retweet_count, like_count, quote_count, post_content,
                    img_urls, shared_url):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_post, post_id, post_url, post_date, username, retweet_count, like_count, quote_count,
                post_content, img_urls, shared_url)
            for record in result:
                print("Created post: {p}".format(p=record['p']))

    @staticmethod
    def _create_post(tx, post_id, post_url, post_date, username, retweet_count, like_count, quote_count, post_content,
                     img_urls, shared_url):

        query = (
            """MERGE (p:TwitterPost { post_id: $post_id, post_url:$post_url, username: $username, retweet_count: $retweet_count, like_count: $like_count,
		 quote_count: $quote_count,  post_content: $post_content,  img_urls: $img_urls, shared_url: $shared_url 
		  }) """

            "RETURN p "
        )
        result = tx.run(query, post_id=post_id, post_url=post_url, username=username, post_date=post_date,
                        retweet_count=retweet_count,
                        like_count=like_count, quote_count=quote_count, post_content=post_content, img_urls=img_urls,
                        shared_url=shared_url)
        try:
            return [{"p": record["p"]["post_id"], "p": record["p"]["post_url"], "p": record["p"]["post_date"],
                     "p": record["p"]["username"],
                     "p": record["p"]["retweet_count"], "p": record["p"]["like_count"], "p": record["p"]["quote_count"],
                     "p": record["p"]["post_content"], "p": record["p"]["img_urls"], "p": record["p"]["shared_url"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_post(self, post_id):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_post, post_id)
            for record in result:
                print("Found post: {record}".format(record=record))
            return result

    @staticmethod
    def _find_and_return_post(tx, post_id):
        query = (
            "MATCH (p:TwitterPost) "
            "WHERE p.post_id = $post_id "
            "RETURN p AS post "
        )
        result = tx.run(query, post_id=post_id)

        return [record["post"] for record in result]

    def create_hashtag(self, hashtag):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_hashtag, hashtag)
            for record in result:
                print("Created hashtag: {h}".format(h=record['h']))

    @staticmethod
    def _create_hashtag(tx, hashtag):

        query = (
            "MERGE (h:Hashtag { hashtag: $hashtag}) "
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

    def find_hashtag(self, hashtag):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_hashtag, hashtag)
            for record in result:
                print("Found hashtag: {record}".format(record=record))
            return result

    @staticmethod
    def _find_and_return_hashtag(tx, hashtag):
        query = (
            "MATCH (h:hashtag) "
            "WHERE h.hashtag = $hashtag "
            "RETURN h AS hashtag "
        )
        result = tx.run(query, hashtag=hashtag)

        return [record["hashtag"] for record in result]

    def create_following_relationship(self, username1, username2):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_following_relationship, username1, username2)
            for record in result:
                print("Created FOLLOWS between: {u1}, {u2}".format(u1=record['u1'], u2=record['u2']))

    @staticmethod
    def _create_and_return_following_relationship(tx, username1, username2):

        query = (
            "MATCH (u1:TwitterUser), (u2:TwitterUser) "
            "WHERE u1.username = $username1 AND u2.username = $username2 "
            "MERGE (u1)-[:FOLLOWS]->(u2) "
            "RETURN u1, u2 "
        )
        result = tx.run(query, username1=username1, username2=username2)
        try:
            return [{"u1": record["u1"]["username"], "u2": record["u2"]["username"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_posted_relationship(self, username, post_id):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_posted_relationship, username, post_id)
            for record in result:
                print("Created posted between: {u}, {p}".format(u=record['u'], p=record['p']))

    @staticmethod
    def _create_and_return_posted_relationship(tx, username, post_id):

        query = (
            "MATCH (u:TwitterUser), (p:TwitterPost) "
            "WHERE u.username = $username AND p.post_id = $post_id "
            "MERGE (u)-[:POSTED]->(p) "
            "RETURN u, p "
        )
        result = tx.run(query, username=username, post_id=post_id)
        try:
            return [{"u": record["u"]["username"], "p": record["p"]["post_id"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_mentioned_in_post(self, post_id, username):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_create_mentioned_in_post_relationship, post_id, username)
            for record in result:
                print("Created mentioned in post between: {p}, {u}".format(p=record['p'], u=record['u']))

    @staticmethod
    def _create_and_return_create_mentioned_in_post_relationship(tx, post_id, username):

        query = (
            "MATCH (u:TwitterUser), (p:TwitterPost) "
            "WHERE u.username =$username AND p.post_id = $post_id "
            "MERGE (p)-[:MENTIONED]->(u) "
            "RETURN p, u "
        )
        result = tx.run(query, post_id=post_id, username=username)
        try:
            return [{"p": record["p"]["post_id"], "u": record["u"]["username"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_liked_post_relationship(self, post_id, username):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_liked_post_relationship, post_id, username)
            for record in result:
                print("Created liked post between: {u}, {p}".format(u=record['u'], p=record['p']))

    @staticmethod
    def _create_and_return_liked_post_relationship(tx, post_id, username):

        query = (
            "MATCH (u:TwitterUser), (p:TwitterPost) "
            "WHERE u.username =$username AND p.post_id = $post_id "
            "MERGE (u)-[:LIKED]->(p) "
            "RETURN u, p "
        )
        result = tx.run(query, post_id=post_id, username=username)
        try:
            return [{"u": record["u"]["username"], "p": record["p"]["post_id"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_retweeted_post_relationship(self, post_id, username):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_retweeted_post_relationship, post_id, username)
            for record in result:
                print("Created retweeted between: {u}, {p}".format(u=record['u'], p=record['p']))

    @staticmethod
    def _create_and_return_retweeted_post_relationship(tx, post_id, username):

        query = (
            "MATCH (u:TwitterUser), (p:TwitterPost) "
            "WHERE u.username =$username AND p.post_id = $post_id "
            "MERGE (u)-[:RETWEETED]->(p) "
            "RETURN u, p "
        )
        result = tx.run(query, post_id=post_id, username=username)
        try:
            return [{"u": record["u"]["username"], "p": record["p"]["post_id"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_quoted_post_relationship(self, post_id, username):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_quoted_post_relationship, post_id, username)
            for record in result:
                print("Created quoted between: {u}, {p}".format(u=record['u'], p=record['p']))

    @staticmethod
    def _create_and_return_quoted_post_relationship(tx, post_id, username):

        query = (
            "MATCH (u:TwitterUser), (p:TwitterPost) "
            "WHERE u.username =$username AND p.post_id = $post_id "
            "MERGE (u)-[:QUOTED]->(p) "
            "RETURN u, p "
        )
        result = tx.run(query, post_id=post_id, username=username)
        try:
            return [{"u": record["u"]["username"], "p": record["p"]["post_id"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_hashtagged_post_relationship(self, post_id, hashtag):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_hashtagged_post_relationship, post_id, hashtag)
            for record in result:
                print("Created hashtagged between: {p}, {h}".format(p=record['p'], h=record['h']))

    @staticmethod
    def _create_and_return_hashtagged_post_relationship(tx, post_id, hashtag):

        query = (
            "MATCH (p:TwitterPost), (h:Hashtag) "
            "WHERE p.post_id =$post_id AND h.hashtag = $hashtag "
            "MERGE (c)-[:HASHTAGGED]->(h) "
            "RETURN h, p "
        )
        result = tx.run(query, post_id=post_id, hashtag=hashtag)
        try:
            return [{"h": record["h"]["hashtag"], "p": record["p"]["post_id"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_replied_post_relationship(self, post_id_1, post_id_2):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_replied_post_relationship, post_id_1, post_id_2)
            for record in result:
                print("Created replied between: {p1}, {p2}".format(p1=record['p1'], p2=record['p2']))

    @staticmethod
    def _create_and_return_replied_post_relationship(tx, post_id_1, post_id_2):

        query = (
            "MATCH (p1:TwitterPost), (p2:TwitterPost) "
            "WHERE p1.post_id =$post_id_1 AND p2.post_id = $post_id_2 "
            "MERGE (p1)-[:REPLIED]->(p2) "
            "RETURN p1, p2 "
        )
        result = tx.run(query, post_id_1=post_id_1, post_id_2=post_id_2)
        try:
            return [{"p1": record["p1"]["post_content"], "p2": record["p2"]["post_content"]} for record in result]

        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

if __name__ == "__main__":
    port = 7687
    url = "bolt://localhost:7687"
    usr = "neo4j"
    password = "123456"
    app = App(url, usr, password)
    # mail = kdrhnkrhn@yahoo.com  id = uberseyler  pass = über787%#şey
    # mail = somemema84@yahoo.com  id= somemema   pass = RdcCan..
    # phone = 5424194117   id= bakbucokguzel  pass = bbCGcom787%*

    login_username = "bakbucokguzel"
    login_password = "bbCGcom787%*"
    twitter = scraper.Twitter_scraper()
    twitter.start_driver()
    twitter.driver.get(twitter.URL + "/login")

    twitter.login(login_username, login_password)
    username = "ciftogluuu"

    # DatabaseHelper._DatabaseHelper__create_user(app, twitter, username)

    DatabaseHelper._DatabaseHelper__find_posts(app, twitter, username)

    # DatabaseHelper._DatabaseHelper__find_posts(app, twitter, username)

    app.close()
