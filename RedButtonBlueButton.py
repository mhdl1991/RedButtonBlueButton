# -*- coding: utf-8 -*-
import random
from enum import Enum
from typing import Optional, List, Dict, Tuple, TypeVar

_E = TypeVar('_E', bound = Enum)

"""
    @author: mhdl1991
    
    a python script for loosely simulating the infamous red button/blue button thought experiment
    https://x.com/waitbutwhy/status/2047710215265730755
    
    "Everyone in the world has to take a private vote by pressing a red or blue button. If more than 50% of people press the blue button, everyone survives. If less than 50% of people press the blue button, only people who pressed the red button survive. Which button would you press?"

"""

class Color(Enum):
    NONE = 0
    RED = 1
    BLUE = 2

class Voter:
    def __init__(self) -> _E:
        """
        Voter
        makes a random selection of either Red or Blue
        """
        self.options = [Color.RED, Color.BLUE]
        self.selection = ""
        
        # Make your selection, ladies and gentlemen
        self.vote()
        
    def vote(self) -> _E:
        """
        we can add reasons why each voter would want to pick one or the other later
        for now the default is random behavior 
        """
        _pick = random.choice(self.options)
        self.selection = _pick
        return _pick
 
    def set_option_manually(self, your_selection: _E) -> _E:
        """
        One voter is chosen as your representative/standin in this simulation
        Not for any particularly good reason, but the idea is to help figure out the likelihood of you living or dying
        """
        if your_selection in self.options:
            self.selection = your_selection
            
        return _E
        
    def get_selection(self) -> _E:
        """
        returns what this voter selected
        """
        return self.selection
        

class Trial:
    def __init__(self, number_voters: int, your_vote: _E) -> Tuple[int, int, int, _E, bool]:
        """
        Each "trial" comprises of number_voters Voters voting and the result of said voting
        one voter is your standin, so they have to have their selection set to your_vote
        """
        self.number_voters = number_voters
        
        # one voter in each trial serves as your stand-in.
        # this is done to help understand how you, the user, should vote in this scenario
        self.standin = Voter()
        if your_vote in [Color.RED, Color.BLUE]:
            self.standin.set_option_manually(your_vote)
            
        # then there's everyone else
        self.voter_bank = [Voter() for n in range(self.number_voters - 1)]
        
        
        self.death_count = 0
        self.how_i_voted = self.standin.get_selection()
        self.i_died = False
        
        self.who_won = Color.RED
        
        self.voting_outcomes()
        
    def voting_outcomes(self) -> Tuple[int, int, int, bool, bool, bool]:
        """
        Do the simulation of the voting and tabulate the results
        """
        self.red_votes = sum([1 for v in self.voter_bank if v.get_selection() == Color.RED])
        self.blue_votes = sum([1 for v in self.voter_bank if v.get_selection() == Color.BLUE])
        
        # add your own vote to the votes
        if self.how_i_voted == Color.RED:
            self.red_votes += 1
        
        if self.how_i_voted == Color.BLUE:
            self.blue_votes += 1
        
        # results
        if self.blue_votes >= self.red_votes:
            #Blue victory, nobody dies, you WON'T die
            self.who_won = Color.BLUE
            self.i_died = False
            self.death_count = 0
        
        else:   
            #Red victory, Blues die, you MIGHT die
            self.who_won = Color.RED
            self.death_count = self.blue_votes
            
            if (self.how_i_voted == Color.RED):
                self.i_died = False # you survived
            if (self.how_i_voted == Color.BLUE):
                self.i_died = True
                self.death_count += 1 # add yourself to the pile of bodies
                
        
        return (self.red_votes, self.blue_votes, self.death_count, self.who_won, self.i_died)
        

