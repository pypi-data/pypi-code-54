import os, pickle

from settings import HIGHSCORES

NAME = 0
SCORE = 1
MAX = 10

class HallOfFame(object):

    def __init__(self):
        self.top_scores = []

    def score_lines(self):
        lines = []
        CPL = 40 #chars per line
        for i in range(MAX):
            temp1 = str(i) + " -       " + self.top_scores[i][NAME]
            temp2 = str(self.top_scores[i][SCORE])
            spaces = CPL - len(temp1) - len(temp2)
            lines += [temp1 + " "*spaces + temp2]

        return lines

    def minor_value(self):
        '''Return the SCORE element of the last tuple in the
        top_scores list.'''
        return self.top_scores[-1][SCORE]

    def add(self, name, score):
        '''Check against minor_value before adding.'''
        top = self.top_scores
        for i in range(MAX):
            if score > top[i][SCORE]:
                break

        self.top_scores = top[:i] + [(name, score)] + top[i:-1]

        f = open(HIGHSCORES, 'wb')
        pickle.dump(self, f)
                

if not os.path.exists(HIGHSCORES):

    top_scores = [("jjconti", 200),
                 ("CEP", 199),
                 ("Warrior", 145),
                 ("CyBorg", 123),
                 ("Mary", 122),
                 ("F5", 101),
                 ("Bicentauro", 90),
                 ("Trent", 78),
                 ("El Grande", 65),
                 ("Joly", 2),]
    
    hof = HallOfFame()
    hof.top_scores = top_scores

    f = open(HIGHSCORES, 'wb')
    pickle.dump(hof, f)

else:
    f = open(HIGHSCORES, 'rb')
    hof = pickle.load(f)
