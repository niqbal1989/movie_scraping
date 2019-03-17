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
movie_stars_df.to_csv('movie_stars.csv')
#read in data if you already scraped but lost your environment because our computer screwed up
#movie_stars_df = pd.read_csv('movie_stars.csv', index_col=0)

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
		print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
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
				if '(' in title:
					title = title.split(' (')[0]
					titles1.append(title)
				else:
					titles1.append(title)				
			else:
				x = str(val)
				x = x[4:len(x)-4]
				x = x.split(',')
				x = ''.join(x)
				OWBO.append(int(x))
		
movie_OWBO = pd.DataFrame({'title': titles1,
				'OWBO': OWBO})
movie_OWBO.to_csv('movie_OWBO.csv')

#movie_OWBO = pd.read_csv('movie_OWBO.csv', index_col = 0)

movie_stars_df['lowertitle'] = movie_stars_df['title'].str.lower()
movie_OWBO['lowertitle'] = movie_OWBO['title'].str.lower()
movie_stars_OWBO = movie_stars_df.merge(movie_OWBO, how= 'left', left_on='lowertitle', right_on = 'lowertitle')
movie_stars_OWBO.isnull().astype(int).sum()
#identify missing values
movie_stars_OWBO[movie_stars_OWBO.duplicated(['stars', 'OWBO'])]
missing_values = movie_stars_OWBO[movie_stars_OWBO['OWBO'].isnull()]
missing_titles = missing_values['title_x']
missing_titles = missing_titles.unique()
#movie_stars_OWB02 = movie_stars_df.merge(movie_OWBO, how= 'left', left_on='title', right_on = 'title')
#movie_stars_OWB02.isnull().astype(int).sum()
movie_OWBO.str.startswith('Fast')
movie_OWBO = movie_OWBO.replace('Fast and Furious', 'Fast & Furious')
movie_OWBO = movie_OWBO.replace('Hannah Montana The Movie', 'Hannah Montana: The Movie')
movie_OWBO = movie_OWBO.replace('The Taking of Pelham 1 2 3', 'The Taking of Pelham 123')
movie_OWBO = movie_OWBO.replace('Bruno', 'Brüno')
movie_OWBO = movie_OWBO.replace("Marvel's The Avengers", 'The Avengers')
movie_OWBO = movie_OWBO.replace("My Bloody Valentine 3-D", 'My Bloody Valentine')
movie_OWBO = movie_OWBO.replace('Precious: Based on the Novel "Push" by Sapphire', 'Precious')
movie_OWBO = movie_OWBO.replace('Harry Potter and the Deathly Hallows Part 1', 'Harry Potter and the Deathly Hallows: Part 1')
movie_OWBO = movie_OWBO.replace('Harry Potter and the Deathly Hallows Part 2', 'Harry Potter and the Deathly Hallows: Part 2')
movie_stars_df = movie_stars_df.replace('Tron', 'Tron Legacy')
movie_OWBO = movie_OWBO.replace('Knight & Day', 'Knight and Day')
movie_OWBO = movie_OWBO.replace('Saw 3D', 'Saw 3D: The Final Chapter')
movie_OWBO = movie_OWBO.replace('Step Up 3-D', 'Step Up 3D')
movie_OWBO = movie_OWBO.replace('Love and Other Drugs', 'Love & Other Drugs')
movie_stars_df = movie_stars_df.replace('The Twilight Saga: Breaking Dawn - Part 1', 'The Twilight Saga: Breaking Dawn Part 1')
movie_stars_df = movie_stars_df.replace('The Twilight Saga: Breaking Dawn - Part 2', 'The Twilight Saga: Breaking Dawn Part 2')
movie_stars_df = movie_stars_df.replace('X: First Class', 'X-Men: First Class')
movie_OWBO = movie_OWBO.replace('Gnomeo and Juliet', 'Gnomeo & Juliet')
movie_OWBO = movie_OWBO.replace('Battle: Los Angeles', 'Battle Los Angeles')
movie_OWBO = movie_OWBO.replace('Spy Kids: All the Time in the World', 'Spy Kids 4: All the Time in the World')
movie_OWBO = movie_OWBO.replace("Tyler Perry's Madea Goes to Jail", 'Madea Goes to Jail')
movie_OWBO = movie_OWBO.replace("Tyler Perry's I Can Do Bad All By Myself", 'I Can Do Bad All by Myself')
movie_OWBO = movie_OWBO.replace("Tyler Perry's Why Did I Get Married Too?", 'Why Did I Get Married Too?')
movie_OWBO = movie_OWBO.replace("Tyler Perry's Madea's Big Happy Family", "Madea's Big Happy Family")
movie_OWBO = movie_OWBO.replace("Tyler Perry's Madea's Witness Protection", "Madea's Witness Protection")
movie_OWBO = movie_OWBO.replace("Tyler Perry's A Madea Christmas", 'A Madea Christmas')
movie_OWBO = movie_OWBO.replace("Tyler Perry's Temptation: Confessions of a Marriage Counselor", 'Temptation: Confessions of a Marriage Counselor')
movie_OWBO = movie_OWBO.replace("Tyler Perry's Boo 2! A Madea Halloween", 'Boo 2! A Madea Halloween')
movie_OWBO = movie_OWBO.replace("Tyler Perry's Acrimony", 'Acrimony')
movie_OWBO = movie_OWBO.replace("Dr. Seuss' The Lorax", 'The Lorax')
movie_OWBO = movie_OWBO.replace("Dr. Seuss' The Grinch", 'The Grinch')
movie_OWBO = movie_OWBO.replace('MIB 3', 'Men in Black 3')
movie_OWBO = movie_OWBO.replace('Les Miserables', 'Les Misérables')
