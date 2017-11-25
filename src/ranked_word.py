class RankedWord:
    def __init__(self,word,isPos,score=0, isUpper=False):
        self.score = score
        self.word = word
        self.isPos = isPos
        self.isUpper = isUpper;

    def getscore(self):
        return self.score

    def getword(self):
        return self.word

    def __lt__(self,other):
        return self.score < other.score

    def __str__(self):
        return str('Word : ' + str(self.word) + " Rank : " + str(self.score))
    

if __name__ == '__main__':
    print("This file can only be imported!")

