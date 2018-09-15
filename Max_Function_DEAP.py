import random

from math import *

from deap import base
from deap import creator
from deap import tools


class Function():
	xMin = 0
	xMax = 5

	def y(x):
		return (4*pow(x,4) - 5*pow(x,3) + exp(-2*x)  - 7*sin(x) - 3*cos(x))

creator.create("FitnessMax", base.Fitness, weights = (1.0,)) 
creator.create("Individual", list, fitness = creator.FitnessMax)


toolbox = base.Toolbox()
#Attribute Generator
toolbox.register("attr_float",random.uniform,Function.xMin,Function.xMax)
#Structure Initializers
IND_SIZE = 1
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n = IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)



def evalOneMax(individual):
    x = individual[0]
    y = Function.y(x)
    return y,


toolbox.register("evaluate", evalOneMax)
#toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta = 0.2, low = Function.xMin, up = Function.xMax)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.04)       #*********************
toolbox.register("mutate", tools.mutPolynomialBounded, eta = 0.1, low = Function.xMin, up = Function.xMax, indpb=0.04)

toolbox.register("select", tools.selTournament, tournsize=3)   

def main():
    random.seed(64)
    pop = toolbox.population(n = 200)

    fitnesses = list(map(toolbox.evaluate,pop))
    for ind,fit in zip(pop,fitnesses):
        ind.fitness.values = fit

    # CXPB  is the probability with which two individuals are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2


    g = 0 
    fits = [ind.fitness.values[0] for ind in pop]
    while (g < 100):
        g = g + 1 

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1 , child2 in zip(offspring[::2],offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1,child2)
                del child1.fitness.values
                del child2.fitness.values

        
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values


        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate,invalid_ind)
        for ind,fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit


        pop[:] = offspring


        fits = [ind.fitness.values[0] for ind in pop]
        i   = fits.index(max(fits))
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        #print(pop)
        print("----------------------")
        print("max value when x = ",pop[i])
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)


if __name__ == "__main__":
    main()