from __future__ import division
import random
import sys
import pylab
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import nx_vtk
import math

import pylab_plotter

def transposed(lists):
	if not lists: return []
	return map(lambda *row: list(row), *lists)


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
	def _updateFail (agentT, agentL, sFun = None):
		agentT.setBelief( BeliefUpdater._updateFailTeacher(agentT.getBelief(),
			agentL.getBelief()), sFun)
		agentL.setBelief( BeliefUpdater._updateFailLearner(agentL.getBelief(),
			agentT.getBelief()), sFun)

	@staticmethod
	def _updateSuccess(agentT, agentL, sFun = None):
		agentT.setBelief(
				BeliefUpdater._updateSuccessTeacher(agentT.getBelief(),
					agentL.getBelief()), sFun)
		agentL.setBelief(
				BeliefUpdater._updateSuccessLearner(agentL.getBelief(),
					agentT.getBelief()), sFun)

	@staticmethod
	def updateBelief (agent1, agent2, is_success, sFun = None):
		if (agent1.getRole() == 1):
			if (is_success):
				BeliefUpdater._updateSuccess(agent1, agent2, sFun)
			else:
				BeliefUpdater._updateFail(agent1, agent2, sFun)
		elif (agent1.getRole() == 0):
			if (is_success):
				BeliefUpdater._updateSuccess (agent2, agent1, sFun)
			else:
				BeliefUpdater._updateFail (agent2, agent2, sFun)

class ScalingFunc:
	@staticmethod
	def scale (sFun, belief):
		if sFun != None:
			print "sFun " + sFun + " " + str(belief)
		if sFun == None:
			return belief
		elif sFun == "tanh":
			return ScalingFunc._tanhFunc(belief)
		elif sFun == "logistic":
			return ScalingFunc._logisticFunc(belief)

	@staticmethod
	def _logisticFunc(belief):
		return (1 / (1 + math.exp(-belief)))

	@staticmethod
	def _tanhFunc(belief):
		print math.tanh(belief)
		return math.tanh(belief)

class Agent:

	_Role = 0 # 1 if teacher
	_CurrentWord = ""
	_Belief = 0.0
	_Name = ""

	def setRole (self, role):
		self._Role = role

	def getRole (self):
		return self._Role

	def setBelief (self, belief, scalingFunc=None):
		self._Belief = ScalingFunc.scale(scalingFunc, belief)

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

	def getName(self):
		return self._Name

	def setName(self, name):
		self._Name = name

	def __str__(self):
		return self._CurrentWord + ", " + self._Name + ",\n " + str(round(self._Belief, 2))

class CGame:

	def __init__(self):
		self._Lexicon = []
		self._Agents = []
		self._Map = {}
		self._NoOfAgents = 10
		self._InitialWords = []
		self._NoOfSuccesses = 0
		self._NoOfFailures = 0
		self._NoOfIterations = 0
		self._MaxDict = 0
		self._Beliefs = []
		self._Categories = []
		self._Fails = []
		self._Successes = []
		self._Network = nx.DiGraph()

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

	def initAgents (self, noOfAgents=0, scalingFunc = None):
		if scalingFunc == 0:
			self.strScalingFunc = None
		elif scalingFunc == 1:
			self.strScalingFunc = "logistic"
		elif scalingFunc == 2:
			self.strScalingFunc = "tanh"
	
		if (self._Network == None):
			self._Network = nx.Graph()

		if (noOfAgents):
			self._NoOfAgents = noOfAgents
		for i in range (self._NoOfAgents):
			ag = Agent()
			rnd_word = self.chooseRandomWord()
			belief = random.uniform(0.05, 1)
		   # print rnd_word + str(belief)
			ag.setCurrentWord(rnd_word)
			ag.setBelief(belief)
			ag.setName(rnd_word)
			self._Network.add_node(ag)
			self._Agents.append(ag)

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

	def playGames (self, drawFlag = 0):
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
				self._Network.add_edge(agent1, agent2, weight=agent1.getBelief())
				agent1.setRole(1)
				agent2.setRole(0)
			elif (agent2.getBelief() > agent1.getBelief()):
				self._Network.add_edge(agent2, agent1, weight=agent2.getBelief())
				agent1.setRole(0)
				agent2.setRole(1)
			else:
				self._Network.add_edge(agent1, agent2, weight=agent1.getBelief())
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

			BeliefUpdater.updateBelief (agent1, agent2, is_success, self.strScalingFunc)
			beliefs = self._getBeliefs()
			list.append(self._Beliefs, beliefs)

		self._Categories.append(1)
		for agent in self._Agents:
			print str(agent.getBelief()) + " " + agent.getCurrentWord()
		if (drawFlag):
			self.draw()

	def draw(self, dim=3):
		pos = nx.random_layout(self._Network, dim=3)
		nx_vtk.draw_nxvtk(self._Network, pos)
		nx.write_dot(self._Network, "net.dot")
		plt.savefig("network.png")

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

def main():
	cgcrbu = CGame()
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
			"Han", "Zan", "An", "Tren", "Yen", "Sen", "Ben", "O", "Bu", "Kaba",
			"Seda", "Kadir", "Sinkaf", "Arif", "Tarif", "Sahip", "Tayyip",
			"Rahip", "Cazip", "Katip", "Kamil", "Samil"
			]

	cgcrbu.setLexicon(lex)
	cgcrbu.setNoOfAgents(20)
	cgcrbu.setMaxDictSize(10)
	cgcrbu.initAgents(1)
	cgcrbu.playGames(0)

#   print cgcrbu.getCategories()

	beliefs = transposed(cgcrbu.getBeliefs())
	initialWords = cgcrbu.getInitialWords()
	plotBeliefs(beliefs, initialWords, cgcrbu.getConvergedWord(), 0)

	print cgcrbu.getSuccesses()
	print cgcrbu.getFailures()
	plotCategories(cgcrbu.getCategories(), 0)
	plotSuccessvsFails(cgcrbu.getSuccesses(), cgcrbu.getFailures(), 0)
	
	successRates = getSuccessRates(cgcrbu.getSuccesses(), cgcrbu.getFailures())
	failRates = getFailRates(cgcrbu.getSuccesses(), cgcrbu.getFailures())
	plotSuccessRates(successRates,failRates, 0)

	noOfIterations = cgcrbu.getNoOfIterations()
	noOfSuccess = cgcrbu.getNoOfSuccesses()
	noOfFailures = cgcrbu.getNoOfFailures()

	print "Iterations " + str(noOfIterations)
	print "No of Successes " + str(noOfSuccess)
	print "No of Failures " + str(noOfFailures)

#main()
