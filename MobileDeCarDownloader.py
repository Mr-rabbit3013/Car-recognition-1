import logging
import re
import requests
from urllib.request import Request, urlopen, URLopener

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

f32_URL = 'https://www.mobile.de/pl/samochod/bmw-seria-4/vhc:car,%%%,pgs:10,ms1:3500_-53_,frx:2017,dmg:false,vcg:sportscar'


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
				car_links = get_links_from(car_page_fragments)
				log.info('Downloading photos from page: ' + str(car_pager))
				for car_link in car_links:
					car_webpage = read_html_page_source(car_link)
					car_photo_urls = get_all_car_photo_links_from(car_webpage)
					for car_photo_url in car_photo_urls:
						log.info('Downloading photos from car number: ' + str(car_counter))
						car_counter += 1
						save_file_on_disc_from(car_photo_url, directory)


def get_all_car_photo_links_from(webpage_source):
	CAR_PHOTOS_LINKS_PREFIX = '<div class="js-gallery-img-wrapper slick-slide slick-current slick-active" data-slick-index="0" aria-hidden="false" tabindex="0" role="tabpanel" id="slick-slide10" aria-describedby="slick-slide-control10" style="width: 800px;">'
	CAR_PHOTOS_LINKS_SUFFIX = 'style="width: 800px;"><div class="gallery-bg js-gallery-img"><div class="lightboxlatest-ad-box hidden-s hidden-m"><div id=""></div></div></div></div></div>'
	LINK_PREFIX = 'src="'
	LINK_SUFFIX = '">'
	pattern = re.compile(CAR_PHOTOS_LINKS_PREFIX + '(.*)' + CAR_PHOTOS_LINKS_SUFFIX)
	link_pattern = re.compile(LINK_PREFIX + '(.*)' + LINK_SUFFIX)
	return link_pattern.findall(pattern.findall(webpage_source)[0])


def get_links_from(car_source_fragments):
	LINK_PREFIX = 'href="'
	LINK_SUFFIX = '.html">'
	links = set()
	pattern = re.compile(LINK_PREFIX + '(.*)' + LINK_SUFFIX)
	for i in range(len(car_source_fragments)):
		for link in pattern.findall(car_source_fragments):
			links.add(MAIN_URL + link[6:])
	return links


def get_all_car_page_fragments(webpage_source):
	CAR_FRAGMENT_PREFIX = '<a class="vehicle-data'
	CAR_FRAGMENT_SUFFIX = '</a>'
	pattern = re.compile(CAR_FRAGMENT_PREFIX + '(.*)' + CAR_FRAGMENT_SUFFIX)
	return pattern.findall(webpage_source)


def check_page(webpage_source):
	ERROR_MESSAGE_PREFIX = '<p class="js-error-message u-text-center">'
	if ERROR_MESSAGE_PREFIX not in webpage_source:
		return True
	else:
		return False


def read_html_page_source(url):
	cookie = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			  'accept-encoding': 'gzip, deflate, br',
			  'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,pt;q=0.6',
			  'cookie': 'sorting_e=""; show_qs_e=vhc%3Acar%2Cms1%3A3500_-53_; mobile.LOCALE=de; vi=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaWQiOiI2MThiYzBlNy0wNzAwLTRiYTMtOGQ2OS1mMmZkMDQ1Y2M3MTgiLCJhdWQiOltdLCJpYXQiOjE1NDE1NzYzMzR9.6W3mN_C5U2gbXkSFbWm99XVwiTnsWwJuZiADHNIYhZg; _ga=GA1.2.495630715.1541576336; _gid=GA1.2.279745817.1541576336; optimizelyEndUserId=oeu1541576335833r0.33012600410861226; visited=1; axd=1001316771521130073; mdeConsentData=BOW2eGqOW2eGqB9ABBDEBa-AAAJw-BOgACAAkABgA1gBuAL8AYQBigDIAM0AaABpgDYAOcAdwB4AD1AHwAhoBEAEjAJMApYBTgFXAK0Ar4BYgFpALYAuYBeAGXAM0AzoBoAG0AN2Ab4B0QDqAPaAfACFQEMAQ6AiACNQEcAR2Aj4CRwElASeAlICVwEtATCAmgCcQE6AUEAocBRQFGgKQApYBTYCngKrAVcBW4CugK-AWKAsoC1QFtAW6AuAC4gFzgLqAvUBfAF-gMAAwMBgwGIgMUAxcBjQGOAMhAZIBlYDLgM1AZwBnYDPgNAAaKA0oDXwGyAbQA2wBuIDdAN5Ab8BwgDiQHGAceA5QDlwHNAc6A6ADqwHZAdwA7wB4ADyAHmgPQA9YB7YD3gPjAfMB9AD7CcP; mdeCustomConsentData=25; _abck=D40AE9EB20F0D4EC1D82D077F4152725685E64373E3100008F96E25B8A016433~0~pJGUz23KSDuaXNklYhrNtDKX8LcA99Pjwc70oDhLBS8=~-1~-1; bm_sz=29CF2042D8C4AAF3A78558F7F72397B6~QAAQN2ReaMb4ndJmAQAAYiXY7lueAriKS1SztQeNqnN7nqjq/yVlenXhgR+w79zhiz1vomqNkyqDp2+a1YdUMFuSycZMjzsQ61CVidTWNQhpZuQyhQ2MjuStpDQxJAQ9FhYdFIXIlS+e9POFBybFWcOVUm/hfYt0ZI3Xfh3gh+Kqm42kQZoPKWnOMuUm; via=google; _gat=1; bm_sv=2C5397CFEA22094BB409C1ED1FB3B7D6~3pE3wPt8df+Wd4cEryKeZgGJ5xEv6D5UuY2QJsftb+plemdMN4kmKKHrKMaaHtzPury8ahHwqiXGx5YHoIGUfJPWlDmNhanhN5jH/48thy2SubBJkeyQblMrjnHitlRbWtSy0WyjX0lrr8NTXBKoTg==; ak_bmsc=1AF5A88A0AEF905D02EB3F670038877802121D25E6210000C12DE35BEFA14A22~plWwmgDKiKF5nMNWrP/DLT+dCgsX8u96wcKRrn62iUtRPqgK2zMXdmts7mHjWh8Pp4nOyhCXUaZrUagAKNUc3olWKYvSwX+IMlp1j73ujf9kxA8W+BgKV4E7klYeLvXnd2SERyc+fqSkkTadfzKyjzhDUAHRGHep9K0PkMVSbQjy+O08UiXwSs7Iim+KYebUEZoP/jijx4BQdLxOuYoKO4XyEzI7PFqEqHU58a05/8U/EpGzi0Tjf2QExX8+pTRcAR',
			  'upgrade-insecure-requests': '1',
			  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
	response = requests.get(url, cookies=cookie)
	return str(response.content)


def save_file_on_disc_from(url, directory):
	try:
		testfile = URLopener()
		testfile.retrieve(url, directory + '-' + str(url).split("/")[-1])
	except Exception as exception:
		log.error('Unexpected exception: ' + str(exception))
