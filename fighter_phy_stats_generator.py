

def fighter_soup_generator(url):
    '''Meant to parse any url via beuatiful soup
    
    Args:
        url(str): url that will be parsed using BeautifulSoup'''
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    return soup



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

def basic_stats_stance(soup):
    
    stance = soup[3].text.strip().split(':')[1].strip()
    
    return stance

def basic_stats_DOB(soup):
    
    DOB = soup[4].text.strip().split(':')[1].strip()
    
    return DOB

#Creating daat for creation of dataframe

fighter_names = list(map(fighter_name, fighter_soup_list))

fighter_records = list(map(fighter_record, fighter_soup_list))

fighter_heights =  list(map(basic_stats_height, stats_soups))

fighter_weights = list(map(basic_stats_weight, stats_soups))

fighter_reachs = list(map(basic_stats_reach, stats_soups))

fighter_stances = list(map(basic_stats_stance, stats_soups))

fighter_DOBs = list(map(basic_stats_DOB, stats_soups))

#Constructing final dataframe

fighter_basic_stats_df = pd.DataFrame()

fighter_basic_stats_df['name'] = fighter_names

fighter_basic_stats_df['record'] = fighter_records

fighter_basic_stats_df['height'] = fighter_heights

fighter_basic_stats_df['weight'] = fighter_weights

fighter_basic_stats_df['reach'] = fighter_reachs

fighter_basic_stats_df['stance'] = fighter_stances

fighter_basic_stats_df['DOB'] = fighter_DOBs

#Saving fighter physical stats

fighter_physical_stats_df.to_csv('fighter_physical_stats_csv', index=False)


