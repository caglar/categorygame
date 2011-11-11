from __future__ import division
import pylab
import numpy as np
import networkx as nx
import nx_vtk
from matplotlib.colors import colorConverter

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
	print "Beliefs"
	numBeliefs = len(beliefs)
	x = pylab.arange(0, xlen, 1)
	y = pylab.arange(0, 1, 1/numBeliefs)
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
	pylab.ioff()
	pylab.draw()
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
	pylab.draw()
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
	pylab.ioff()
	pylab.draw()
	pylab.show()


def plotSuccessRates(successRates, failRates, log_scale=0):
	xlen = len(successes)
	x = pylab.arange(0, xlen, 1)
	pylab.rcParams.update(params)
	pylab.xlabel("t", fontsize = 14)
	pylab.ylabel('NoOfCategories', fontsize = 14)
	pylab.plot(x, failRates, lw = 2, label = "Fail Rates")
	pylab.plot(x, successRates, lw = 2, label = "Success Rates")

	if (log_scale):
		pylab.yscale('log')
		pylab.xscale('log')

	pylab.legend()
	pylab.raw()
	pylab.show()
