import CarDownloader
import MobileDeCarDownloader

e60_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-5/e60-2003-2010/-/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D%24page%3D2&page='
e90_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-3/e90-2005-2012/-/sedan/?search%5Bfilter_float_year%3Ato%5D=2008&search%5Bfilter_enum_damaged%5D=0&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D&page='
f10_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-5/f10-2009/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_float_door_count%3Afrom%5D=4&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D&page='
f30_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-3/f30-2012/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D&page='
f01_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-7/f01-2008-2015/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=%3D&page='
e46_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-3/e46-1998-2007/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bcountry%5D=%3D&page='
f20_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-1/f20-2011/compact/?search%5Bfilter_enum_damaged%5D=0&search%5Bcountry%5D=%3D&page='
e87_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-1/e87-2004-2013/compact/?search%5Bfilter_enum_damaged%5D=0&search%5Bcountry%5D=%3D&page='
g30_URL = 'https://www.otomoto.pl/osobowe/bmw/seria-5/g30-2017/sedan/?search%5Bfilter_enum_damaged%5D=0&search%5Bcountry%5D=%3D&page='
e83_URL = 'https://www.otomoto.pl/osobowe/bmw/x3/e83-2003-2010/?search%5Bfilter_enum_damaged%5D=0&search%5Bcountry%5D=%3D&page='
f15_URL = 'https://www.otomoto.pl/osobowe/bmw/x5/f15-2013/?search%5Bfilter_float_year%3Ato%5D=2016&search%5Bfilter_enum_damaged%5D=0&search%5Bcountry%5D=%3D&page='
e70_URL = 'https://www.otomoto.pl/osobowe/bmw/x5/e70-2006-2013/?search%5Bfilter_enum_damaged%5D=0&search%5Bcountry%5D=%3D&page='

# replace pgn: with %%%
f32_URL = 'https://www.mobile.de/pl/samochod/bmw-seria-4/vhc:car,pgn:%%%,pgs:50,ms1:3500_-53_,dmg:false,vcg:sportscar'

CAR_PHOTOS_DIRECTORY = 'C:\\Users\\Mateusz\\Desktop\\f32\\'

if __name__ == '__main__':
    downloader = MobileDeCarDownloader.CarDownloader()
    downloader.download_images(f32_URL, CAR_PHOTOS_DIRECTORY)