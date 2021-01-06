import numpy as np
import random
from copy import deepcopy
import matplotlib.pyplot as plt
def initialize(N):
    Map = np.zeros((N,N))
    for i in range( 0 , N):
        for j in range(0 , i):
            Map[i][j] = random.randint(0,6)
            Map[j][i] = Map[i][j]
    return Map
def Print(N , Map):
    for i in range(N):
        print(i , "->  ", end = " ")
        for j in range(0,N):
            if j==N-1:
                print(Map[i][j])
            else:
                print(Map[i][j], end = " , ")

def repeat(num , individual):
    if len(individual)==0:
        return False

    for i in individual:
        if i==num:
            return True
    return False

def initial_individual(N):
    individual = []
    while len(individual) < N:
        num = random.randint(0 , N*10)%N
        if (repeat(num , individual)==False):
            individual.append(num)
    individual.append(individual[0])
    return individual


def Score(Map , individual):
    score = 0
    for i in range(1 , len(individual)):
        if(Map[individual[i-1]][individual[i]]!=0):
            score+=Map[individual[i-1]][individual[i]]
        else:
            score = 1000000
            break
    return score

def initial_population(M, N, Map):
    population = []
    while len(population) < M:
        individual = initial_individual(N)
        if (repeat(individual, population)==False and Score(Map, individual)!=1000000):
            population.append(individual)


    return population

def mutate(individual):
    N = len(individual)
    x = deepcopy(individual)
    while True:
        i = random.randint(1 , N-1)%(N-1)
        j = random.randint(1 , N-1)%(N-1)
        if i!=j:
            individual[i] , individual[j] = individual[j] , individual[i]
            break;
    # for i in range(len(individual)-1):
    #
    #     for j in range(len(individual[:-1])):
    #         if individual[j]==individual[i] and i!=j:
    #             print(individual, "repeat" , x)
    #             return individual

    individual[-1] = individual[0]
    return individual

def crossover(a , b):
    a_1 = deepcopy(a)
    b_1 = deepcopy(b)

    pivot =random.randint(1, len(a)-2)%len(a)

    for i in range(pivot , len(a)-1):
        j = a_1.index(b[i] , 0 , len(a)-1)
        a_1[i] , a_1[j] = a_1[j] , a_1[i]

    for i in range(0 , pivot):
        j = b_1.index(a[i] , 0 , len(b)-1)
        b_1[i] , b_1[j] = b_1[j], b_1[i]
    if a_1[0]!=a_1[-1]:
        a_1[-1] = deepcopy(a_1[0])
    if b_1[0]!=b_1[-1]:
        b_1[-1] = deepcopy(b_1[0])

    return a_1 , b_1
def swap_top(a):
    n = len(a)
    pi = random.randint(1 , n-2)
    a[pi] , a[0] = a[0],a[pi]
    a[-1] = a[0]
    return a
def min_score(Map, population):
    min_1 = 1000000
    path_1 = []
    min_2 = 1000000
    path_2 = []
    for i in population:
        a = Score(Map,  i)
        if a < min_1:
            min_1 = a
            path_1 = deepcopy(i)
        if a >= min_1 and path_1!=i and a < min_2:
            min_2 = a
            path_2 = deepcopy(i)
    return path_1 , path_2
def sort_population(population , Map):
    population = sorted(population , key = lambda x : Score(Map , x))
    return population
def fitness(Map , population , gen):
    mini = 1000000
    path = []
    for j in range(0 , gen):
        new_population = []
        population = sort_population(population, Map)
        a = deepcopy(population[0])
        b = deepcopy(population[1])
        a , b = crossover(a , b)
        new_population.append(a)
        new_population.append(b)
        for i in population:
            a  = Score(Map, i)
            if a < mini:
                mini = a
                path = deepcopy(i)
            x = mutate(deepcopy(i))
            if Score(Map ,x) < a:
                new_population.append(x)
            # else:
            #     new_population.append(deepcopy(i))
            x = swap_top(deepcopy(i))
            if Score(Map, x) < a:
                new_population.append(x)
        population = new_population
    return mini , path
