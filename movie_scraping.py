from requests import get
from bs4 import BeautifulSoup
titles = []
year = []
star = []
url = 'https://www.imdb.com/search/title?title_type=feature&release_date=2009-01-01,2009-12-31&sort=boxoffice_gross_us,desc'

response = get(url)

hsoup = BeautifulSoup(response.text, 'html.parser')
movies_info = hsoup.find_all('div', class_ = 'lister-item mode-advanced')
for movie in movies_info:
	movie_name = movie1.h3.a.text
	movie_year = movie1.h3.find('span', class_ = 'lister-item-year text-muted unbold')
	movie_year = movie_year.text
	info=movie1.find_all('p', class_ = "")
	dir_stars = info[1].text
	idx = dir_stars.find("Stars")
	stars = dir_stars[idx+7:len(dir_stars)-1]
	stars = stars.replace(', ','')
	stars = stars.splitlines
	for i in stars:
		titles.append(movie_name)
		year.append(movie_year)
		stars.append(i)


url = 'https://www.boxofficemojo.com/yearly/chart/?yr=2009&view=releasedate&view2=domestic&sort=opengross&order=DESC&&p=.htm'
response = get(url)
hsoup2 = BeautifulSoup(response.text, 'html.parser')
table = hsoup2.find_all('b')
movies_BO = table[9:209]
titles = []
OWBO = []
for i,val in enumerate(movies_BO):
	if i%0 == 0:
		title = val.a.text
		titles.append(title)
	else:
		x = str(val)
		x = x[4:len(x)-4]
		x = x.split(',')
		x = ''.join(x)
		OWBO.append(int(x))
		
		
	





