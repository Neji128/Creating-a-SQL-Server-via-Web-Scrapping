from bs4 import BeautifulSoup
import requests, re
import pandas as pd

def getEventUrls(all_events_url):
    '''
    Fetches the event urls found on the given url ex: "http://www.ufcstats.com/statistics/events/"{arg_here}
        
        Args:
            
            string: unmodified target events url
        
        Output:
            
            list: python object containing strings of event urls
    '''   
    
    events_response = requests.get(all_events_url)
    
    events_soup = BeautifulSoup(events_response.content, "html.parser")
    
    events = events_soup.findAll("a", attrs={"class": re.compile("b-link b-link_style_black")})

    event_url_list = [event.get("href") for event in events]
    
    return event_url_list

def getEventDates(all_events_url):
    
    '''
    Fetches the event urls found on the given url ex: "http://www.ufcstats.com/statistics/events/"{arg_here}
        
        Args:
            
            string: unmodified target events url
        
        Output:
            
            list: python object containing strings of event dates
    '''   
    
    events_response = requests.get(all_events_url)
    
    events_soup = BeautifulSoup(events_response.content, "html.parser")
    
    event_dates = events_soup.findAll("span", attrs={"class": re.compile("b-statistics__date")})

    event_dates_list = [event_date.text.strip() for event_date in event_dates]
    
    return event_dates_list

def getEventFightUrls(event_details_url):
    
    '''
    Fetches the event urls found on the given url ex: "http://http://www.ufcstats.com/event-details/"{arg_here}
        
        Args:
            
            string: unmodified target event-details url
        
        Output:
            
            list: python object containing strings of event dates
    '''   
    
    events_response = requests.get(event_details_url)
    
    events_soup = BeautifulSoup(events_response.content, "html.parser")
    
    event_fights = events_soup.findAll("a", attrs={"class": re.compile("b-flag b-flag_style_green")})
    
    event_fight_url_list = [fight.get("href") for fight in event_fights]
    
    return event_fight_url_list

def getEventSummaryStats(event_details_url):
       
    '''
    Fetches the event urls found on the given url ex: "http://http://www.ufcstats.com/event-details/"{arg_here}
        
        Args:
            
            string: unmodified target event-details url
        
        Output:
            
            list: python object containing strings of event dates
    '''   
    
    event_summary_table = pd.read_html(event_details_url)[0]
    
    return event_summary_table

def getFightStatsTables(fight_url):
    
    fight_stats_tables_list = pd.read_html(fight_url)

    return fight_stats_tables_list


def getFightOutcomes(fight_url):
    
    '''
    Fetches fighter's outcome, name and nickname from fight-details url
    
        Args: unmodified target fight-details url
            
            string:
                
        Output:
            
            list: python object containg 2 lists of strings [outcome, fighter_name, fighter_nickname]
    '''
    response = requests.get(fight_url)
    
    response_soup = BeautifulSoup(response.content, "html.parser")
    
    fight_outcomes_soup = response_soup.find("div", attrs={"class": re.compile("b-fight-details__person")})
    
    outcomes_list = []
    
    fight_outcomes_strings_list = [x.text.strip() for x in fight_outcomes_soup]
    
    fight_outcomes_strings_list = [x for x in fight_outcomes_strings_list if x != '']
    
    fight_outcomes_strings_list = [x.split("\n\n") for x in fight_outcomes_strings_list]
    
    for outcome in fight_outcomes_strings_list:
        
        outcome = [x.strip() for x in outcome]
        
        outcome = [x.replace('"', '') for x in outcome]
        
        outcomes_list.append(outcome)

    return outcomes_list
    
def getFightCard(fight_url):
    
    '''
    Fetches the fight card title tied to the fight
    
        Args: unmodified target fight-details url
            
            string:
                
        Output:
            
            string: title of the event fight card
    '''
    
    response = requests.get(fight_url)
    
    response_soup = BeautifulSoup(response.content, "html.parser")
    
    fight_card_title = response_soup.find("h2", attrs={"class": re.compile("b-content__title")})
    
    fight_card_title_text = fight_card_title.text.strip()
    
    return fight_card_title_text

def getSignificantStrikesStats(fight_url):
    
    '''
    Fetches the fight significan strike percentage by target for the fight
    
        Args: unmodified target fight-details url
            
            string:
                
        Output:
            
            string:
    '''
    
    response = requests.get(fight_url)
    
    response_soup = BeautifulSoup(response.content, "html.parser")
    
    fight_sig_strike_categories = response_soup.findAll("i", attrs={"class": re.compile("b-fight-details__charts-row")})
    
    fight_sig_strike_categories = [cat.text.strip() for cat in fight_sig_strike_categories]
    
    fight_sig_strike_stats = response_soup.findAll("i", attrs={"class": re.compile("b-fight-details__charts-num b-fight-details__charts-num_style")})
    
    fight_sig_strike_stats = [stat.text.strip() for stat in fight_sig_strike_stats]
    
    #isolating values associated with fighter in position 1
    fight_sig_strike_stats_left = fight_sig_strike_stats[::2]
    
    #isolating values associated with fighter in position 2
    fight_sig_strike_stats_right = fight_sig_strike_stats[1::2]
    
    return fight_sig_strike_stats_left, fight_sig_strike_stats_right