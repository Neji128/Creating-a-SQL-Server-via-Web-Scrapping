import pickle
import requests, re
from bs4 import BeautifulSoup
import json
import pandas as pd

with open('fighter_url_list', 'rb') as f:
    fighter_url_list = pickle.load(f)

#Generating Soup Lists

def fighter_soup_generator(url):
    '''Meant to parse any url via beuatiful soup
    
    Args:
        url(str): url that will be parsed using BeautifulSoup'''
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    return soup

#generating a soup_list to limit requests
fighter_url_soup_list = list(map(fighter_soup_generator, fighter_url_list))

def base_stats_soup_generator(soup):
    '''Meant to identiy statistics in the context of UFC Stats urls.
    
    Args:
        
        soup(BeautifulSoup object) : must be an unaltered soup'''
    
    base_stats = soup.findChildren('li', attrs={'class': re.compile('b-list')})
    
    return base_stats

#generating a list of parsed soup objects

fighter_stats_objects = list(map(base_stats_soup_generator, fighter_url_soup_list))

# Construction of Fighter Physical Statistics DataFrame 

def fighter_name(soup):
    '''Identifies fighter history to be parsed.

    Args:
    
        soup(BeautifulSoup object): BeautifulSoup object must originate from a urls hosting fighter profiles'''
    
    name = soup.find('span', attrs={'class': re.compile('b-content__title-highlight')})
    
    return name.text.strip()

def fighter_record(soup):
    
    record = soup.findChildren('span', attrs={'class': re.compile('b-content__title-record')})
    
    return record[0].text.strip().split(':')[1].strip()

def basic_stats_height(soup):
    
    '''soups run thorugh this function should be run through stats_soup function beforehand.'''
    
    #feet
    height = soup[0].text.strip().split(':')[1].strip().split(' ')[0].replace("'", "")
    
   #inches
    if height == '--':
        
        pass
    
    else:
        
        height = int(height)
        
        inches = int(soup[0].text.strip().split(':')[1].strip().split(' ')[1].replace("'", "").replace('"', '').replace("--", "0"))

        height_to_inches = (height * 12) 
    
        final_height = height_to_inches + inches
    
        return (inches + height_to_inches)

def basic_stats_weight(soup):
    
    weight = soup[1].text.strip().split(':')[1].strip().replace(' lbs.', '')
    
    if weight == '--':
        
        pass
    
    else:
        
        weight = int(weight)
        
    return weight 

def basic_stats_reach(soup):
    
    reach = soup[2].text.strip().split(':')[1].strip().replace('"', '')
    
    if reach == '--':
        
        pass
    
    else:
        
        reach = int(reach)
        
    return reach

def basic_stats_stance(soup):
    
    stance = soup[3].text.strip().split(':')[1].strip()
    
    return stance

def basic_stats_DOB(soup):
    
    DOB = soup[4].text.strip().split(':')[1].strip()
    
    return DOB

#Creating daat for creation of dataframe

fighter_names = list(map(fighter_name, fighter_url_soup_list))

fighter_records = list(map(fighter_record, fighter_url_soup_list))

fighter_heights =  list(map(basic_stats_height, fighter_stats_objects))

fighter_weights = list(map(basic_stats_weight, fighter_stats_objects))

fighter_reachs = list(map(basic_stats_reach, fighter_stats_objects))

fighter_stances = list(map(basic_stats_stance, fighter_stats_objects))

fighter_DOBs = list(map(basic_stats_DOB, fighter_stats_objects))

#Constructing final dataframe

fighter_phys_stats_df = pd.DataFrame()

fighter_phys_stats_df['name'] = fighter_names

fighter_phys_stats_df['record'] = fighter_records

fighter_phys_stats_df['height'] = fighter_heights

fighter_phys_stats_df['weight'] = fighter_weights

fighter_phys_stats_df['reach'] = fighter_reachs

fighter_phys_stats_df['stance'] = fighter_stances

fighter_phys_stats_df['DOB'] = fighter_DOBs

#Saving fighter physical stats

fighter_phys_stats_df.to_csv('fighter_physical_stats_csv', index=False)


