import requests
import logging
from pathlib import Path

import croppola
import resize

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('log')
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('search_interior.log')
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
log.addHandler(file_handler)
log.addHandler(console_handler)


SEARCH_PHRASE = "bmw car interior"
SEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
KEY_1 = "36355d5593f34608aef0709daa7602a1"
KEY_2 = "1e79798d7a1147d688e23ec49a7fa32d"
TARGET_IMAGE_PATH = "D:\\car_photos\\inside"
LOOP_NUMBER = 15
OFFSET = 150


if __name__ == '__main__':
    headers = {"Ocp-Apim-Subscription-Key": KEY_1}
    image_num = 0
    for i in range(LOOP_NUMBER):
        params = {"q": SEARCH_PHRASE,
                  "license": "public",
                  "imageType": "photo",
                  "count": str(OFFSET),
                  "offset": str(OFFSET * i)}
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        image_urls = set([img["contentUrl"] for img in search_results["value"][:]])
        for image_url in image_urls:
            try:
                filename = str(image_url).split("/")[-1].split(".")[0] + '.jpg'
                filepath = TARGET_IMAGE_PATH + '/' + filename
                if Path(filepath).exists():
                    log.info('File: ' + filepath + ' exist. Skipping..')
                    continue
                log.info('Image: ' + str(image_num) + '/' + str(LOOP_NUMBER * OFFSET) + '  ' + filename)
                image = requests.get(image_url)
                f = open(filepath, 'wb')
                f.write(image.content)
                croppola.single_crop(filepath, filepath)
                resize.single_resize(filepath, filepath)
                image_num = image_num + 1
            except Exception as exception:
                log.error('Unexpected exception: ' + str(exception))