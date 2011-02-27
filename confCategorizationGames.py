from __future__ import division
import random
import sys
import pylab
from matplotlib.colors import colorConverter
import random
import numpy as np

def transposed(lists):
    if not lists: return []
    return map(lambda *row: list(row), *lists)


def color(colour, weight=2.4):
    """ Convert colour into a nice pastel shade"""
    rgb = np.asarray(colorConverter.to_rgb(colour))
    # scale colour
    maxc = max(rgb)
    if maxc < 1.0 and maxc > 0:
        # scale colour
        scale = 1.0 / maxc
        rgb = rgb * scale
    # now decrease saturation
    total = rgb.sum()
    slack = 0
    for x in rgb:
        slack += 1.0 - x

    # want to increase weight from total to weight
    # pick x s.t.  slack * x == weight - total
    # x = (weight - total) / slack
    x = (weight - total) / slack
    rgb = [c + (x * (1.0-c)) for c in rgb]
    return rgb

def get_colours(n):
    """ Return n pastel colours. """
    base = np.asarray([[1,0,0], [0,1,0], [0,0,1]])
    if n <= 3:
        return base[0:n]
    # how many new colours to we need to insert between
    # red and green and between green and blue?
    needed = (((n - 3) + 1) / 2, (n - 3) / 2)
    colours = []
    for start in (0, 1):
        for x in np.linspace(0, 1, needed[start]+2):
            colours.append((base[start] * (1.0 - x)) +
                           (base[start+1] * x))
    return [color(c) for c in colours[0:n]]

