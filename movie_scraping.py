from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn
import numpy as np
start_time = time()
requests =  0
titles = []
year = []
star = []
imdb_second_page = '&start=51&ref_=adv_nxt'
iter1 = [1,2]
imdb_year_url = [str(i) for i in range(2009, 2019)]
for year_url in imdb_year_url:
	for x in iter1:
		if x == 1:
			url = 'https://www.imdb.com/search/title?title_type=feature&release_date='+year_url+'-01-01,'+year_url +'-12-31&sort=boxoffice_gross_us,desc'
		if x == 2:
			url = 'https://www.imdb.com/search/title?title_type=feature&release_date='+year_url+'-01-01,'+year_url +'-12-31&sort=boxoffice_gross_us,desc'+ imdb_second_page
		response = get(url)
		#pause loop for random interval between 10 and 15 to space out url requests
		sleep(randint(10,15))
		#monitor requests
		requests += 1
		elapsed_time = time() - start_time
		print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
		#clear output so memory isn't unnecessarily used, but wait to clear until a new output is present
		clear_output(wait = True)
		#make sure we are scraping correctly
		if response.status_code != 200:
			warn('Request: {}; Status code: {}'.format(requests, response.status_code))
		#break loop if make more requests than necessary
		if requests > len(iter1)*len(imdb_year_url):
			warn('Number of requests  has exceeded expectations')
			break
		hsoup = BeautifulSoup(response.text, 'html.parser')
		movies_info = hsoup.find_all('div', class_ = 'lister-item mode-advanced')
		for movie in movies_info:
			movie_name = movie.h3.a.text
			movie_year = movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
			movie_year = movie_year.text
			if movie_year == '':
				movie_year = int(year_url)
			else:
				movie_year = int(movie_year[-5:-1])
			info=movie.find_all('p', class_ = "")
			dir_stars = info[1].text
			idx = dir_stars.find("Stars")
			stars = dir_stars[idx+7:len(dir_stars)-1]
			stars = stars.replace(', ','')
			stars = stars.split('\n')
			for i in stars:
				titles.append(movie_name)
				year.append(movie_year)
				star.append(i)


movie_stars_df = pd.DataFrame({'title': titles,
				'year': year,
				'stars': star})

titles1 = []
OWBO = []
start_time=time()
requests = 0
bom_year_url = [str(i) for i in range(2009, 2019)]
for year_url in bom_year_url:
	for x in iter1:
		if x == 1:
			url = 'https://www.boxofficemojo.com/yearly/chart/?yr='+ year_url+'&view=releasedate&view2=domestic&sort=opengross&order=DESC&&p=.htm'
		if x == 2:
			url = 'https://www.boxofficemojo.com/yearly/chart/?page='+ str(x)+'&view=releasedate&view2=domestic&yr='+ year_url +'&sort=opengross&p=.htm'
		response = get(url)
#pause loop for random interval between 10 and 15 to space out url requests
		sleep(randint(10,15))
		#monitor requests
		requests += 1
		elapsed_time = time() - start_time
		print('Request:{}; Frequancy: {} requests/s'.format(requests, requests/elapsed_time))
		#clear output so memory isn't unnecessarily used, but wait to clear until a new output is present
		clear_output(wait = True)
		#make sure we are scraping correctly
		if response.status_code != 200:
			warn('Request: {}; Status code: {}'.format(requests, response.status_code))
		#break loop if make more requests than necessary
		if requests > len(iter1)*len(bom_year_url):
			warn('Number of requests  has exceeded expectations')
			break
		hsoup2 = BeautifulSoup(response.text, 'html.parser')
		table = hsoup2.find_all('b')
		movies_BO = table[9:209]

		for i,val in enumerate(movies_BO):
			if i%2 == 0:
				title = val.a.text
				titles1.append(title)
			else:
				x = str(val)
				x = x[4:len(x)-4]
				x = x.split(',')
				x = ''.join(x)
				OWBO.append(int(x))
		
movie_OWBO = pd.DataFrame({'title': titles1,
				'OWBO': OWBO})

		
	





