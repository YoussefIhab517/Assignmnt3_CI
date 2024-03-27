import random
import numpy as np
def initialize_pop(size,variables,max,min):
    pop=[]
    for i in range(size):
        temp=[]
        for j in range(variables):
            temp.append(random.random()*4 - 2)
        pop.append(temp)
    return pop

def generate_chromosomes(number,length):
    chromosomes=[]
    i=0
    while(len(chromosomes)!=number):
        chromosomes.append("")
        for j in range(length):
            x= random.randint(0,1)
            chromosomes[i]+=str(x)
        i+=1
    return chromosomes
def choose_elite(chromosome,fitness):
      sorted_chromose = [chromosome for _, chromosome in sorted(zip(fitness, chromosome), reverse=True)]
      top_two =  sorted_chromose[:2]
      return top_two
def rank_fitness(population):
    fitness=[]
    for i in range(len(population)):
        fitness.append(8-(population[i][0]+0.0317)**2+population[i][1]**2)
    rank= np.array(fitness).argsort().argsort()+1
    sp=1+random.random()
    rank_fitness=[]
    for j in range(len(rank)):
        rank_fitness.append( (2-sp) + 2 * (sp - 1) * (rank[j]-1)/(len(fitness)-1) )
    return rank_fitness
def select(population,k,fitness):
    selected_individuals = []
    tournament_selection = random.sample(population, k) 
    tournament_fitness = rank_fitness(tournament_selection)
    winner = choose_elite(tournament_selection ,tournament_fitness)
    selected_individuals.append(winner)
    return selected_individuals
def arithmetic_crossover(parent1, parent2, pcross):
    child1 = []
    child2 = []
    if random.random() < pcross:
        for gene1, gene2 in zip(parent1, parent2):
            beta = random.uniform(0, 1)
            child1_gene = beta * gene1 + (1 - beta) * gene2
            child2_gene = (1 - beta) * gene1 + beta * gene2
            child1.append(child1_gene)
            child2.append(child2_gene)
    else:
        child1 = parent1
        child2 = parent2

    return child1, child2
def gaussian_mutation(individual, sigma, Pmut, Rmax, Rmin):
    mutated_individual = []
    for gene in individual:
        if random.random() < Pmut:
            mutation = random.gauss(0, sigma)
            mutated_gene = gene + mutation
            mutated_gene = max(min(mutated_gene, Rmax), Rmin) 
            mutated_individual.append(mutated_gene)
        else:
            mutated_individual.append(gene)
    return mutated_individual
runs=1
population_size=100
generations=100
pcross=0.6
pmut=0.05
sigma=0.5
k = int(input("enter tournament selection sample size: "))
for j in range(runs):
    print("run ",j+1)
    chromosomes = initialize_pop(population_size,2,2,-2)
    best_fitness=[]
    for i in range(generations):
        rank_fitnessess=rank_fitness(chromosomes)
        best_fitness.append(max(rank_fitnessess))
        new_population=[]
        while len(new_population)<len(chromosomes):
            selection=[]
            selection =select(chromosomes,k,rank_fitness)
            offspring= arithmetic_crossover(selection[0][0],selection[0][1],pcross)
            new_population.append(gaussian_mutation(offspring[0],sigma,pmut,2,-2))
            new_population.append(gaussian_mutation(offspring[1],sigma,pmut,2,-2))
        new_population=new_population[0:population_size-2]
        best=choose_elite(chromosomes,rank_fitnessess)
        new_population.extend(best)
        chromosomes=new_population.copy()
        if i==generations-1:
            print("final population: \n",chromosomes,"\n")
    print("best fitness history: \n",best_fitness,"\n")