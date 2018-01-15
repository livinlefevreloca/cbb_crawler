#!Python3

#crawler.py - crawl the seasons index page from sports-reference.com and pull data if the team was from the NCAA tournament


from bs4 import BeautifulSoup
import sys, requests, time, pickle
#url = sys.argv[1]

root_url = "https://www.sports-reference.com/"

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
        return soup.find('table', {'id': 'conference-summary_clone'})
    if(depth ==2):
        return soup.find('table', {'id': 'standings'})
    
        
def parse_for_links(branch, depth=0):
    if(depth == 0):
        table = get_table(branch, depth)
        year_cue = que()
        cells = table.find_all('td', {'data-stat': 'season'})
        for cell in cells:
            a_tag = cell.find('a')
            year_cue.insert(root_url + a_tag['href'])
        return year_cue
    elif(depth == 1):
        table = get_table(branch, depth)
        conf_cue = que()
        cells = table.find_all('td', {'data-stat': 'conf_name'})
        for cell in cells:
            a_tag = cell.find('a')
            conf_cue.insert(root_url + a_tag['href'])
        return conf_cue
        
    
    
def parse_for_data(leaf):
    #TODO - parse the given table for data. check if notes contains NCAA tournament and if so pull SOS, OPP, OWN and win%
    table = get_table(leaf, 2)
    rows = table.find_all('tr')
    conf_dict = {}
    for row in rows:
        if( "NCAAA Tournament" in row.find('td', {'data-stat': "notes"}).text):
            WL = row.find('td', {'data-stat': 'win_loss_pct'}).text
            PPG = row.find('td', {'data-stat': 'pts_per_g'}).text
            OPG = row.find('td', {'data-stat': 'opp_pts_per_g'}).text
            SOS = row.find('td', {'data-stat': 'sos'}).text
            school = row.find('td', {'data-stat': 'school_name'})
            team_dict = { 'Win-Loss': WL, 'pts_per_g': PPG, 'opp_pts_per_g': OPG, 'Str_of-Sched': SOS}
            conf_dict[school] = team_dict
            
    return conf_dict
  
class que():
    
    def __init__(self):
        self.que_list = [];
        
    def insert(self, item):
        self.que_list = [item] + self.que_list
    def pull(self):
        return self.que_list.pop()
        





    