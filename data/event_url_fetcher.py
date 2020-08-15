import pickle
from bs4 import BeautifulSoup
import requests, re
import json

#creating a list of unique fighter URLs available on website
event_url_list = []

response = requests.get('http://www.ufcstats.com/statistics/events/completed?page=all')

soup = BeautifulSoup(response.content, 'html.parser')

#targeting URLs that contain fighter data

events = soup.findAll('a', attrs={'href': re.compile('http:')})

for event in events:

    event_url_list.append(event.get('href'))

#removing duplicate URLs

event_url_list = list(set(event_url_list))

#removing invalid URLs

for url in event_url_list:

    if 'event-details' not in url:

        event_url_list.remove(url)
    
for url in event_url_list:  

    if len(url) <  54:

        event_url_list.remove(url)

#saving output for later manipulation

with open('event_url_list', 'wb') as f:
    pickle.dump(event_url_list, f)