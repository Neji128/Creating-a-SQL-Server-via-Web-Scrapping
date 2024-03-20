import requests, re
from bs4 import BeautifulSoup
import pandas as pd

def getFighterName(soup):
    '''
    Identifies fighter history to be parsed.
    
        Args:
            soup (bs4 object): BeautifulSoup object must originate from the ufcstats.com section '''
    
    name_soup = soup.find("span", attrs={"class": re.compile("b-content__title-highlight")})
    
    name = name_soup.text.strip()
    
    return name

def getFighterRecord(soup):
    '''
    Fetches each fighter's fighting record from a beautiful soup object
        
        Args:
            
            soup (bs4 object): unmodified BeautifulSoup object geted from ufcstats.com/fighters list
        
        Output:
            
            tuple: wins, losses, draws
    '''
    
    record_children = soup.findChild("span", attrs={"class": re.compile("b-content__title-record")})
    
    result = [x.strip() for x in record_children]
    
    result_string = "".join(result)
    
    record_title, record_digits = result_string.split(":")
    
    record_list = [x for x in record_digits if x.isdigit()]
    
    wins, loses, draws = record_list
    
    return wins, loses, draws

def getBasicStats(soup):
    '''
    Fetches each fighter's basic statistics from a beautiful soup object
        
        Args:
            
            soup (bs4 object): unmodified BeautifulSoup object geted from ufcstats.com/fighters list
        
        Output:
            
            list: height, weightk, reach, stance, DOB
    '''
    
    i_class_title_objects = soup.findChildren("i", attrs={"class": re.compile("b-list__box-item-title b-list__box-item-title_type_width")})

    base_stats_objects_list = [i.next_sibling.strip() for i in i_class_title_objects[:5]]

    return base_stats_objects_list

def getCareerStats(soup):
    '''
    Fetches each fighter's career statistics from a beautiful soup object
        
        Args:
            
            soup (bs4 object): unmodified BeautifulSoup object geted from ufcstats.com/fighters list
        
        Output:
            
            list: SLpM, Str. Acc., SApM, Str. Def., TD Avg, TD Acc., TD Def., Sub. Avg
    '''
    
    i_class_objects = soup.find_all("i", attrs={"class": "b-list__box-item-title b-list__box-item-title_font_lowercase b-list__box-item-title_type_width"})
    
    career_stats_object_list = [i.next_sibling.strip() for i in i_class_objects]

    career_stats_list = [re.sub(r"[^\d.]", "",item) for item in career_stats_object_list]
    
    return career_stats_list

def getFighterHistory(url):
    '''
    Fetches the tabular history of a fighter
            
        Args:
            
            url: the url associated with the target fighter
        
        Output:
            
            list: height, weightk, reach, stance, DOB
    '''
    table = pd.read_html(url, skiprows=(1, 1))
    
    return table
    
