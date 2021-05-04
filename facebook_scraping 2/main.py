
from scraper import Facebook_scraper
import csv

browser = "chrome"

facebook = Facebook_scraper()
facebook.start_driver()
facebook.driver.get(facebook.URL)
facebook.login()

result = facebook.search_user("uobeee", get_posts = True, detail = False)


