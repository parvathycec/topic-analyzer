
class RankedWord:
    def __init__(self,word,score):
        self.score = score
        self.word = word

    def getscore(self):
        return self.score

    def getword(self):
        return self.word

    def __lt__(self,other):
        return self.score < other.score


import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

def check_all_cases_rank(key,content,total_rank):
    rank = 0
    if key in content:
        rank = total_rank
    elif key.lower() in content:
        rank = total_rank
    elif key.upper() in content:
        rank = total_rank
    elif key.title() in content:
        rank = total_rank

    return rank
        

def do_rank(url,word):
    score = 0
    ranking = RankedWord(word,score)

    

    ranking.score = 11

    return ranking


\

        
    
    
    