def weighted_choice_b(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    return bisect.bisect_right(totals, rnd)

class BeliefUpdater:

    UpdateRate = 0.025
    @staticmethod
    def _updateSuccessTeacher (belief1, belief2):
        return belief1 + 10 * BeliefUpdater.UpdateRate * belief2

    @staticmethod
    def _updateFailTeacher (belief1, belief2):
        return belief1 - BeliefUpdater.UpdateRate * belief2

    @staticmethod
    def _updateSuccessLearner (belief1, belief2):
        return belief1 + 10 * BeliefUpdater.UpdateRate * belief2

    @staticmethod
    def _updateFailLearner (belief1, belief2):
        return belief1 * (1 - BeliefUpdater.UpdateRate) - BeliefUpdater.UpdateRate * (belief2 - belief1)

    @staticmethod
    def _updateFail (agentT, agentL):
        agentT.setBelief( BeliefUpdater._updateFailTeacher(agentT.getBelief(),
            agentL.getBelief()))
        agentL.setBelief( BeliefUpdater._updateFailLearner(agentL.getBelief(),
            agentT.getBelief()))

    @staticmethod
    def _updateSuccess(agentT, agentL):
        agentT.setBelief(
                BeliefUpdater._updateSuccessTeacher(agentT.getBelief(),
            agentL.getBelief()))
        agentL.setBelief(
                BeliefUpdater._updateSuccessLearner(agentL.getBelief(),
            agentT.getBelief()))

    @staticmethod
    def updateBelief (agent1, agent2, is_success):
        if (agent1.getRole() == 1):
            if (is_success):
                BeliefUpdater._updateSuccess(agent1, agent2)
            else:
                BeliefUpdater._updateFail(agent1, agent2)
        elif (agent1.getRole() == 0):
            if (is_success):
                BeliefUpdater._updateSuccess (agent2, agent1)
            else:
                BeliefUpdater._updateFail (agent2, agent2)

class Agent:

    _Role = 0 # 1 if teacher
    _CurrentWord = ""
    _Belief = 0.0

    def setRole (self, role):
        self._Role = role

    def getRole (self):
        return self._Role

    def setBelief (self, belief):
        self._Belief = belief

    def getBelief (self):
        return self._Belief

    def setCurrentWord (self, word):
        self._CurrentWord = word

    def getCurrentWord (self):
        return self._CurrentWord

    def hear (self, word):
        self.setCurrentWord(word)

    def speak (self):
        return self._CurrentWord

class Sim:

    _Lexicon = []
    _Agents = []
    _Map = {}
    _NoOfAgents = 10
    _InitialWords = []
    _NoOfSuccesses = 0
    _NoOfFailures = 0
    _NoOfIterations = 0
    _MaxDict = 0
    _Beliefs = []
    _Categories = []
    _Fails = []
    _Successes = []

    def setMaxDictSize(self, maxDict):
        self._MaxDict = maxDict

    def setLexicon (self, lex):
        self._Lexicon = lex

    def getBeliefs(self):
        return self._Beliefs

    def chooseRandomWord (self):
        l = len(self._Lexicon)
        if (self._MaxDict != 0):
            l = self._MaxDict
        n = random.randint(0, l-1)
        return self._Lexicon[n]

    def setNoOfAgents (self, noOfAgents):
        self._NoOfAgents = noOfAgents

    def getNoOfAgents (self):
        return self.NoOfAgents

    def getRandomAgent (self):
        l = len(self._Agents)
        rnd_val = random.randint(0, l-1)
        return self._Agents[rnd_val]

    def initAgents (self, noOfAgents=0):
        if (noOfAgents):
           self._NoOfAgents = noOfObjects
        for i in range (self._NoOfAgents):
            ag = Agent()
            rnd_word = self.chooseRandomWord()
            belief = random.uniform(0.05, 1)
            print rnd_word + str (belief)
            ag.setCurrentWord (rnd_word)
            ag.setBelief (belief)
            self._Agents.append (ag)

    def _initMap (self):
        for i in range (self._NoOfAgents):
            word = self._Agents[i].getCurrentWord()
            self._InitialWords.append( word )
            if self._Map.has_key(word):
                self._Map[word] += 1
            else:
                self._Map[word] = 1
    def getConvergedWord(self):
        return self._Map.keys()[0]

    def getNoOfSuccesses (self):
        return self._NoOfSuccesses

    def getNoOfFailures (self):
        return self._NoOfFailures

    def getNoOfIterations (self):
        return self._NoOfIterations

    def _getBeliefs(self):
        beliefs = []
        for agent in self._Agents:
            list.append(beliefs, agent.getBelief())
        return beliefs

    def getSuccesses(self):
        return self._Successes

    def getFailures(self):
        return self._Fails

    def getInitialWords(self):
        return self._InitialWords

    def getCategories(self):
        return self._Categories

    def playGames (self):
           l = len (self._Agents)
           self._initMap()
           is_success = 0
           while (len(self._Map) > 1):
            agent1 = self.getRandomAgent()
            agent2 = self.getRandomAgent()
            self._NoOfIterations += 1
            noOfCategories = len(self._Map)
            self._Categories.append(noOfCategories)

            while (agent2 == agent1):
                agent2 = self.getRandomAgent()

            if (agent1.getBelief() > agent2.getBelief()):
                agent1.setRole(1)
                agent2.setRole(0)
            elif (agent2.getBelief() > agent1.getBelief()):
                agent1.setRole(0)
                agent2.setRole(1)
            else:
                agent1.setRole(1)
                agent2.setRole(1)

            if agent1.speak() == agent2.speak():
                self._NoOfSuccesses += 1
                is_success = 1
            else:
                is_success = 0
                self._NoOfFailures += 1
                if agent1.getRole() == 1:
                    lWord = agent2.speak()
                    sWord = agent1.speak()
                    self._Map[lWord] -= 1
                    self._Map[sWord] += 1
                    agent2.hear(sWord)
                    if self._Map[lWord] < 1:
                        del self._Map[lWord]
                else:
                    lWord = agent1.speak()
                    sWord = agent2.speak()
                    self._Map[lWord] -= 1
                    self._Map[sWord] += 1
                    agent1.hear(sWord)
                    if self._Map[lWord] == 0:
                        del self._Map[lWord]
                if len(self._Map) == 1:
                    break
            self._Successes.append(self._NoOfSuccesses)
            self._Fails.append(self._NoOfFailures)

            BeliefUpdater.updateBelief (agent1, agent2, is_success)
            beliefs = self._getBeliefs()
            list.append(self._Beliefs, beliefs)
           self._Categories.append(1)
           for agent in self._Agents:
            print str(agent.getBelief()) + " " + agent.getCurrentWord()

params = {
             'backend': 'ps',
             'axes.labelsize': 10,
             'text.fontsize': 10,
             'legend.fontsize': 10,
             'xtick.labelsize': 8,
             'ytick.labelsize': 8,
             'text.usetex': True,
}

def plotBeliefs(beliefs, initialWords, convergedWord, log_scale=0):
    xlen = len(beliefs[0])
    x = pylab.arange(0, xlen, 1)
    y = pylab.arange(0, 1, 1/len(beliefs))
    clist = ('r', 'g', 'b', 'c', 'm', 'y', 'k')
    pylab.rcParams.update(params)
    a = 0
    pylab.xlabel("t\n Winning Word is: " + convergedWord, fontsize = 14)
    pylab.ylabel('Belief', fontsize = 14)
    for belief in beliefs:
        c = get_colours(xlen)
        pylab.plot(x, belief, lw = 2, label = initialWords[a])
        a +=1

    if (log_scale):
        pylab.yscale('log')
        pylab.xscale('log')

    pylab.legend()
    pylab.show()

def plotCategories(categories, log_scale=0):
    xlen = len(categories)
    x = pylab.arange(0, xlen, 1)
    #y = pylab.arange(0, 1, 1/len(beliefs))
    pylab.rcParams.update(params)
    pylab.xlabel("t", fontsize = 14)
    pylab.ylabel('NoOfCategories', fontsize = 14)
    pylab.plot(x, categories, lw = 2, label = "No of Categories")

    if (log_scale):
        pylab.yscale('log')
        pylab.xscale('log')

    pylab.legend()
    pylab.show()

def plotSuccessvsFails(successes, fails, log_scale=0):
    xlen = len(successes)
    x = pylab.arange(0, xlen, 1)
    pylab.rcParams.update(params)
    pylab.xlabel("t", fontsize = 14)
    pylab.ylabel('NoOfCategories', fontsize = 14)
    pylab.plot(x, successes, lw = 2, label = "No of Successes")
    pylab.plot(x, fails, lw = 2, label = "No of Failures")

    if (log_scale):
        pylab.yscale('log')
        pylab.xscale('log')

    pylab.legend()
    pylab.show()


def getSuccessRates(successes, fails):
    rates = []
    for i in range(0, len(successes)):
        rates.insert(i, successes[i] / (successes[i] + fails[i]))
    return rates

def getFailRates(successes, fails):
    rates = []
    for i in range(0, len(fails)):
        rates.insert(i, fails[i] / (successes[i] + fails[i]))
    return rates

def plotSuccessRates(successes, fails, log_scale=0):
    xlen = len(successes)
    x = pylab.arange(0, xlen, 1)
    pylab.rcParams.update(params)
    pylab.xlabel("t", fontsize = 14)
    pylab.ylabel('NoOfCategories', fontsize = 14)
    failRates = getFailRates(successes, fails)
    successRates = getSuccessRates(successes, fails)
    pylab.plot(x, failRates, lw = 2, label = "Fail Rates")
    pylab.plot(x, successRates, lw = 2, label = "Success Rates")

    if (log_scale):
        pylab.yscale('log')
        pylab.xscale('log')

    pylab.legend()
    pylab.show()

def main():
    cgcrbu = Sim()

    lex = ["Araba", "Bebek", "Kitap", "Baba", "Anne", "Kelebek", "Su", "Mama",
            "Yemek", "Adda", "Dede", "Puf", "Da", "Sabun", "Tren", "Nine",
            "Bebe", "Gece", "Sabah", "Masa", "Sehpa", "Sopa", "Kolpa", "Dolap",
            "Sokak", "Ev", "Deli", "Okul", "Koku", "Lavabo", "Kedi", "Veli",
            "Sokak", "Solak", "Manyak", "Salak", "Saat", "Vade", "Saka",
            "Sirk", "Firt", "Bot", "Kot", "Yat", "Bat", "Sat", "Kat", "Hat",
            "Bat", "Mat", "Pay", "Kar", "Hala", "Teyze", "Amca", "Proje",
            "Daire", "Yuvarlak", "Kare", "Sark", "Park", "Ben", "Erkek",
            "Adam", "Kiz", "Hiz", "Gaz", "Saz", "Kaz", "Hala", "Kola", "Balo",
            "Kart", "Sarp", "Harp", "Kan", "Kafa", "Bina", "Taban", "Saban",
            "Kaban", "Yaban", "Tavan", "Yavan", "Savan", "Hayvan", "Satan",
            "Sakal", "Bakkal", "Market", "Bilgi", "Ajan", "Bay", "Bayan",
            "Hatun", "Adam", "Saman", "Hakan", "Onur", "Bodur", "Korner",
            "Gol", "Manav", "Karpuz", "Kavun", "Karton", "Tok", "Yok", "Kil",
            "Sil", "Bil", "Pil", "Dil", "Dingil", "Silgi", "Kalem", "Motor",
            "Kart", "Nart", "Abart", "Sakat", "Tart", "Yat", "Mat", "Mart",
            "Dart", "Guatr", "Grip", "Nezle", "Sebze", "Meyve", "Mor", "Siyah",
            "Beyaz", "Lacivert", "Beyin", "Zihin", "Aroma", "Zamir", "Fiil",
            "Eylemsi", "Zarf", "Mektup", "Kasa", "Kazan", "Sazan", "Tarzan",
            "Hazan", "Murat", "Can", "Cem", "Cam", "Kan", "Tan", "Yan", "Ban",
            "Han", "Zan", "An", "Tren", "Yen", "Sen", "Ben", "O", "Bu"
           ]

    cgcrbu.setLexicon(lex)
    cgcrbu.setNoOfAgents(20)
    cgcrbu.setMaxDictSize(20)
    cgcrbu.initAgents()
    cgcrbu.playGames()

#    print cgcrbu.getCategories()
    beliefs = transposed(cgcrbu.getBeliefs())
    initialWords = cgcrbu.getInitialWords()
    plotBeliefs(beliefs, initialWords, cgcrbu.getConvergedWord(), 1)
#    print cgcrbu.getSuccesses()
#    print cgcrbu.getFailures()

#    plotCategories(cgcrbu.getCategories(), 1)
#    plotSuccessvsFails(cgcrbu.getSuccesses(), cgcrbu.getFailures(), 1)
    #plotSuccessRates(cgcrbu.getSuccesses(), cgcrbu.getFailures())
    noOfIterations = cgcrbu.getNoOfIterations()
    noOfSuccess = cgcrbu.getNoOfSuccesses()
    noOfFailures = cgcrbu.getNoOfFailures()

    print "Iterations " + str(noOfIterations)
    print "No of Successes " + str(noOfSuccess)
    print "No of Failures " + str(noOfFailures)

main()
