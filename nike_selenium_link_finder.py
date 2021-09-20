from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

url = 'https://www.nike.com/w/mens-running-shoes-37v7jznik1zy7ok'

print('<<<--- Driver opened --->>>')
driver = webdriver.Chrome()
print('<<<--- Getting:', url,'--->>>')
driver.get(url)

last_height = driver.execute_script('return document.body.scrollHeight')

while True:
	# break
	print('--- Scrolling... ---')
	driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
	print('--- Sleeping... ---')
	time.sleep(20)
	new_height = driver.execute_script('return document.body.scrollHeight')
	if new_height == last_height:
		break
	last_height = new_height
	print('Scroll Height:', last_height)
	

soup = BeautifulSoup(driver.page_source, 'lxml')
product_cards = soup.find_all('div', class_='product-card css-1lukt7x css-z5nr6i css-11ziap1 css-14d76vy css-dpr2cn product-grid__card')

df = pd.DataFrame({
	'Title': [''],
	'Price': [''],
	'Link': [''],
	})

counter = 1
for card in product_cards:
	try:
		link = card.find('a', class_='product-card__link-overlay').get('href')
		title = card.find('div', class_='product-card__title').text
		price = card.find('div', class_='product-price css-11s12ax is--current-price').text
		print(f'[{counter}]', link[:200], title, price)
		counter += 1
		df = df.append({
		'Link': link,
		'Title': title,
		'Price': price,
		}, ignore_index=True)
	except Exception as e:
		print(f'--- {e} ---')
	# break

print('--- Creating Excel ---')
df.to_excel('nike primary.xlsx')

time.sleep(2)
driver.close()