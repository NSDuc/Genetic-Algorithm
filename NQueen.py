from math import *
from random import *

class Chess:
	Size = 8
	Solution_Fit = 28
	

class Genetic():
	Generation = 200
	Population = 100
	Tournsize = 5
	# CXPB  is the probability with which two individuals are crossed
	#
	# MUTPB is the probability for mutating an individual
	CXPB, MUTPB = 0.5, 0.1
class Tools():
	def Creator():
		return [randint(1,Chess.Size) for _ in range(Chess.Size)]
	def EvalFit(val):
		fit = Chess.Solution_Fit
		for i in range(Chess.Size-1):
			for j in range(i+1,Chess.Size):
				if (val[i] == val[j]) | (abs(val[i] - val[j]) == abs(i-j)):
					fit -=1
		return fit

	def Mate(valA,valB):
		p = randint(1,Chess.Size-1)
		if random() > Genetic.CXPB :
			valX = valA[:p] + valB[p:]
			valY = valB[:p] + valA[p:]
			return valX, valY
		else:
			return valA, valB
	def Mutate(val):
		p = randint(1,Chess.Size-1)
		val[p] = randint(1,Chess.Size)
		return val 


class Individual:
	def __init__(self,val):
		self.val  = val
		self.fit  = Tools.EvalFit(val)

	def Mutate(self):
		self.val  = Tools.Mutate(self.val)
		self.fit  = Tools.EvalFit(self.val)


G  = 0
Pop = [Individual(Tools.Creator()) for _ in range(Genetic.Population)]

while(G < Genetic.Generation):
	G = G + 1

	Selects   = []
	for i in range(Genetic.Population):
		tour = sample(Pop,Genetic.Tournsize)
		fits = [ind.fit for ind in tour]

		select = Individual(tour[fits.index(max(fits))].val)
		Selects.append(select)

	Offsprings = []
	for ind1, ind2 in zip(Selects[::2],Selects[1::2]):
		val1, val2 = Tools.Mate(ind1.val,ind2.val)
		Offsprings.append(Individual(val1))
		Offsprings.append(Individual(val2))
	del Selects

	for ind in Offsprings:
		if random() < Genetic.MUTPB:
			ind.Mutate()

	Pop = Offsprings
	del Offsprings
	
	Fits = [ind.fit for ind in Pop]
	i   = Fits.index(max(Fits))
	length = len(Pop)
	mean = sum(Fits) / length
	sum2 = sum(x*x for x in Fits)
	std = abs(sum2 / length - mean**2)**0.5
	print("----------------------")
	print("max value when x = ",Pop[i].val)
	print("  Min %s" % min(Fits))
	print("  Max %s" % max(Fits))
	print("  Avg %s" % mean)
	print("  Std %s" % std)
	del Fits,i,length,mean,sum2,std