if __name__ == '__main__':

    number_tests = 5000
    number_voters = 1000
    
    print("Everyone in the world has to take a private vote")
    print("By pressing a red or blue button.")
    print("If more than 50% of people press the blue button, everyone survives.")
    print("If less than 50% of people press the blue button,")
    print("only people who pressed the red button survive.")
    print()
    print("Which button should you press?")
    print()
    
    print("This Python script will simulate this scenario")
    print(f"It will run {number_tests} virtual polls. In each poll, {number_voters} simulated voters each vote for red or blue")
    print("One voter is chosen to represent you, the user.")
    print()
    
    
    # evenly split number of tests into ones where you vote red and ones where you vote blue
    if number_tests % 2 == 1:
        number_tests = number_tests + 1
            
    number_red_tests = number_tests // 2
    number_blue_tests = number_tests - number_red_tests
        
    red_tests = [Trial(number_voters, Color.RED) for trial in range(number_red_tests)]
    blue_tests = [Trial(number_voters, Color.BLUE) for trial in range(number_blue_tests)]
        
    redtest_red_wins = 0
    bluetest_red_wins = 0
    total_red_wins = 0
    
    redtest_blue_wins = 0 
    bluetest_blue_wins = 0
    total_blue_wins = 0
    
    red_win_probability = 0
    blue_win_probability = 0
    
    redtest_yourdeaths_count = 0
    redtest_alldeaths_count = 0
    redtest_avgdeathtoll = 0
    
    bluetest_yourdeaths_count = 0
    bluetest_alldeaths_count = 0
    bluetest_avgdeathtoll = 0
    
    total_yourdeaths_count = 0
    
    # tests where you vote red
    for test in red_tests:
        if test.who_won == Color.RED:
            redtest_red_wins += 1
            
        if test.who_won == Color.BLUE:
            redtest_blue_wins += 1
            
        if test.i_died:
            redtest_yourdeaths_count += 1
        
        redtest_alldeaths_count += test.death_count
        
    redtest_avgdeathtoll = redtest_alldeaths_count / number_red_tests
    
    print(f"there are {number_red_tests} polls where you voted red")
    print(f"During these tests, there were {redtest_red_wins} Red wins, and {redtest_blue_wins} Blue wins")
    print(f"During these tests, you died {redtest_yourdeaths_count} times (Probability = {redtest_yourdeaths_count / number_red_tests})")
    print(f"The average death toll is {redtest_avgdeathtoll}")
    print()
        
    # tests where you vote blue
    for test in blue_tests:
        if test.who_won == Color.RED:
            bluetest_red_wins += 1
            
        if test.who_won == Color.BLUE:
            bluetest_blue_wins += 1
        
        if test.i_died:
            bluetest_yourdeaths_count += 1
        
        bluetest_alldeaths_count += test.death_count
        
    bluetest_avgdeathtoll = bluetest_alldeaths_count / number_blue_tests
        
    print(f"there are {number_blue_tests} polls where you voted blue")
    print(f"During these tests, there were {bluetest_red_wins} Red wins, and {bluetest_blue_wins} Blue wins")
    print(f"During these tests, you died {bluetest_yourdeaths_count} times, (Probability =  {bluetest_yourdeaths_count / number_blue_tests})")
    print(f"The average death toll is {bluetest_avgdeathtoll}")
    print()
    
    total_blue_wins = bluetest_blue_wins + redtest_blue_wins
    total_red_wins = bluetest_red_wins + redtest_red_wins
    total_yourdeaths_count = bluetest_yourdeaths_count + redtest_yourdeaths_count
    total_alldeaths_counts = bluetest_alldeaths_count + redtest_alldeaths_count
    
    print(f"Overall, blue won {total_blue_wins} out of {number_tests} times (Probability = {total_blue_wins / number_tests})")
    print(f"Overall, red won {total_red_wins} out of {number_tests} times (Probability = {total_red_wins / number_tests})")
    print(f"Throughout these simulated polls, you've died {total_yourdeaths_count} times (Probability = {total_yourdeaths_count / number_tests})")
    print(f"Throughout these simulated polls, The average death toll is {total_alldeaths_counts / number_tests}")
    