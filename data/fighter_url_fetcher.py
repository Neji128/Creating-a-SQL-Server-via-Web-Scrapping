import pickle
from bs4 import BeautifulSoup
import requests, re
import json

fighter_url_list = []
response = requests.get('http://www.ufcstats.com/statistics/fighters?char=a&page=all')
soup = BeautifulSoup(response.content, 'html.parser')

#targeting URLs that contain fighter data
fighters = soup.findAll('a', attrs={'href': re.compile('http:')})
for fighter in fighters:
    fighter_url_list.append(fighter.get('href'))

#removing duplicate URLs
fighter_url_list = list(set(fighter_url_list))

#removing invalid URLs
for url in fighter_url_list:
    if 'fighter-details' not in url:
        fighter_url_list.remove(url)
    elif 'statistics' in url:
        fighter_url_list.remove(url)
    elif len(url) < 56:
        fighter_url_list.remove(url)

#saving output for later manipulation
with open('fighter_url_list', 'wb') as f:
    pickle.dump(fighter_url_list, f)