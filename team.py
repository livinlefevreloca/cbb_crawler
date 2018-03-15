#! python3
#team.py - class to represent individual teams in the tournament
import numpy as np

class Team():
    
    def __init__(self, name, vector):
        self.name = name
        self.vec = vector
    
    def get_name(self):
        return self.name
    
    def get_vector(self):
        return self.vec
    
    def play(self, opp_team_vec, opp_team_name):
        print('{}: {}'.format(self.get_name(), self.get_vector()))
        print('{}: {}'.format(opp_team_name, opp_team_vec))
        return np.subtract(self.get_vector(), opp_team_vec)