import logging
import re
from urllib.request import URLopener

import requests
from fake_useragent import UserAgent

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('log')
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('downloading_car_photos.log')
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
log.addHandler(file_handler)
log.addHandler(console_handler)

MAIN_URL = 'https://www.mobile.de'
PAGE_NUMBER_PLACEHOLDER = '%%%'
PAGE_NUMBER_PHRASE = 'pgn:'

f32_URL = 'https://www.mobile.de/pl/samochod/bmw-seria-4/vhc:car,ms1:3500_-53_,vcg:sportscar'


class CarDownloader:
	"""Class for downloading images from Mobile.de"""

	def __init__(self):
		self

	def download_images(self, url, directory):
		car_counter = 1
		car_pager = 1
		while True:
			correct_url = str(url).replace(PAGE_NUMBER_PLACEHOLDER, PAGE_NUMBER_PHRASE + str(car_pager))
			car_pager += 1
			webpage_source = read_html_page_source(correct_url)
			if check_page(webpage_source):
				car_page_fragments = get_all_car_page_fragments(webpage_source)
				car_links = get_all_car_pages(car_page_fragments)
				for car_link in car_links:
					log.info('Downloading photos from car number: ' + str(car_counter))
					car_counter += 1
					subpage = read_html_page_source(car_link)
					photo_links = get_all_car_photo_links_from(subpage)
					for photo_url in photo_links:
						save_file_on_disc_from(photo_url, directory)


def get_all_car_photo_links_from(webpage_source):
	images = re.findall(r"<div class=\"js-image-data\" data-title(.+?)<\/div>", webpage_source)[0]
	links = re.findall(r"https:(.+?).JPG", images)
	update_pages = ["https:" + link + ".JPG" for link in links]
	return update_pages


def get_all_car_page_fragments(webpage_source):
	return re.findall(r"<article class(.+?)<\/article>", webpage_source)


def get_all_car_pages(car_fragments):
	links = set()
	for fragment in car_fragments:
		links.add(MAIN_URL + (re.findall(r"href=\"(.+?)\">", fragment)[0]))
	return links


def check_page(webpage_source):
	ERROR_MESSAGE_PREFIX = '<p class="js-error-message u-text-center">'
	if ERROR_MESSAGE_PREFIX not in webpage_source:
		return True
	else:
		return False


def read_html_page_source(url):
	ua = UserAgent(cache=False)
	cookie = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			  'accept-encoding': 'gzip, deflate, br',
			  'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,pt;q=0.6',
			  'cookie': 'sorting_e=""; show_qs_e=vhc%3Acar%2Cms1%3A3500_-53_; vi=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaWQiOiI2MThiYzBlNy0wNzAwLTRiYTMtOGQ2OS1mMmZkMDQ1Y2M3MTgiLCJhdWQiOltdLCJpYXQiOjE1NDE1NzYzMzR9.6W3mN_C5U2gbXkSFbWm99XVwiTnsWwJuZiADHNIYhZg; _ga=GA1.2.495630715.1541576336; optimizelyEndUserId=oeu1541576335833r0.33012600410861226; visited=1; axd=1001316771521130073; mdeConsentData=BOW2eGqOW2eGqB9ABBDEBa-AAAJw-BOgACAAkABgA1gBuAL8AYQBigDIAM0AaABpgDYAOcAdwB4AD1AHwAhoBEAEjAJMApYBTgFXAK0Ar4BYgFpALYAuYBeAGXAM0AzoBoAG0AN2Ab4B0QDqAPaAfACFQEMAQ6AiACNQEcAR2Aj4CRwElASeAlICVwEtATCAmgCcQE6AUEAocBRQFGgKQApYBTYCngKrAVcBW4CugK-AWKAsoC1QFtAW6AuAC4gFzgLqAvUBfAF-gMAAwMBgwGIgMUAxcBjQGOAMhAZIBlYDLgM1AZwBnYDPgNAAaKA0oDXwGyAbQA2wBuIDdAN5Ab8BwgDiQHGAceA5QDlwHNAc6A6ADqwHZAdwA7wB4ADyAHmgPQA9YB7YD3gPjAfMB9AD7CcP; mdeCustomConsentData=25; _abck=D40AE9EB20F0D4EC1D82D077F4152725685E64373E3100008F96E25B8A016433~0~pJGUz23KSDuaXNklYhrNtDKX8LcA99Pjwc70oDhLBS8=~-1~-1; via=google; mobile.LOCALE=en; bm_sz=D9EF162DD3C32C8097F2202B783B75C9~QAAQLmReaMQV4OFmAQAA2Z+5CK7/IvIu7KnGghMAARjdvrDsSXO6+EBcjcdyTL9Qz5iWOA2+uscHRDKh30fHRWL6/RtOAfLmQ6GyoXUajI7L8KVKsMMmC5PgCXfWmBGTQFrAo8J2c9Mq0pAtiqzL1cJW/caGG4Te8QrHm5a4VA//QJFjcMFQXaAEXzarJw==; _gid=GA1.2.777159791.1542039644; ak_bmsc=82BB32FCE739F677698F5B5698E8B863685E642EB80500005AA8E95BE0026011~pll+Y0cnvz1jtXl47g5JNnUAt2Z/QRDCOXZiLpDJ1RKxfEP8Iz2TC49gxg0OvbXV4u9iTbrwkiet5CxG5kxUS3t6DgoSeErMy33a5aVoMndPgwq9ODz1gSRfb7eWgauJAMBxsGX2UQ9HamKWCkpkfnzXZvShWFjQMX4h5vWJWKpIOY6uPc6QLO91VK0Wlo3lGLJf+lcOg4ynxYv8iPIlHKgNtIjzidxbpe5IhSWVJH44JwEa6RcidPDUET1aBtwMRB; tis=EP117%3A1891%7CEP117%3A1891; _gat=1; bm_sv=73A262F052614595DFA94D531D14DCF1~GLs/UWOsaegwN1ckoFwmIvbO95bwHjo6/CARviHeTzJLafZewk7sJOz1cWvLXC00MAphEHsXvBIOlao6Pt8eBV1OX90XT13Z3n7bOEhL+mvUX+C9OSSLj9VdukMZBKmVmMFsCsO+FQC5+/nMfRXYPxRNWRZtvEsyzOtmqyhnhFE=',
			  'upgrade-insecure-requests': '1',
			  'User-Agent': str(ua.chrome)}
	response = requests.get(url, cookies=cookie)
	return str(response.content)


def write_to_file(file, collection):
	with open(file, 'w') as f:
		for item in collection:
			f.write("%s\n" % item)


def save_file_on_disc_from(url, directory):
	try:
		testfile = URLopener()
		testfile.retrieve(url, directory + str(url).split("00")[1].replace("/", ""))
	except Exception as exception:
		log.error('Unexpected exception: ' + str(exception))
