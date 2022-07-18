from distutils.log import info
from bs4 import BeautifulSoup as bs
from numpy import tile
import requests

def get_content_value(row_data):
    if row_data.find('li'):
        return [li.get_text(' ',strip=True).replace('\xa0',' ') for li in row_data.find_all('li')]
    else:
        return row_data.get_text(' ',strip=True).replace('\xa0',' ')

def get_info_box(url):
    r = requests.get(url)
    soup = bs(r.content)
    info_box = soup.find(class_='infobox vevent')
    info_row = info_box.find_all('tr')
    
    # Starting save Dict
    movie_info = {}

    # get index of rows (get correct info we need)
    for index , row in enumerate(info_row):
        # index == 0 means that is title
        if index == 0:
            movie_info['title'] = row.find('th').get_text(' ',strip=True)
        elif index == 1:
            continue
        else:
            content_key = row.find('th').get_text(' ',strip=True)
            content_value = get_content_value(row.find('td'))
            movie_info[content_key] = content_value

    return movie_info




r = requests.get('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films')

soup = bs(r.content)

movie_info = soup.select('.wikitable.sortable i a')

base_url = 'https://en.wikipedia.org'

movie_info_list = []

for row in movie_info:
    if len(row) == 10:
        break
    try:
        ref_path = row['href']
        full_url = base_url + ref_path
        title = row['title']
        movie_info_list.append(get_info_box(full_url))

    except:
        pass

print(movie_info_list)
