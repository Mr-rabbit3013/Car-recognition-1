import logging
import re
from urllib.request import Request, urlopen, URLopener

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('log')
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('e60.log')
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
log.addHandler(file_handler)
log.addHandler(console_handler)


class CarDownloader:

    """Class for downloading images from OtoMoto"""
    def __init__(self):
        self

    def download_images(self, url, directory):
        car_counter = 1
        webpage_source = read_html_page_source(url + '1')
        car_pages = read_car_pages(webpage_source)
        for i in range(1, int(car_pages)):
            webpage_source = read_html_page_source(url + str(i))
            car_links = get_all_car_links_from(webpage_source)
            log.info('Downloading photos from page: ' + str(i))
            for car_link in car_links:
                log.info('Downloading photos from car number: ' + str(car_counter))
                car_counter += 1
                photo_links = get_photo_links_from(car_link)
                for photo_url in photo_links:
                    save_file_on_disc_from(photo_url, directory)


def read_car_pages(webpage_source):
    RESULT_COUNT_PHRASE = '"result_count":'
    first_index = webpage_source.find(RESULT_COUNT_PHRASE)
    last_index = webpage_source.find(',', first_index)
    count = webpage_source[first_index + len(RESULT_COUNT_PHRASE): last_index]
    return int(int(count) / 32)


def read_html_page_source(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage_source = urlopen(req).read()
    return webpage_source.decode("utf8")


def get_all_car_links_from(webpage_source):
    OFFER_TITLE_LINK_PHRASE = 'class="offer-title__link"'
    link_indexes = [m.start() for m in re.finditer(OFFER_TITLE_LINK_PHRASE, webpage_source)]
    links = set()
    for i in range(0, len(link_indexes)):
        link = get_single_link_from(webpage_source[link_indexes[i] + len(OFFER_TITLE_LINK_PHRASE):])
        links.add(link)
    return links


def get_single_link_from(webpage_source):
    START_LINK_PHRASE = 'href="'
    first_link_index = webpage_source.find(START_LINK_PHRASE) + len(START_LINK_PHRASE)
    last_link_index = webpage_source[first_link_index: 300].find('"') + first_link_index
    return webpage_source[first_link_index: last_link_index]


def get_photo_links_from(url):
    webpage_source = read_html_page_source(url)
    PHOTO_URL_START_PHRASE = 'data-tracking="gallery_open" src="'
    link_indexes = [m.start() for m in re.finditer(PHOTO_URL_START_PHRASE, webpage_source)]
    links = set()
    for i in range(0, len(link_indexes)):
        link = get_single_photo_link_from(webpage_source[link_indexes[i] + len(PHOTO_URL_START_PHRASE):])
        links.add(link)
    return links


def get_single_photo_link_from(webpage_source):
    last_link_index = webpage_source[: 300].find('"')
    return webpage_source[: last_link_index]


def save_file_on_disc_from(url, directory):
    try:
        testfile = URLopener()
        testfile.retrieve(url, directory + '-' + str(url).split("/")[-1])
    except Exception as exception:
        log.error('Unexpected exception: ' + str(exception))
