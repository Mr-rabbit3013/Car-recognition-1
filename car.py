import CarDownloader


e60_URL_PAGE = 'https://www.otomoto.pl/osobowe/bmw/seria-5/e60-2003-2010/-/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D%24page%3D2&page='
e60_CAR_PHOTOS_DIRECTORY = 'C:\\Users\\wieczoma\\Desktop\\e60\\original\\'

e90_URL_PAGE = 'https://www.otomoto.pl/osobowe/bmw/seria-3/e90-2005-2012/-/sedan/?search%5Bfilter_float_year%3Ato%5D=2008&search%5Bfilter_enum_damaged%5D=0&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D&page='
e90_CAR_PHOTOS_DIRECTORY = 'C:\\Users\\wieczoma\\Desktop\\e90\\original\\'

f10_URL_PAGE = 'https://www.otomoto.pl/osobowe/bmw/seria-5/f10-2009/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_float_door_count%3Afrom%5D=4&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D&page='
f10_CAR_PHOTOS_DIRECTORY = 'D:\\f10\\original\\'

f30_URL_PAGE = 'https://www.otomoto.pl/osobowe/bmw/seria-3/f30-2012/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D&page='
f30_CAR_PHOTOS_DIRECTORY = 'D:\\f30\\original\\'

f01_URL_PAGE = 'https://www.otomoto.pl/osobowe/bmw/seria-7/f01-2008-2015/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D&page='
f01_CAR_PHOTOS_DIRECTORY = 'D:\\f01\\original\\'


if __name__ == '__main__':
    downloader = CarDownloader.CarDownloader()
    downloader.download_images(f01_URL_PAGE, f01_CAR_PHOTOS_DIRECTORY)