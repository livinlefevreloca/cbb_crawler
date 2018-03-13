#!Python3

#crawler.py - crawl the seasons index page from sports-reference.com and pull data if the team was from the NCAA tournament


from bs4 import BeautifulSoup
from collections import Iterator
import sys, requests, time, pickle, bs4, re
url1= 'https://www.sports-reference.com/cbb/seasons/'
url2 = "https://www.sports-reference.com/cbb/conferences/"
url3 = "https://www.sports-reference.com/cbb/postseason/"
url4 = "/cbb/schools/"
root_url = "https://www.sports-reference.com"

def get_html(url):
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    return res.text

def make_soup(res):
    return BeautifulSoup(res, 'html.parser')

def get_table(soup, depth=0):
    if(depth==0):
        return soup.find('table', {'id': 'seasons'})
    if(depth ==1):
        return soup.find('table', {'id': 'conference-summary'})
    if(depth ==2):
        return soup.find('table', {'id': 'standings'})
    if(depth ==3):
        return soup.find('table', {'id': 'seasons'})
    
        
def parse_for_links(branch, depth):
    if(depth == 0):
        table = get_table(branch, depth)
        year_cue = que()
        rows = table.find_all('tr')
        for row in rows:
            if(row.find('td') == None):
                continue
            cell_year = row.find('td', {'data-stat': 'season'})
            a_tag_year = cell_year.find('a')
            # if "2018" in a_tag_year['href']:
            #     continue
            year_cue.insert(root_url + a_tag_year['href'])
        return year_cue
    elif(depth == 1):
        table = get_table(branch, depth)
        conf_cue = que()
        cells = table.find_all('td', {'data-stat': 'conf_name'})
        for cell in cells:
            a_tag = cell.find('a')
            # if "2018" in a_tag['href']:
            #     continue
            conf_cue.insert(root_url + a_tag['href'])
        return conf_cue
    elif(depth == 3):
        table = get_table(branch, depth)
        tourn_cue = que()
        rows = table.find_all('tr')
        for row in rows[2:]:
            if(row.find('td') == None):
                continue
            cell_tourn = row.find('td', {'data-stat': 'ncaa_tourney'})
            if cell_tourn.contents == []:
                continue
            a_tag_tourn = cell_tourn.find('a')
            tourn_cue.insert(root_url + a_tag_tourn['href'])
        return tourn_cue
        
       
    
    
def parse_for_data(leaf):
    #parse the given table for data. check if notes contains NCAA tournament and if so pull SOS, OPP, OWN and win%
    table = get_table(leaf, 2)
    rows = table.find_all('tr')
    conf_dict = {}
    for row in rows:
        if(row.find('td', {'data-stat': 'notes'}) != None):
            if( "NCAA Tournament" in row.find('td', {'data-stat': "notes"}).text):
                try:    
                    WL = row.find('td', {'data-stat': 'win_loss_pct'}).text
                    PPG = row.find('td', {'data-stat': 'pts_per_g'}).text
                    OPG = row.find('td', {'data-stat': 'opp_pts_per_g'}).text
                    SOS = row.find('td', {'data-stat': 'sos'}).text
                    school = row.find('td', {'data-stat': 'school_name'}).find('a').text
                    team_dict = { 'Win-Loss': WL, 'pts_per_g': PPG, 'opp_pts_per_g': OPG, 'Str_of-Sched': SOS}
                    conf_dict[school] = team_dict
                except AttributeError as e:
                    print(e)
                    pass
            
    return conf_dict
    
    

def format_dat(dat):
    if '-' in dat:
        words = dat.split('-')
    elif ' ' in dat:
        words = dat.split(' ')
    else:
        return dat
    new_words = [word for word in words]
    new_dat = ' '.join(new_words)
    return new_dat
        
    
def parse_for_winners(soup):
    brackets = soup.find('div', {'id': 'brackets'})
    tourn_dict = {}
    for region in brackets.findChildren():
        if( type(region) is bs4.element.NavigableString):
            continue
        reg = region.get('id')
        region_dict = {}
        rounds = region.find_all('div', {'class': 'round'})
        for i, rnd in enumerate(rounds):
            round_list = []
            for game in rnd:
                if( type(game) is bs4.element.NavigableString):
                    continue
                if(game.has_attr('class')):
                    if game['class'] == ['bye']:
                        continue
                match_list = []
                for elm in game:
                    if( type(elm) is not bs4.element.Tag):
                        continue
                    if elm.name == 'span':
                        dat = elm.find('a').text
                    else:
                        dat = elm.find('a')['href']
                        dat = dat.replace(url4, '')
                        dat = re.sub(r'\/\d\d\d\d.html','', dat)
                        dat = format_dat(dat)
                    if elm.has_attr('class'):
                        if elm['class'] == ['winner']:
                            dat = '(' + dat + ')'
                    if dat == '':
                        print('failed to find')
                        print(elm)
                    match_list.append(dat) 
                round_list.append(match_list)
            if len(round_list) != 0:
                region_dict[i+1] = round_list   
        tourn_dict[reg] = region_dict  
    return tourn_dict  
    
def continous_pickle(file_path, add, key, key_two=None):
    try:
        with open(file_path, 'rb') as file:
            obj = pickle.load(file)
    except OSError as e:
        print('no such pickl exisits')
    if key_two is not None:
        obj[key][key_two] = add
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
            print('pickled double key')
            print(obj)
    else:
        obj[key] = add
        
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
            print('pickled single key')
    
    
    
    
  
class que():
    
    def __init__(self):
        self.que_list = [];
        
    def get_size(self):
        return len(self.que_list)
        
    def insert(self, item):
        self.que_list = [item] + self.que_list
    def pull(self):
        return self.que_list.pop()
   
    def __iter__(self):
        while self.get_size() != 0:
            time.sleep(3)
            yield self.pull()
   
            





def main():
    root_res = get_html(url1)
    root_soup = make_soup(root_res)
    years = parse_for_links(root_soup, 0)
    tourns = parse_for_links(root_soup, 3)
    year_path = './pickles/years.pickle'
    winners_data = {}
    winner_path = './pickles/new_winners.pickle'
    
    with open(year_path, 'wb') as f:
            seasons = {}
            pickle.dump(seasons,f)
            
    for year in years:
        print(year)
        date = year.replace(url1, '').replace('.html', '')
        year_res = get_html(year)
        year_soup = make_soup(year_res)
        confs = parse_for_links(year_soup,1)
        conference_data ={}
        continous_pickle(year_path,conference_data,date)
        for conf in confs:
            print(conf)
            conference = conf.replace(url2, '').replace('/'+date+'.html', '')
            conf_res = get_html(conf)
            conf_soup = make_soup(conf_res)
            continous_pickle(year_path, parse_for_data(conf_soup), date, conference)
    with open(winner_path, 'wb') as f:
        pickle.dump({}, f)
    for tourn in tourns:
        print(tourn)
        tourn_year = tourn.replace(url3, '').replace('-ncaa.html', '')
        tourn_res = get_html(tourn)
        tourn_soup = make_soup(tourn_res)
        winners = parse_for_winners(tourn_soup)
        print(winners.keys())
        winners_data[tourn_year] = winners
        continous_pickle(winner_path, winners, tourn_year)
  
  
  


