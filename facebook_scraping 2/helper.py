import datetime
import locale
import re
class HelperFunctions():

	@staticmethod
	def __format_date(posted_date):
		locale.setlocale(locale.LC_TIME, "tr_TR")
		date_format_list = ["%d %B, %H:%M", "%d %B %Y, %H:%M", "%d %B %Y", "%d %B"]
		if "Dün" in posted_date:
			dt_obj = datetime.datetime.today()
			dt_obj = dt_obj.replace(hour=int(posted_date.split(" ")[1].split(":")[0]))
			dt_obj = dt_obj.replace(minute=int(posted_date.split(" ")[1].split(":")[1]))
		if re.findall("[0-9]{0,2}[g]{1}",posted_date) != []:
			num = int(re.findall('\d+', posted_date)[0])
			today = datetime.datetime.now()    
			dt_obj = today - datetime.timedelta(days=num)
		for format in date_format_list:
			try:
				dt_obj = datetime.datetime.strptime(posted_date, format)
			except:
				pass
		if dt_obj.year == 1900:
			current_year = datetime.datetime.today().year
			dt_obj = dt_obj.replace(year=current_year)
		dt_str = dt_obj.strftime("%d.%m.%Y %H:%M")
		return dt_str

	@staticmethod
	def __get_parsed_mentions(raw_text):
		regex = re.compile(r"@([\w\.]+)")
		regex.findall(raw_text)
		return regex.findall(raw_text)

	@staticmethod
	def __get_parsed_hashtags(raw_text):
		regex = re.compile(r"#(\w+)")
		regex.findall(raw_text)
		return regex.findall(raw_text)

	@staticmethod
	def __format_numbers(string):
		"""expects string and returns numbers from them as integer type,
		e.g => input = '54454 comment', than output => 54454
		"""
		if '.' in string:
			string = string.replace(".", "")
		try:
			return int(string.split(" ")[0])
		except IndexError:
			return 0

	@staticmethod
	def __hashtag_number(string):

		number = float(string.split()[0])
		decisive_string = string.split()[1]
		if decisive_string == 'B':
			number = int(number * 1000)
		elif decisive_string == 'Mn':
			number = int(number * 1000000)
	
		return number


	@staticmethod
	def __extract_number(string):

		number= int(re.findall('\d+', string )[0])
		return number

	@staticmethod
	def __get_position(string):
		p = re.compile(r"(?<=('te )).*|(?<=('de )).*|(?<=('ta )).*|(?<=('da )).*")
		match = p.search(string)        
		if match:               
			position = match.group(0)
		return position

	@staticmethod
	def __get_career(string):
		try:
			company = re.search(r'([ \wÜüşŞçÇÖöĞğıİ]*)(\'de|\'da|\'te|\'ta)',string)[0][:-3]
			position = re.search(r'(\'de|\'da|\'te|\'ta)([ \wÜüşŞçÇÖöĞğıİ]*)',string)[0][4:]
			duration = string.split('\n')[1]
			city = string.split('\n')[3]
			return company, position, duration, city
		except:
			return " "
	
	@staticmethod
	def __get_university(string):
		if('niversite' in string or 'nivercity' in string):
			univ = re.search(r'[ \wÜüşŞçÇÖöĞğıİ?]*\'de', string.split('\n')[0])[0][:-3]
			graduateYear = string.split('\n')[1]
			faculty = re.search(r'(\'de)([ \wÜüşŞçÇÖöĞğıİ]*)( okudu)', string.split('\n')[0])[2][1:]
			return univ, graduateYear, faculty
		else:
			return " "

				   
	    # if('Lise' in sampleLine or 'lise' in sampleLine):
	    #     pass
	    #     # deniz bu formatın nasıl olacağı hakkında hiçbir fikrim yok :(

