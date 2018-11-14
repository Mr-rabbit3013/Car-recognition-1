import logging
import re
from urllib.request import URLopener
from pathlib import Path

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
    images = re.compile(u"<div class=\"js-image-data\" data-title(.+?)<\/div>", re.UNICODE)
    images = images.findall(webpage_source)[0]
    links = re.compile(u"https:(.+?).JPG", re.UNICODE)
    links = links.findall(images)
    update_pages = ['https:' + link + '.JPG' for link in links]
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
    ua = UserAgent()
    cookie = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'accept-encoding': 'gzip, deflate, br',
              'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,pt;q=0.6',
              'cookie': 'sorting_e=""; show_qs_e=vhc%3Acar%2Cms1%3A3500_-53_; mobile.LOCALE=de; vi=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaWQiOiJkM2NjODEwZC1lMjY0LTQyM2ItYmQ0OC0yMTczODZkNzUyZmYiLCJhdWQiOltdLCJpYXQiOjE1NDE1Mzg1MDB9.lY_yHXmzxPDWAnsdHVqSnyfhHpaTn03-J9W-KdCbwIE; _ga=GA1.2.2040238419.1541538502; __gads=ID=03706eb646499294:T=1541538501:S=ALNI_MbLP8npOqdXGb3FBKZ7eWw6mDcLNA; optimizelyEndUserId=oeu1541538504530r0.5612834202323105; visited=1; _abck=3C05924E088668DEE73C9D69CED42758685E64373E310000C402E25B3C43A239~0~uNZrWf7ouRh1FdBfnOvs4EIdGxtj8EJbN09rS257yco=~-1~-1; axd=1002018852208240172; cto_axid=HJwid2y5JJ3c_LtJdklIHl34dFtyxT_v; mdeConsentData=BOW1BvmOW1BvmB9ABBDEBa-AAAJw-BOgACAAkABgA1gBuAL8AYQBigDIAM0AaABpgDYAOcAdwB4AD1AHwAhoBEAEjAJMApYBTgFXAK0Ar4BYgFpALYAuYBeAGXAM0AzoBoAG0AN2Ab4B0QDqAPaAfACFQEMAQ6AiACNQEcAR2Aj4CRwElASeAlICVwEtATCAmgCcQE6AUEAocBRQFGgKQApYBTYCngKrAVcBW4CugK-AWKAsoC1QFtAW6AuAC4gFzgLqAvUBfAF-gMAAwMBgwGIgMUAxcBjQGOAMhAZIBlYDLgM1AZwBnYDPgNAAaKA0oDXwGyAbQA2wBuIDdAN5Ab8BwgDiQHGAceA5QDlwHNAc6A6ADqwHZAdwA7wB4ADyAHmgPQA9YB7YD3gPjAfMB9AD7CcP; mdeCustomConsentData=25; GED_PLAYLIST_ACTIVITY=W3sidSI6IlBFL1QiLCJ0c2wiOjE1NDE1MzkzMDcsIm52IjoxLCJ1cHQiOjE1NDE1MzkzMDYsImx0IjoxNTQxNTM5MzA2fV0.; bm_sz=7ADFEF820ADF0B581A6E846D98BDE950~QAAQN2ReaOoFrdJmAQAAErnQDVY35dMknLbMy3tltWW8W5WPFg3i6a+bnmyGiLnwxy/Jz9ZS7PmMbTH953mxSArLyApCdSSFiEODMxkcC8Y0wJh8mYXJIQg5duwL16N2XJMKRcWUhfPiQiD6MY7XR773zulKPdDUDVuudFBfJcgGBaenTaQUjBgZLWVLxQ==; _gid=GA1.2.1081161282.1542125045; ak_bmsc=623CEF43BB554C8FDFB1E105B3145704685E642EB80500000915EB5B4505672C~plCR1b79+SyTql/Hgv5HE8QI7p2/f+8T39cafcgAqd8MXMsi/3yvx6Ip2wy2PJ46ajyxjaPOFYnSbpQEuVtqUcpsb0y82VSk/zHeFroX3lNMiKRrr468U6Ri0YvydAcV8ZoZyYhrx1NQrCu7mqMkCjk4M321vEH+OMPN9sbf33qw2MfmPCvQ8dhDNVjsUE3WDscRJuJqfgmwOfVugj9l8Ix9SBXE9BJc++BxqUdJQEsp74QktCTd3zEOCBpTI7H5bu; bm_sv=F66A3D9C1589BDF34F6D513E863C4D96~GLs/UWOsaegwN1ckoFwmIgv/aE2KbEdCOJpiNO1fiD88V7BFT4JALlDkQjSazHO9UyqnfwZDiB8cuh8Qp6IN5k/UJfIkqdy6Zwd+kWNYNGbZgr/uux2aBlzkGuCRRLUCsOOilnwNQTkY25+hJJ6P8081pQAMDAa1Z09xk6E0sWI=',
              'upgrade-insecure-requests': '1',
              'User-Agent': str(ua.chrome)}
    response = requests.get(url, cookies=cookie)
    return str(response.text)


def write_to_file(file, collection):
    with open(file, 'w') as f:
        for item in collection:
            f.write("%s\n" % item)


def save_file_on_disc_from(url, directory):
    try:
        testfile = URLopener()
        url = str(url).replace("\\u003d", '=')
        filename = directory + str(url).split("00")[1].replace("/", "")
        if Path(filename).exists():
            return
        testfile.retrieve(url, filename)
    except Exception as exception:
        log.error('Unexpected exception: ' + str(exception))
