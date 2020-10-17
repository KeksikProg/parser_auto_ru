import requests # for get requests
from bs4 import BeautifulSoup # for parsing web pages
import csv # for tables
import subprocess # for automatic open csv file 

URL = 'https://auto.ru/voronezh/cars/chevrolet/used/'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.234', 'accept':'*/*'}
PAGES = 5 # For get 2 pages from web-site
FILE = 'cars.csv'






def get_html(url, params=None):
	# for get html code with web page (params for add in url page and td.)	
	r = requests.get(url, headers = HEADERS, params = params)
	r.encoding = 'UTF-8' 	# get html code from web page (headers so that the site does not think that the robot(but this is))
	return r








def get_price_or_city(item, price = True):
	if price:
		try:
			i = item.find('div', class_ = 'ListingItemPrice-module__content').get_text(strip = True).replace('\xa0', '')
			return i
		except AttributeError:
			try:
				i = item.find('div', class_ = 'ListingItemPrice-module__content').find('span').get_text(strip = True).replace('\xa0', '')
				return i
			except AttributeError:
				i = 'Уточняйте на сайте'
				return i
	else:
		try:
			i = item.find('span', class_ = 'MetroListPlace__regionName MetroListPlace_nbsp').get_text(strip = True)
		except AttributeError:
			i = 'Уточняйте на сайте'
		return i








def get_content(html):
	# for parsing web page

	soup = BeautifulSoup(html, 'html.parser') 	# this is parser for our page
	items = soup.find_all('div', class_ = 'ListingItem-module__main') 	# this is list with all car with class ListingItem-module__main
	cars = []

	for item in items:
		cars.append({
			'title' : item.find('h3', class_ = 'ListingItemTitle-module__container ListingItem-module__title').get_text(strip = True), # strip for delete space in text
			'link' : item.find('a', class_ = 'Link ListingItemTitle-module__link').get('href'),
			'price' : get_price_or_city(item),
			'city' : get_price_or_city(item, price = False)})
	return cars
		







def save_in_file(items, path):
	with open(path, 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Марка', 'Ссылка', 'Цена', 'Город'])
		for item in items:
			writer.writerow([item['title'], item['link'], item['price'], item['city']])








def parse():
	# func  where in call another all func
	
	html = get_html(URL)
	if html.status_code == 200:
		cars = []
		print('Подготовка в парсингу...')
		for page in range(1, PAGES + 1):
			print(f'	Страница {page} обрабатывается, всего {PAGES}...')
			html = get_html(URL, params = {'page' : page})
			cars.extend(get_content(html.text))
		print('Запись объектов в csv файл...')
		save_in_file(cars, FILE)
		print(f'Парсинг завершен! получено {len(cars)} объектов')
		subprocess.call(['libreoffice cars.csv'], shell = True)
	else:
		print('Ошибка, парсинг прерван, всего хорошего...')


parse()
