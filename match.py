#!python3
#match.py - creates a class to model a match between 2 teams
import random
from models.desTree import model
from sklearn import preprocessing 
import numpy as np
import pickle

class Match():
    
    def __init__(self, teams):
        #randomly determine team1 and team2 for deciding the match.
        self.team1 = teams[0]
        self.team2 = teams[1]
        self.winner = None
    
    def get_teams(self):
        return (self.team1, self.team2)
    
        
    def get_winner(self):
        teams = self.get_teams()
        outcome = teams[0].play(teams[1].get_vector(), teams[1].get_name())
        with open('scale.pickle', 'rb') as scale:
            scaler = pickle.load(scale)
        print('vector(pre transform): {}'.format(outcome,))
        outcome = scaler.transform([outcome,])
        val = model.predict(np.array(outcome))[0]
        winner = teams[0] if val == 1 else teams[1]
        print('{} wins {} vs {}'.format(winner.get_name(), teams[0].get_name(), teams[1].get_name()))
        print('vector: {}'.format(outcome,))
        print('\n')
        return winner
        