#!python3
#tournament.txt - simulate 2018 tournament

import pickle
from team import Team
from rnd import Round
import numpy as np
# predict first four

first4 = [['Long Island University', 'Radford'], ['St. Bonaventure', 'UCLA'], ['North Carolina Central', 'Texas Southern'], ['Arizona State', 'Syracuse']]

with open('./pickles/2018.pickle', 'rb') as data:
        team_data = dict(pickle.load(data))

def make_vec(name):
    data = team_data[name]
    return np.array([float(data['Win-Loss']), float(data['pts_per_g']),float(data['opp_pts_per_g']), float(data['Str_of-Sched'])])


   
def first_four(firfor):
    
    teams = []
    for pair in firfor:
        vec1 = make_vec(pair[0])
        vec2 = make_vec(pair[1])
        matchup = [[Team(pair[0], vec1), Team(pair[1], vec2)],]
        rnd = Round(matchup)
        winner = rnd.advance()
        teams.append(winner)
        print('Winner of {} vs {} is {}'.format(pair[0], pair[1], winner.get_name()))
        
#first_four(first4)


def make_match_list():
    with open('NCAA_matches.txt', 'r') as matches:
        
        return [(line.split(',')[0].rstrip(), line.split(',')[1].rstrip()) for line in matches if len(line) > 3]    

def play_tourn():
    match_list = make_match_list()
    match_list = [(Team(pair[0], make_vec(pair[0])), Team(pair[1], make_vec(pair[1]))) for pair in match_list]
    rnd64 = Round(match_list)
    rnd32_list = rnd64.advance()
    print([team.get_name() for team in rnd32_list])
    print('\n')
    rnd32_list = [(rnd32_list[i], rnd32_list[i+1]) for i in range(0, len(rnd32_list), 2)]
    rnd32 = Round(rnd32_list)
    rnd16_list = rnd32.advance()
    print([team.get_name() for team in rnd16_list])
    print('\n')
    rnd16_list = [(rnd16_list[i], rnd16_list[i+1]) for i in range(0, len(rnd16_list), 2)]
    rnd16 = Round(rnd16_list)
    rnd8_list = rnd16.advance()
    print([team.get_name() for team in rnd8_list])
    print('\n')
    rnd8_list = [(rnd8_list[i], rnd8_list[i+1]) for i in range(0, len(rnd8_list), 2)]
    rnd8 = Round(rnd8_list)
    rnd4_list = rnd8.advance()
    print([team.get_name() for team in rnd4_list])
    print('\n')
    rnd4_list = [(rnd4_list[i], rnd4_list[i+1]) for i in range(0, len(rnd4_list), 2)]
    rnd4 = Round(rnd4_list)
    champ_list = rnd4.advance()
    champ_list = [(champ_list[i], champ_list[i+1]) for i in range(0, len(champ_list), 2)]
    champ = Round(champ_list)
    champion = champ.advance()
    print(champion.get_name())
    

play_tourn()