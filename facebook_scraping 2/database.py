import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import scraper
from  database_helper import DatabaseHelper
class App:

	def __init__(self, uri, user, password):
		self.driver = GraphDatabase.driver(uri, auth=(user, password))

	def close(self):
		# Don't forget to close the driver connection when you are finished with it
		self.driver.close()


	def create_user(self,username, profile_url, screen_name, profile_img_url, bio):
		with self.driver.session() as session:
		# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_user, username, profile_url, screen_name, profile_img_url, bio)
			for record in result:
				print("Created user: {u}".format(u=record['u']))
			

	@staticmethod
	def __create_user(tx,username, profile_url, screen_name, profile_img_url, bio):

		query = (
		"MERGE (u: FacebookUser {username: $username, profile_url: $profile_url, screen_name:$screen_name, profile_img_url: $profile_img_url, bio: $bio}) "
		"RETURN (u) "
		)
		result = tx.run(query,username=username, profile_url=profile_url, screen_name=screen_name, profile_img_url=profile_img_url, bio=bio)
		try:
			return [{"u": record["u"]["screen_name"]}  for record in result]
			# Capture any errors along with the query and data for traceability
		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(query=query, exception=exception))
			raise

	def create_page(self, page_url, page_name, screen_name, category, liked_number, follower_number, bio):
		with self.driver.session() as session:
		# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_page, page_url, page_name, screen_name, category, liked_number, follower_number, bio)
			for record in result:
				print("Created page: {p}".format(p=record['p']))
			

	@staticmethod
	def __create_page(tx,page_url, page_name, screen_name, category, liked_number, follower_number, bio):

		query = (
		"MERGE (p: FacebookPage {page_url: $page_url, page_name:$page_name, screen_name: $screen_name, category: $category, liked_number:$liked_number, follower_number: $follower_number, bio: $bio}) "
		"RETURN (p) "
		)
		result = tx.run(query, page_url=page_url, page_name=page_name, screen_name=screen_name, category=category, liked_number=liked_number, follower_number=follower_number, bio=bio)
		try:
			return [{"p": record["p"]["page_name"]}  for record in result]
			# Capture any errors along with the query and data for traceability
		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(query=query, exception=exception))
			raise


	def create_post(self,  post_url ,post_date, content_text, img_url_list, video_url):
		with self.driver.session() as session:
		# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_post,  post_url ,post_date, content_text, img_url_list, video_url)
			for record in result:
				print("Created post: {p}".format(p=record['p']))

	@staticmethod
	def __create_post(tx, post_url ,post_date, content_text, img_url_list, video_url):

		query = (
		"MERGE (p:FacebookPost {post_url: $post_url, post_date:$post_date, content_text: $content_text, img_url_list: $img_url_list, video_url: $video_url}) "
		"RETURN p "
		)
		result = tx.run(query, post_url=post_url, post_date= post_date, content_text= content_text, img_url_list= img_url_list, video_url=video_url)
		try:
			return [{"p": record["p"]["post_url"],"p": record["p"]["post_date"], "p": record["p"]["content_text"],
			 "p": record["p"]["img_url_list"], "p": record["p"]["video_url"]}
			 for record in result]
		# Capture any errors along with the query and data for traceability
		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise


	def create_posted_relationship(self, profile_url, post_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_posted_relationship, profile_url, post_url)
			for record in result:
				print("Created posted between: {u}, {p}".format(u=record['u'], p=record['p']))



	@staticmethod
	def __create_and_return_posted_relationship(tx, profile_url, post_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:POSTED]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_page_posted_relationship(self, profile_url, post_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_page_posted_relationship, profile_url, post_url)
			for record in result:
				print("Created page posted between: {u}, {p}".format(u=record['u'], p=record['p']))



	@staticmethod
	def __create_and_return_page_posted_relationship(tx, page_url, post_url):

		query = (
			"MATCH (u: FacebookPage), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.page_url= $page_url " 
			"MERGE (u)-[:POSTED]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, page_url=page_url, post_url=post_url)
		try:
			return [{"u": record["u"]["page_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_like_page_relationship(self, profile_url, page_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_like_page_relationship, profile_url, page_url)
			for record in result:
				print("Created liked between: {u}, {p}".format(u=record['u'], p=record['p']))



	@staticmethod
	def __create_and_return_like_page_relationship(tx, profile_url, page_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPage) "
			"WHERE p.page_url= $page_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:LIKED]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, page_url=page_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["page_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise


	def create_friends_with_relationship(self, profile_url_1, profile_url_2):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_friends_with_relationship, profile_url_1, profile_url_2)
			for record in result:
				print("Created friends between: {u1}, {u2}".format(u1=record['u1'], u2=record['u2']))

	@staticmethod
	def __create_and_return_friends_with_relationship(tx, profile_url_1, profile_url_2):

		query = (
			"MATCH (u1: FacebookUser), (u2: FacebookUser) "
			"WHERE u1.profile_url= $profile_url_1 AND u2.profile_url= $profile_url_2 " 
			"MERGE (u1)-[:FRIENDS_WITH]->(u2) "
			"RETURN u1, u2 "
		)
		result = tx.run(query, profile_url_1=profile_url_1, profile_url_2=profile_url_2)
		try:
			return [{"u1": record["u1"]["profile_url"], "u2": record["u2"]["profile_url"]} for record in result]

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
		result = tx.run(query,hashtag = hashtag)
		try:
			return [{"h": record["h"]["hashtag"]}
			 for record in result]
		# Capture any errors along with the query and data for traceability
		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_location(self, location):
		with self.driver.session() as session:
		# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_location, location)
			for record in result:
				print("Created location: {l}".format(l=record['l']))

	@staticmethod
	def __create_location(tx, location):

		query = (
		"MERGE (l:Location {location: $location}) "
		"RETURN l "
		)
		result = tx.run(query,location = location)
		try:
			return [{"l": record["l"]["location"]}
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
			"MATCH (h: Hashtag), (p: FacebookPost) "
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




	def create_mentioned_in_post_relationship(self, post_url, profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_create_mentioned_in_post_relationship, post_url, profile_url)
			for record in result:
				print("Created mentioned on comment between: {p}, {u}".format(p=record['p'], u=record['u']))

	@staticmethod
	def __create_and_return_create_mentioned_in_post_relationship(tx, post_url, profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:MENTIONED_IN]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise




	def create_liked_post_relationship(self, post_url, profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_liked_post_relationship, post_url, profile_url)
			for record in result:
				print("Created liked post between: {p}, {u}".format(p=record['p'], u=record['u']))

	@staticmethod
	def __create_and_return_liked_post_relationship(tx, post_url, profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.username= $username " 
			"MERGE (u)-[:LIKED]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, post_url=post_url , profile_url=profile_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

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
	def __create_comment(tx,  comment):

		query = (
		"MERGE (c:FacebookComment {comment: {comment}}) "
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

	def create_company(self, company_name):
		with self.driver.session() as session:
		# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_company, company_name)
			for record in result:
				print("Created company: {c}".format(c=record['c']))

	@staticmethod
	def __create_company(tx,  company_name):

		query = (
		"MERGE (c:Company {company_name: {company_name}}) "
		"RETURN c "
		)
		result = tx.run(query, company_name=company_name)
		try:
			return [{"c": record["c"]["company_name"]}
			 for record in result]
		# Capture any errors along with the query and data for traceability
		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_university(self, university_name):
		with self.driver.session() as session:
		# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_university, university_name)
			for record in result:
				print("Created university: {u}".format(u=record['u']))

	@staticmethod
	def __create_university(tx,  university_name):

		query = (
		"MERGE (u:University {university_name: {university_name}}) "
		"RETURN u "
		)
		result = tx.run(query, university_name=university_name)
		try:
			return [{"u": record["u"]["university_name"]}
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
			"MATCH (c: FacebookComment), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND c.comment= $comment " 
			"MERGE (c)-[:COMMENTED_ON]->(p) "
			"RETURN c, p "
		)
		result = tx.run(query, comment=comment , post_url=post_url)
		try:
			return [{"c": record["c"]["comment"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_commented_relationship(self, comment, profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_commented_relationship, comment, profile_url)
			for record in result:
				print("Created commented  between: {c}, {u}".format(c=record['c'], u=record['u']))

	@staticmethod
	def __create_and_return_commented_relationship(tx, comment, profile_url):

		query = (
			"MATCH (c: FacebookComment), (u: FacebookUser) "
			"WHERE c.comment= $comment AND u.profile_url= $profile_url " 
			"MERGE (u)-[:COMMENTED]->(c) "
			"RETURN u, c "
		)
		result = tx.run(query, comment=comment , profile_url=profile_url)
		try:
			return [{"c": record["c"]["comment"], "u": record["u"]["profile_url"]} for record in result]

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
			"MATCH (c1: FacebookComment), (c2: FacebookComment) "
			"WHERE c1.comment= $c1 AND c2.comment= $c2 " 
			"MERGE (c1)-[:REPLIED]->(c2) "
			"RETURN c1, c2 "
		)
		result = tx.run(query, c1=c1 , c2=c2)
		try:
			return [{"c1": record["c1"]["comment"], "c2": record["c2"]["comment"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_live_in_relationship(self, profile_url, location):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_live_in_relationship, profile_url, location)
			for record in result:
				print("Created live in relationship between: {u}, {l}".format(u=record['u'], l=record['l']))

	@staticmethod
	def __create_and_return_live_in_relationship(tx, profile_url, location):

		query = (
			"MATCH (u: FacebookUser), (l: Location) "
			"WHERE l.location= $location AND u.profile_url= $profile_url " 
			"MERGE (u)-[:LIVE_IN]->(l) "
			"RETURN u, l "
		)
		result = tx.run(query, profile_url=profile_url, location=location)
		try:
			return [{"u": record["u"]["profile_url"], "l": record["l"]["location"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_born_in_relationship(self, profile_url, location):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_live_in_relationship, profile_url, location)
			for record in result:
				print("Created born in relationship between: {u}, {l}".format(u=record['u'], l=record['l']))

	@staticmethod
	def __create_and_return_born_in_relationship(tx, profile_url, location):

		query = (
			"MATCH (u: FacebookUser), (l: Location) "
			"WHERE l.location= $location AND u.profile_url= $profile_url " 
			"MERGE (u)-[:BORN_IN]->(l) "
			"RETURN u, l "
		)
		result = tx.run(query, profile_url=profile_url, location=location)
		try:
			return [{"u": record["u"]["profile_url"], "l": record["l"]["location"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise


	def create_like_reaction_to_post_relationship(self, post_url,profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_like_reacted_in_post_relationship,post_url,profile_url)
			for record in result:
				print("Created like reaction in post relationship between: {u}, {p}".format(u=record['u'], p=record['p']))

	@staticmethod
	def __create_and_return_like_reacted_in_post_relationship(tx,post_url,profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:LIKED_REACTION]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise



	def create_love_reaction_to_post_relationship(self, post_url,profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_love_reacted_in_post_relationship,post_url,profile_url)
			for record in result:
				print("Created love reaction in post relationship between: {u}, {p}".format(u=record['u'], p=record['p']))

	@staticmethod
	def __create_and_return_love_reacted_in_post_relationship(tx,post_url,profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:LOVED_REACTION]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise


	def create_care_reaction_to_post_relationship(self, post_url,profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_care_reacted_in_post_relationship,post_url,profile_url)
			for record in result:
				print("Created care reaction in post relationship between: {u}, {p}".format(u=record['u'], p=record['p']))

	@staticmethod
	def __create_and_return_care_reacted_in_post_relationship(tx,post_url,profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:CARE_REACTION]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise


	def create_sad_reaction_to_post_relationship(self, post_url,profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_sad_reacted_in_post_relationship,post_url,profile_url)
			for record in result:
				print("Created sad reaction in post relationship between: {u}, {p}".format(u=record['u'], p=record['p']))

	@staticmethod
	def __create_and_return_sad_reacted_in_post_relationship(tx,post_url,profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:SAD_REACTION]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise


	def create_angry_reaction_to_post_relationship(self, post_url,profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_angry_reacted_in_post_relationship,post_url,profile_url)
			for record in result:
				print("Created angry reaction in post relationship between: {u}, {p}".format(u=record['u'], p=record['p']))

	@staticmethod
	def __create_and_return_angry_reacted_in_post_relationship(tx,post_url,profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:ANGRY_REACTION]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_haha_reaction_to_post_relationship(self, post_url,profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_haha_reacted_in_post_relationship,post_url,profile_url)
			for record in result:
				print("Created haha reaction in post relationship between: {u}, {p}".format(u=record['u'], p=record['p']))

	@staticmethod
	def __create_and_return_haha_reacted_in_post_relationship(tx,post_url,profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:HAHA_REACTION]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_wow_reaction_to_post_relationship(self, post_url,profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_wow_reacted_in_post_relationship,post_url,profile_url)
			for record in result:
				print("Created wow reaction in post relationship between: {u}, {p}".format(u=record['u'], p=record['p']))

	@staticmethod
	def __create_and_return_wow_reacted_in_post_relationship(tx,post_url,profile_url):

		query = (
			"MATCH (u: FacebookUser), (p: FacebookPost) "
			"WHERE p.post_url= $post_url AND u.profile_url= $profile_url " 
			"MERGE (u)-[:WOW_REACTION]->(p) "
			"RETURN u, p "
		)
		result = tx.run(query, profile_url=profile_url, post_url=post_url)
		try:
			return [{"u": record["u"]["profile_url"], "p": record["p"]["post_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise


	def create_company_located_in_relationship(self, company_name, location):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_company_located_in_relationship, company_name, location)
			for record in result:
				print("Created company located in relationship between: {c}, {l}".format(c=record['c'], l=record['l']))

	@staticmethod
	def __create_and_return_company_located_in_relationship(tx, company_name, location):

		query = (
			"MATCH (c: Company), (l: Location) "
			"WHERE l.location= $location AND c.company_name= $company_name " 
			"MERGE (c)-[:LOCATED_IN]->(l) "
			"RETURN c, l "
		)
		result = tx.run(query, company_name=company_name, location=location)
		try:
			return [{"c": record["c"]["company_name"], "l": record["l"]["location"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_worked_relationship(self, company_name, profile_url, position, duration):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_worked_in, company_name, profile_url, position, duration)
			for record in result:
				print("Created worked in relationship between: {c}, {u}".format(c=record['c'], u=record['u']))

	@staticmethod
	def __create_and_return_worked_in(tx, company_name, profile_url, position, duration):

		query = (
			"MATCH (u: FacebookUser),(c: Company) "
			"WHERE u.profile_url = $profile_url AND c.company_name = $company_name "
			"MERGE (u)-[r:WORK_IN { position: $position, duration: $duration }]->(c) "
			"RETURN c, u "
		)
		result = tx.run(query, company_name=company_name, profile_url=profile_url, position=position, duration=duration)
		try:
			return [{"c": record["c"]["company_name"], "u": record["u"]["profile_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def create_studied_in_relationship(self, university_name, faculty, grad_year, profile_url):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__create_and_return_studied_in, university_name, faculty, grad_year, profile_url)
			for record in result:
				print("Created studied in relationship between: {uni}, {user}".format(uni=record['uni'], user=record['user']))

	@staticmethod
	def __create_and_return_studied_in(tx, university_name, faculty, grad_year, profile_url):

		query = (
			"MATCH (user: FacebookUser),(uni: University) "
			"WHERE user.profile_url = $profile_url AND uni.university_name = $university_name "
			"MERGE (user)-[r:STUDIED_IN { faculty: $faculty, grad_year: $grad_year }]->(uni) "
			"RETURN uni, user "
		)
		result = tx.run(query, university_name=university_name, faculty=faculty, grad_year=grad_year, profile_url=profile_url)
		try:
			return [{"uni": record["uni"]["university_name"], "user": record["user"]["profile_url"]} for record in result]

		except ServiceUnavailable as exception:
			logging.error("{query} raised an error: \n {exception}".format(
			query=query, exception=exception))
			raise

	def find_node(self, q):
		with self.driver.session() as session:
			# Write transactions allow the driver to handle retries and transient errors
			result = session.write_transaction(
			self.__find_and_return_node,q)
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
	url = "bolt://localhost:11007"
	usr = "neo4j"
	password = "sniper61"
	app = App(url, usr, password)
	facebook = scraper.Facebook_scraper()
	facebook.start_driver()
	facebook.driver.get(facebook.URL)
	facebook.login()



	DatabaseHelper._DatabaseHelper__create_detailed_user(app, facebook, "uobeee")
	#DatabaseHelper._DatabaseHelper__create_page_helper(app, facebook, "mahmutok", search_post =  True)

	app.close()