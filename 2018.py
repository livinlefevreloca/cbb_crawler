from bs4 import BeautifulSoup
from collections import Iterator
import sys, requests, time, pickle, bs4, re
import crawler as c

start_url = "https://www.sports-reference.com/cbb/seasons/2018.html"
root_url = 'https://www.sports-reference.com/'

def load_team_list():
    team_list = []
    with open('TournTeams.txt', 'r') as teams:
        for team in teams:
            team_list.append(team.rstrip())
    return team_list

def pull_team_data(row):
    WL = row.find('td', {'data-stat': 'win_loss_pct'}).text
    PPG = row.find('td', {'data-stat': 'pts_per_g'}).text
    OPG = row.find('td', {'data-stat': 'opp_pts_per_g'}).text
    SOS = row.find('td', {'data-stat': 'sos'}).text
    return {'Win-Loss': WL, 'pts_per_g': PPG, 'opp_pts_per_g': OPG, 'Str_of-Sched': SOS}

def search_for_team(soup, teams):
    schools = soup.find('table', {'id': 'standings'})
    rows = schools.find_all('tr')
    conf_data = []
    for row in rows:
        try:
            school = row.find('td',{'data-stat': 'school_name'})
            school_name = school.find('a').text
            if school_name in teams:
                team_data = pull_team_data(row)
                conf_data.append((school_name, team_data))
        except AttributeError as e:
            continue
    return conf_data
    

def main():
    root_res = c.get_html(start_url)
    root_soup = c.make_soup(root_res)
    confs = c.parse_for_links(root_soup,1)
    teams = load_team_list()
    data_2018 = []
    for conf in confs:
        print(conf)
        conf_res = c.get_html(conf)
        conf_soup = c.make_soup(conf_res)
        data_2018 += search_for_team(conf_soup, teams)
    print(len(data_2018))
    print(data_2018)
    with open('./pickles/2018.pickle', 'wb') as pickle_2018:
        pickle.dump(data_2018, pickle_2018)
    
    
main()