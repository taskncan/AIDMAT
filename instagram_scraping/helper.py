import re
import datetime
class HelperFunctions():


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
	def __get_int(text):	

		text = text.replace(".","")
		text = text.replace(",","")
		text = int(text)
		return text

	@staticmethod
	def __get_datetime(datetime_str):
		
		d_obj = datetime.datetime.fromisoformat(datetime_str[:-1])
		d_str = d_obj.strftime('%Y-%m-%d %H:%M:%S')
		return d_str



