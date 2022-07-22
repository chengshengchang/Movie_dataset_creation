from distutils.log import info
from re import L
from tkinter.ttk import Style
from bs4 import BeautifulSoup as bs
from numpy import tile
import requests
import json
import pandas as pd


# Save and Reload data (json format)
def save_data(title, data):
    with open(title , 'w',encoding='utf-8') as f:
        json.dump(data , f , ensure_ascii=False , indent=2)

def load_data(title):
    with open(title, encoding='utf-8') as f:
        return json.load(f)

def get_content_value(row_data):
    if row_data.find('li'):
        return [li.get_text(' ',strip=True).replace('\xa0',' ') for li in row_data.find_all('li')]
    elif row_data.find('br'):
        # row_data.stripped_strings means that strip those under the row_data tag<a> text
        return [text for text in row_data.stripped_strings]
    else:
        return row_data.get_text(' ',strip=True).replace('\xa0',' ')

def clean_tags(soup):
    for tags in soup.find_all(['span','sup']):
        tags.decompose()


def get_info_box(url):
    r = requests.get(url)
    soup = bs(r.content)

    clean_tags(soup)

    info_box = soup.find(class_='infobox vevent')
   
    info_row = info_box.find_all('tr')

    # Starting save Dict
    movie_info = {}

    # get index of rows (get correct info we need)
    for index , row in enumerate(info_row):
        # index == 0 means that is title
        if index == 0:
            movie_info['title'] = row.find('th').get_text(' ',strip=True)
        else:
            header = row.find('th')
            exception = row.find(class_='infobox-header')
            if header and not exception:
                content_key = row.find('th').get_text(' ',strip=True)
                content_value = get_content_value(row.find('td'))
                movie_info[content_key] = content_value

    return movie_info


# test_info = get_info_box('https://en.wikipedia.org/wiki/The_Twilight_Zone_Tower_of_Terror#Film_adaptation')
# save_data('test.json',test_info)


r = requests.get('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films')

soup = bs(r.content)

movie_info = soup.select('.wikitable.sortable i a')

base_url = 'https://en.wikipedia.org'

movie_info_list = []

for index,row in enumerate(movie_info):
    # not run again cuz I already save to json file
    break
    if index % 10 == 0:
        print('Progress => ', index)
    try:
        ref_path = row['href']
        full_url = base_url + ref_path
        title = row['title']
        movie_info_list.append(get_info_box(full_url))

    except Exception as e:
        print(e)
        print(row.get_text())




# save_data('movie_info_list.json', movie_info_list)



# clean our data
movie_info_list = load_data('movie_info_list.json')

# Subtasks
# Clean up Reference [1] [2] -> revise def get_info_box(): -> done
# Split up the long strings -> done
# Clean up NoneType and Error wiki page -> done



# Convert running time into an integer -> done

df_movie_info_list = pd.DataFrame.from_dict(movie_info_list)


# input running time will be str
def running_time_to_int(runningtime):
    # Case 2
    if isinstance(runningtime , list):
        return int(runningtime[0].split(' ')[0])
    else:
        entry = str(runningtime).split(' ')[0]
        if '-' in entry:
            entry = entry[:2]
        return  entry

for index , row in enumerate(df_movie_info_list['Running time']):
    if type(row) != float:
        df_movie_info_list.loc[index,'Movie minutes (int)']= running_time_to_int(row)
    else:
        df_movie_info_list.loc[index,'Movie minutes (int)'] = None


# print(df_movie_info_list['Movie minutes (int)'])
# Convert Dates into datatime object
# Convert Budget & Box office to numbers

