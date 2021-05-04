from scraper import Instagram_scraper

posts_count = 1
browser = "chrome"

instagram_ai = Instagram_scraper(browser)

result = instagram_ai.get_hashtag_results("doritos", 7)

print(result)

