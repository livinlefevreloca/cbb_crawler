#!python3

#round.py creates a class representing a single round of the tournament
from match import Match

class Round():
    
    def __init__(self, teams_list):
        self.matches = teams_list
        self.next_matches = []
        
    def advance(self):
        adv_teams = []
        for pair in self.matches:
            current_match = Match(pair)
            adv_teams.append(current_match.get_winner())
        
        if len(adv_teams) ==1:
            
            return adv_teams[0]
        else:
            [self.next_matches.append([adv_teams[i], adv_teams[i+1]]) for i in range(0,len(adv_teams),2)]
            return adv_teams
        
    def get_current_matches(self):
        return self.matches
    
    def get_next_matches(self):
        return "Matches have not been played yet" if len(self.next_matches) == 0 else self.next_matches
    