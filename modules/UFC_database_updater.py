import pickle
from bs4 import BeautifulSoup
import requests, re
import json
from datetime import datetime

#creating datetime object for date at script run

today = datetime.today()
current_date= today.strftime("%B %d, %Y")
current_datetime = datetime.strptime(current_date, "%B %d, %Y") 

#accessign event_url_list
with open('event_url_list', 'rb') as f:
    event_url_list = pickle.load(f)

#identifying events set for future dates

unadded_events = []

for url in event_url_list[18:]:

    response = requests.get(url)

    event_soup = BeautifulSoup(response.content, 'html.parser')

    date_holder = event_soup.findChildren('li', attrs={'class': re.compile('b-list__')})

    event_date = date_holder[0].text.split(':')[1].strip()

    event_datetime = datetime.strptime(event_date, "%B %d, %Y") 

    if event_datetime >= current_datetime:

        unadded_events.append(url)

print(unadded_events)