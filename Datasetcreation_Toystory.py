from distutils.log import info
from bs4 import BeautifulSoup as bs
import requests

# Load the web page
r = requests.get('https://en.wikipedia.org/wiki/Toy_Story_3')

# Convert to Beautifulsoup Object
soup = bs(r.content)

# find the info box in the web page
# find info box first
info_box = soup.find(class_='infobox vevent')
# Prettifu command help to pretify HTML
# print(info_box.prettify())
# find table row
info_row = info_box.find_all('tr')
for row in info_row:
    # print(row.prettify())
    pass

def get_content_value(row_data):
    if row_data.find('li'):
        return [li.get_text(' ',strip=True).replace('\xa0',' ') for li in row_data.find_all('li')]
    else:
        return row_data.get_text(' ',strip=True).replace('\xa0',' ')

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



print(movie_info)