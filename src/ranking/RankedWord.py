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

    def __str__(self,other):
        return str('Word : ' + str(self.word) + " Rank : " + str(self.score))

    
