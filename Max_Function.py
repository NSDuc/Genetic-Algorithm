from math import *
from random import *



class Function():
	xMin = 0
	xMax = 5
	def y(x):
		return (4*pow(x,4) - 5*pow(x,3) + exp(-2*x)  - 7*sin(x) - 3*cos(x))		

class Genetic():
	Resolution = 20
	Generation = 200
	Population = 200
	Tournsize = 5
	# CXPB  is the probability with which two individuals are crossed
	#
	# MUTPB is the probability for mutating an individual
	CXPB, MUTPB = 0.5, 0.2
class Tools():
	def Creator():
		return uniform(Function.xMin,Function.xMax)
	def EvalFit(val):
		return Function.y(val)

	def Encode(val):
		gen = int((val-Function.xMin)/(Function.xMax - Function.xMin)* (2**Genetic.Resolution-1))
		return gen
	def Decode(gen):
		val = (gen *(Function.xMax - Function.xMin) / (2**Genetic.Resolution-1)) + Function.xMin
		return val

	def Mate(gen1,gen2):
		p = randint(0,Genetic.Resolution-1)
		left  = int('1'*(p-1) + '0'*(Genetic.Resolution-p+1),2)
		right = int('0'*(p-1) + '1'*(Genetic.Resolution-p+1),2)
		if random() > Genetic.CXPB:
			ret1  = (gen1 & left) | (gen2 & right)
			ret2  = (gen2 & left) | (gen1 & right)
			return  ret1, ret2
		else:
			return gen1, gen2
	def Mutate(gen):
		p = randint(0,Genetic.Resolution-1)
		mask = '1'*(p-1) + '0' + '1'*(Genetic.Resolution-p)
		return gen & int(mask,2)


class Individual:
	def __init__(self,val):
		self.val  = val
		self.fit  = Tools.EvalFit(val)
		self.gen  = Tools.Encode(val)

	def Mutate(self):
		self.gen  = Tools.Mutate(self.gen)
		self.val  = Tools.Decode(self.gen)
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
		gen1, gen2 = Tools.Mate(ind1.gen,ind2.gen)
		val1 = Tools.Decode(gen1)
		val2 = Tools.Decode(gen2)
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



	



